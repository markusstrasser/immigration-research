#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1", "pymupdf>=1.26"]
# ///
"""Reconcile RPC state, nationality, month and grand-total cells.

Native-First: official XLSX cells and PDF text geometry are sufficient. This
script only emits rederivable CSV/JSON in ignored scratch; no causal model.
"""
from __future__ import annotations
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
import pymupdf
import openpyxl

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / ".scratch/clarity-next-20260905/admission"
MONTHS = "Oct Nov Dec Jan Feb Mar Apr May Jun Jul Aug Sep".split()


def repair_ocr_row(page, group, first_num, centers, active_months, original):
    """Re-read mismatching raster rows; do not infer a cell from the total."""
    values=[0]*13
    for w in group:
        if w[0]<first_num or not re.fullmatch(r"[\d,]+",w[4]):
            continue
        rect=pymupdf.Rect(w[0]-1,w[1]-2,w[2]+1,w[3]+2)
        png=page.get_pixmap(matrix=pymupdf.Matrix(6,6),clip=rect).tobytes("png")
        out=subprocess.run(["tesseract","stdin","stdout","--psm","7","-c","tessedit_char_whitelist=0123456789,"],input=png,capture_output=True,check=True)
        s=out.stdout.decode().strip()
        if not re.fullmatch(r"[\d,]+",s):
            raise ValueError(("OCR cell unreadable",w,s))
        x=(w[0]+w[2])/2
        ci=min(range(len(centers)),key=lambda i:abs(x-centers[i]))
        col=12 if ci==len(active_months) else MONTHS.index(active_months[ci])
        values[col]=int(s.replace(",",""))
    if sum(values[:12])!=values[12] or not values[12]:
        raise ValueError(("OCR row did not reconcile",original,values))
    return values


