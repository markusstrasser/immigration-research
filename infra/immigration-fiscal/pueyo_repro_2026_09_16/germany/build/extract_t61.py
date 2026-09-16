import openpyxl, csv
RAW='/Users/alien/Projects/immigration-research/infra/immigration-fiscal/pueyo_repro_2026_09_16/germany/raw'
wb=openpyxl.load_workbook(f'{RAW}/T61_bund_2025.xlsx',read_only=True,data_only=True)
ws=wb['T61']
KEYS={'------':'total_all','890000':'total_excl_imm','892000':'violent','100000':'sexual',
      '010000':'murder','020000':'manslaughter','725000':'imm_offences','892500':'homicide_all'}
cols=['tv_insg','nd_anzahl','nd_anteil','kein_aufenthalt','unerlaubt','erlaubt','asylbewerber',
      'schutz_asylber','duldung','sonstiger_erlaubt','zuwanderer']
recs=[]
for r in ws.iter_rows(min_row=8,values_only=True):
    k=str(r[0]).strip() if r[0] is not None else ''
    if k in KEYS and str(r[2]).strip()=='X':
        rec={'key':k,'offence':KEYS[k],'label':str(r[1])}
        for i,c in enumerate(cols): rec[c]=r[3+i]
        recs.append(rec)
with open(f'{RAW}/../t61_residence_status_2025.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(recs[0])); w.writeheader(); w.writerows(recs)
for r in recs:
    nd=r['nd_anzahl']
    print(f"{r['offence']:16s} nd={nd:>8} unerlaubt={r['unerlaubt']:>7} ({r['unerlaubt']/nd:6.1%}) kein_auf={r['kein_aufenthalt']:>6} ({r['kein_aufenthalt']/nd:5.1%}) asylb={r['asylbewerber']:>6} duldung={r['duldung']:>6} sonst_erl={r['sonstiger_erlaubt']:>7}")