def rpc_pdf(path, year):
    rows, grand = [], None
    current_state = None
    state_totals = {}
    for page_no, page in enumerate(pymupdf.open(path), 1):
        words = page.get_text("words")
        if not any(w[4] in MONTHS for w in words):
            cached = STAGE / f"rpc{year}_ocr" / f"page{page_no:02}.json"
            if cached.exists():
                cached_data=json.loads(cached.read_text())
                assert cached_data["sha256"]==hashlib.sha256(path.read_bytes()).hexdigest()
                words=cached_data["words"]
            else:
                tp=page.get_textpage_ocr(dpi=300,full=True,tessdata="/opt/homebrew/share/tessdata")
                words=page.get_text("words",textpage=tp)
                cached.parent.mkdir(exist_ok=True)
                cached.write_text(json.dumps({"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"words":words,"engine":"Tesseract via PyMuPDF,300dpi"}))
        month_words = [w for w in words if w[4] in MONTHS]
        if not month_words:
            continue
        header_y = min(w[1] for w in month_words)
        headers = {w[4]: (w[0]+w[2])/2 for w in month_words if abs(w[1]-header_y)<2}
        active_months=[m for m in MONTHS if m in headers]
        assert len(headers) == (9 if year==2026 else 12), (path.name, page_no, headers)
        xstep = headers[active_months[1]] - headers[active_months[0]]
        centers = [headers[m] for m in active_months] + [headers[active_months[-1]]+xstep]
        first_num = centers[0]-xstep/2
        # Original 2022/23 layout has country x=120.77; newer condensed layout x=74.60.
        country_x = 111 if year==2026 else (113 if year==2024 else (120 if first_num > 160 else 74))
        y_groups = []
        for word in sorted(words, key=lambda w:(w[1],w[0])):
            if word[1] <= header_y+4 or word[1]>page.rect.height-45:
                continue
            if not y_groups or abs(word[1]-y_groups[-1][0]) > 2.5:
                y_groups.append([word[1], []])
            y_groups[-1][1].append(word)
        for y, group in y_groups:
            group.sort(key=lambda w:w[0])
            left = " ".join(w[4] for w in group if w[0]<country_x-1)
            country = " ".join(w[4] for w in group if country_x-1<=w[0]<first_num)
            number_words = [w for w in group if w[0]>=first_num and re.fullmatch(r"[\d,]+",w[4])]
            if not number_words or any(not re.fullmatch(r"[\d,]+",w[4]) for w in group if w[0]>=first_num):
                continue
            values = [0]*13
            used = set()
            for w in number_words:
                ci = min(range(len(centers)), key=lambda i:abs((w[0]+w[2])/2-centers[i]))
                col = 12 if ci==len(active_months) else MONTHS.index(active_months[ci])
                assert col not in used, (path.name,page_no,y,col,group)
                used.add(col)
                values[col] = int(w[4].replace(",",""))
            if sum(values[:12])!=values[12] and year in (2022,2024):
                values=repair_ocr_row(page,group,first_num,centers,active_months,values)
            assert sum(values[:12])==values[12], (path.name,page_no,left,country,values)
            if left.replace(" ","")=="GrandTotal":
                assert grand is None
                grand = values
                continue
            if left:
                current_state = left
            if country=="Total":
                assert current_state not in state_totals
                state_totals[current_state]=values
            elif country:
                assert current_state
                rows.append(dict(fiscal_year=year,state=current_state,nationality=country,
                                 page=page_no,**dict(zip(MONTHS+["Total"],values))))
            else:
                raise ValueError(("Unlabeled data row",path.name,page_no,y,left,values))
    assert grand is not None, path
    country_sums = defaultdict(lambda:[0]*13)
    states = defaultdict(lambda:[0]*13)
    for row in rows:
        for i,k in enumerate(MONTHS+["Total"]):
            country_sums[row["nationality"]][i]+=row[k]
            states[row["state"]][i]+=row[k]
    assert [sum(v[i] for v in country_sums.values()) for i in range(13)]==grand, (path.name,grand,sum(v[12] for v in country_sums.values()))
    for state, values in state_totals.items():
        assert states[state] == values, (path.name,state,values,states[state])
    monthly_totals = dict(zip(MONTHS, grand[:12]))
    coverage = "Complete fiscal year; October through September observed"
    if year == 2026:
        # The source omits October, and all displayed nonnegative month counts
        # exhaust its FY-to-date total. August/September are future, not zero.
        assert grand[0] == grand[10] == grand[11] == 0
        for month in ("Aug", "Sep"):
            monthly_totals[month] = None
            for row in rows:
                row[month] = None
        coverage = "Through 2026-07-31; Nov-Jul displayed; omitted Oct=0 derived from total; Aug-Sep unobserved/null"
    return rows, dict(source=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                      fiscal_year=year,grand_total=grand[12],monthly_totals=monthly_totals,coverage=coverage,
                      country_totals={k:v[12] for k,v in sorted(country_sums.items())},
                      countries=len(country_sums),states=len(states),rows=len(rows),
                      checks="every row months=total; sum country-months=national month; all available state totals reconciled")


def rpc2019(path):
    sheet=openpyxl.load_workbook(path,data_only=True,read_only=True).active
    countries=defaultdict(int); states=defaultdict(int); expected={}; state=None; rows=[]
    for rowno,r in enumerate(sheet.values,1):
        if len(r)<4 or not isinstance(r[2],(int,float)):
            continue
        assert r[2]==r[3]
        if r[0]=="Total":
            grand=r[2]
        elif r[0]:
            state=r[0];expected[state]=r[2]
        elif r[1]:
            countries[r[1]]+=r[2];states[state]+=r[2]
            rows.append(dict(fiscal_year=2019,state=state,nationality=r[1],row=rowno,total=r[2]))
    assert states==expected and sum(countries.values())==grand
    return dict(fiscal_year=2019,grand_total=grand,country_totals=dict(countries),states=len(states),countries=len(countries),rows=len(rows),checks="state-country sums=state totals; national=state sum; cumulative=FY count; no monthly cells in source",source=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest()),rows


def write_csv(name, rows):
    with (STAGE/name).open("w") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def lpr():
    path=STAGE/"ohss_lpr2024.xlsx"
    w=openpyxl.load_workbook(path,read_only=True,data_only=True)
    rows=list(w["Table 6"].values); years=rows[5][1:]; category=None; out=[]
    for r in rows[6:]:
        if r[0] in ("TOTAL","ADJUSTMENTS OF STATUS","NEW ARRIVALS"):
            category=r[0]
        elif isinstance(r[1],(int,float)):
            for y,v in zip(years,r[1:]):
                if y in (2019,2022,2023,2024):
                    out.append(dict(fiscal_year=y,type=category,admission_class=r[0],count=v))
    ix={(r["fiscal_year"],r["type"],r["admission_class"]):r["count"] for r in out}
    for (y,t,c),v in ix.items():
        if t=="TOTAL":
            assert abs(v-ix[y,"ADJUSTMENTS OF STATUS",c]-ix[y,"NEW ARRIVALS",c])<=15
    write_csv("lpr_type_class_selected_years.csv",out)
    countries=[]
    country_mode=False
    for r in w["Table 3"].values:
        if r[0]=="COUNTRY":country_mode=True;continue
        if country_mode and isinstance(r[1],(int,float)):
            for y,v in zip(years,r[1:]):
                if y in (2019,2022,2023,2024):countries.append(dict(fiscal_year=y,country_of_birth=r[0],count=v))
    write_csv("lpr_country_selected_years.csv",countries)
    wb=openpyxl.load_workbook(STAGE/"ohss_lpr2024_newadj.xlsx",read_only=True,data_only=True)
    tables=[]; country_maps={}; audit=[]
    for typ,sheet in [("TOTAL",w["Table 10"]),("NEW ARRIVALS",wb["Table 10 New Arrivals"]),("ADJUSTMENTS OF STATUS",wb["Table 10 Adjust"])]:
        vals=list(sheet.values);header=vals[5];countries_started=False;cm={}
        for r in vals[6:]:
            if r[0]=="COUNTRY":countries_started=True;continue
            if not countries_started or not isinstance(r[1],(int,float)):continue
            cm[r[0]]=list(r[1:])
            assert abs(r[1]-sum(r[2:]))<=35,(typ,r)
            for c,v in zip(header[1:],r[1:]):tables.append(dict(fiscal_year=2024,type=typ,country_of_birth=r[0],admission_class=c,count=v))
        total=cm["Total"]
        for j,c in enumerate(header[1:]):
            difference=sum(v[j] for k,v in cm.items() if k!="Total")-total[j]
            assert abs(difference)<=5*len(cm),(typ,c,difference)
            audit.append(dict(type=typ,column=c,country_sum_minus_published_total=difference,rounding_bound=5*len(cm)))
        country_maps[typ]=cm
    write_csv("lpr_country_type_class_2024.csv",tables)
    # Country suppression baskets differ; only common individually named countries can bridge.
    mismatches=[]
    shared=set.intersection(*(set(cm) for cm in country_maps.values()))-{"All other countries1"}
    for c in shared:
        a=country_maps["ADJUSTMENTS OF STATUS"][c];n=country_maps["NEW ARRIVALS"][c];t=country_maps["TOTAL"][c]
        for j in range(7):
            difference=a[j]+n[j]-t[j]
            if abs(difference)>15:mismatches.append((c,j,difference))
    assert not mismatches,mismatches
    return dict(rounding="Each published cell rounded to nearest10, not exact counts",table6_type_checks=True,country_column_checks=audit,common_country_type_checks=len(shared),somalia2024={typ:cm["Somalia"] for typ,cm in country_maps.items()},national={str(y):{typ:ix[y,typ,"Total"] for typ in ("TOTAL","NEW ARRIVALS","ADJUSTMENTS OF STATUS")} for y in (2019,2022,2023,2024)})


def ead():
    path=STAGE/"uscis_i765_fy2026_q2.xlsx"
    ws=openpyxl.load_workbook(path,data_only=True,read_only=True).active
    vals=list(ws.values);out=[];rows=[]
    for r in vals[5:]:
        if len(r)<22 or not isinstance(r[2],(int,float)):continue
        rows.append(r)
        for j,typ in enumerate(("initial","renewal","replacement","not_requested","total")):
            out.append(dict(category=r[0],description=r[1],filing_type=typ,receipts=r[2+4*j],approvals=r[3+4*j],denials=r[4+4*j],pending=r[5+4*j]))
        for j in range(4):assert sum(r[2+j+4*k] for k in range(4))==r[18+j],r
    column_checks=[dict(column=j+1,category_sum=sum(r[j] for r in rows[1:]),published_total=rows[0][j],difference=sum(r[j] for r in rows[1:])-rows[0][j]) for j in range(2,22)]
    source_exceptions = {6: -2, 18: -1, 22: -3}
    assert all(c["difference"] == source_exceptions.get(c["column"], 0) for c in column_checks), column_checks
    write_csv("ead_category_filing_fy2026_q2.csv",out)
    p=list(openpyxl.load_workbook(STAGE/"uscis_i765_pending_fy2026_q2.xlsx",data_only=True,read_only=True).active.values)
    pending=[]
    for j,(typ,cat) in enumerate((("initial","c8"),("initial","all"),("renewal","c8"),("renewal","all")),1):
        assert sum(r[j] for r in p[6:11])==p[5][j]
        pending.append(dict(filing_type=typ,category=cat,total=p[5][j],at_least180days=p[10][j],share_at_least180days=p[10][j]/p[5][j]))
    write_csv("ead_pending_age_fy2026_q2.csv",pending)
    return dict(flow_row_checks=True,flow_column_checks=column_checks,pending_bucket_checks=True,pending=pending,
                cross_report_differences=[dict(filing_type=t,pending_age_report=next(r["total"] for r in pending if r["category"]=="all" and r["filing_type"]==t),category_flow_report=next(r["pending"] for r in out if r["category"]=="Total" and r["filing_type"]==t)) for t in ("initial","renewal")],
                data_systems="Flow:CLAIMS3+ELIS PAER0020935; pending-age:NPD PAER0020915; both queried April2026. Different reports are not forced equal.")


def ohss_refugees():
    w=openpyxl.load_workbook(STAGE/"ohss_refugees2024.xlsx",data_only=True,read_only=True)
    rows=list(w["Table 14"].values);years=rows[5][1:11];country=False;out=[]
    for r in rows:
        if r[0]=="COUNTRY":country=True;continue
        if not country or not isinstance(r[1],(int,float)):continue
        for y,v in zip(years,r[1:11]):
            if y in (2019,2022,2023,2024):out.append(dict(fiscal_year=y,country_of_nationality=r[0],count=v))
    audit=[]
    for y in (2019,2022,2023,2024):
        ys=[r for r in out if r["fiscal_year"]==y]
        total=next(r["count"] for r in ys if r["country_of_nationality"]=="Total")
        difference=sum(r["count"] for r in ys if r["country_of_nationality"]!="Total")-total
        assert abs(difference)<=5*len(ys)
        audit.append(dict(year=y,total=total,somalia=next(r["count"] for r in ys if r["country_of_nationality"]=="Somalia"),country_sum_minus_total=difference,countries=len(ys)-1))
    write_csv("ohss_refugees_country_selected_years.csv",out)
    return audit


def quarterly():
    out=[];audit=[]
    for path in sorted(STAGE.glob("ohss_legal_fy*q4.xlsx")):
        year=int(path.name[13:17]);w=openpyxl.load_workbook(path,data_only=True,read_only=True)
        item=dict(year=year,source=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),tables={})
        for sn in ("Table 1A","Table 1B","Table 2"):
            vals=list(w[sn].values)
            country_mode=sn=="Table 1B"
            title=" ".join(str(r[0]) for r in vals[:6])
            country_basis="nationality" if "NATIONALITY" in title else "birth" if "BIRTH" in title else "not_applicable"
            taken=[]
            for rowno,r in enumerate(vals,1):
                if str(r[0]).strip()=="COUNTRY":country_mode=True;continue
                if not country_mode or len(r)<6 or not isinstance(r[1],(int,float)):continue
                r=list(r[:16 if sn!="Table 2" else 6]);taken.append(r)
                blocks=("total","adjustment","new_arrival") if sn!="Table 2" else ("refugee",)
                for j,typ in enumerate(blocks):
                    v=r[1+5*j:6+5*j]
                    if all(isinstance(n,(int,float)) for n in v):
                        assert abs(sum(v[1:])-v[0])<=25,(path.name,sn,r)
                    out.append(dict(year=year,source=path.name,sheet=sn,row=rowno,country_basis=country_basis,label=r[0],type=typ,total=v[0],q1=v[1],q2=v[2],q3=v[3],q4=v[4]))
                if sn!="Table 2" and all(isinstance(x,(int,float)) for x in r[1:16]):
                    assert all(abs(r[1+k]-r[6+k]-r[11+k])<=15 for k in range(5)),(path.name,sn,r)
            totals=next(r for r in taken if r[0]=="Total")
            if sn!="Table 1B":
                diffs=[]
                for j in range(1,len(totals)):
                    numeric=[r[j] for r in taken if r[0]!="Total" and isinstance(r[j],(int,float))]
                    missing=sum(not isinstance(r[j],(int,float)) for r in taken if r[0]!="Total")
                    difference=sum(numeric)-totals[j]
                    if not missing:assert abs(difference)<=5*len(taken),(path.name,sn,j,difference)
                    diffs.append(dict(column=j+1,sum_minus_total=difference,non_numeric_cells=missing))
                item["tables"][sn]=dict(country_basis=country_basis,total=totals,Somalia=next((r for r in taken if r[0]=="Somalia"),None),country_column_checks=diffs)
            else:item["tables"][sn]=dict(total=totals)
        assert item["tables"]["Table 1A"]["total"][1:]==item["tables"]["Table 1B"]["total"][1:]
        audit.append(item)
    write_csv("ohss_quarterly_country_type_class_selected_years.csv",out)
    return audit


def main():
    manifest=json.loads((STAGE/"manifest.json").read_text())
    for name, record in manifest.items():
        if name.endswith((".xlsx", ".pdf", ".json")):
            assert hashlib.sha256(Path(record["path"]).read_bytes()).hexdigest() == record["sha256"], ("Source hash changed", name)
    results=[]
    all_rows=[]
    errors=[]
    source_limits=[]
    if "rpc_fy2019.xlsx" in manifest:
        result,rows=rpc2019(Path(manifest["rpc_fy2019.xlsx"]["path"]));results.append(result)
        write_csv("rpc_state_nationality_2019.csv",rows)
        print("rpc2019",result["grand_total"],"Somalia",result["country_totals"].get("Somalia",0),flush=True)
    for name, record in manifest.items():
        if not re.fullmatch(r"rpc_fy\d{4}(?:_july)?\.pdf",name):
            continue
        if name in ("rpc_fy2022.pdf","rpc_fy2024.pdf") and "--audit-raster" not in sys.argv:
            source_limits.append(dict(file=name,reason="Raster/malformed-font PDF audit did not fully reconcile; complete official OHSS country tables are provided under their own nationality definition and vintage, never spliced into RPC."))
            continue
        try:
            rows, result=rpc_pdf(Path(record["path"]),int(name[6:10]))
            results.append(result); all_rows.extend(rows)
            print(name,result["grand_total"],"Somalia",result["country_totals"].get("Somalia",0),flush=True)
        except Exception as exc:
            errors.append(dict(file=name,error=str(exc)))
            print("[FAILED]",name,str(exc),flush=True)
    (STAGE/"rpc_results.json").write_text(json.dumps(dict(results=results,errors=errors,source_limits=source_limits),indent=2)+"\n")
    (STAGE/"lpr_results.json").write_text(json.dumps(lpr(),indent=2)+"\n")
    (STAGE/"ead_results.json").write_text(json.dumps(ead(),indent=2)+"\n")
    (STAGE/"ohss_refugees_results.json").write_text(json.dumps(ohss_refugees(),indent=2)+"\n")
    (STAGE/"ohss_quarterly_results.json").write_text(json.dumps(quarterly(),indent=2)+"\n")
    if all_rows:
        with (STAGE/"rpc_state_nationality_month.csv").open("w") as f:
            writer=csv.DictWriter(f,fieldnames=list(all_rows[0]));writer.writeheader();writer.writerows(all_rows)
    return bool(errors)


if __name__=="__main__":
    raise SystemExit(main())
