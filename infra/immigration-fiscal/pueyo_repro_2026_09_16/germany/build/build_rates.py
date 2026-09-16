"""Build de_nationality_rates.csv: PKS 2025 T62 suspects / AZR 31.12.2025 residents."""
import csv, json, os
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(D,'raw')

t62={r['bka_name']:r for r in csv.DictReader(open(os.path.join(D,'t62_suspects_2025.csv')))}
azr={r['name_de']:r for r in csv.DictReader(open(os.path.join(D,'azr_nationality_2025.csv')))}
cw=json.load(open(os.path.join(D,'build','crosswalk_bka_azr.json')))
alias=json.load(open(os.path.join(D,'build','iso3_alias.json')))
mus={r['name_de']:r for r in csv.DictReader(open(os.path.join(D,'build','muslim_majority.csv')))}
wb=json.load(open(os.path.join(RAW,'wb_gdp_2023.json')))[1]
gdp_by_iso={e['countryiso3code']:e['value'] for e in wb if e['value'] is not None}
wbname={e['country']['value']:e['countryiso3code'] for e in wb}

# German baseline (Bevoelkerungsfortschreibung 12411-0007, 31.12.2025)
GER_POP=71036222
GER_POP_M1839=8571972
ger=t62['Deutschland']
MEAS=['total_all','total_excl_imm','violent','sexual','murder','manslaughter','homicide_all','imm_offences']
ger_rate={m:int(ger[m])/GER_POP*1e5 for m in MEAS}

def azr_rows(bka_name):
    if bka_name in cw:
        return [azr[n] for n in cw[bka_name] if n in azr]
    return [azr[bka_name]] if bka_name in azr else []

out=[]
for name,r in t62.items():
    if r['bka_code'] in ('','...','000'): continue
    if name in ('Ungeklärt','Ohne Angabe','Staatenlos'): continue
    rows=azr_rows(name)
    if not rows: 
        out.append(dict(bka_name=name,matched=0)); continue
    pop=sum(int(x['pop_2025']) for x in rows)
    pop24=sum(int(x['pop_2024']) for x in rows)
    m1839=sum(int(x['male_18_39_2025']) for x in rows)
    en=rows[0]['name_en']
    iso=alias.get(en) or wbname.get(en) or ''
    rec=dict(bka_name=name,bka_code=r['bka_code'],name_en=en,iso3=iso,matched=1,
             pop_2025=pop,pop_2024=pop24,pop_mean=(pop+pop24)/2,
             male_18_39=m1839,share_m1839=round(m1839/pop,4) if pop else '')
    for m in MEAS:
        rec['n_'+m]=int(r[m])
        rec['rate_'+m]=round(int(r[m])/pop*1e5,1) if pop else ''
        rec['ratio_'+m]=round((int(r[m])/pop*1e5)/ger_rate[m],2) if pop else ''
    # Pueyo-style average of four ratios
    if pop:
        rec['pueyo_avg4_murderkey']=round(sum(rec['ratio_'+m] for m in ['violent','sexual','murder','total_all'])/4,2)
        rec['pueyo_avg4_homicide']=round(sum(rec['ratio_'+m] for m in ['violent','sexual','homicide_all','total_all'])/4,2)
        rec['pueyo_avg4_exclimm']=round(sum(rec['ratio_'+m] for m in ['violent','sexual','homicide_all','total_excl_imm'])/4,2)
    rec['gdp_pc_2023']=gdp_by_iso.get(iso,'')
    mm=mus.get(rows[0]['name_de']) or mus.get(name)
    rec['muslim_majority']=mm['muslim_majority'] if mm else 0
    out.append(rec)

out=[r for r in out if r.get('matched')==1 and r.get('pop_2025',0)>0]
out.sort(key=lambda r:-r['pueyo_avg4_murderkey'])
fields=list(out[0].keys())
with open(os.path.join(D,'de_nationality_rates.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)
print('German baseline rates per 100k:',{k:round(v,1) for k,v in ger_rate.items()})
print('rows written',len(out))
big=[r for r in out if r['pop_2025']>=10000]
print('n with >=10k residents',len(big))
print()
print(f"{'country':26s}{'pop':>9}{'avg4':>7}{'avg4_ex':>8}{'tot':>7}{'tot_ex':>7}{'viol':>7}{'sex':>7}{'murd':>7}")
for r in big[:25]:
    print(f"{r['bka_name'][:25]:26s}{r['pop_2025']:>9}{r['pueyo_avg4_murderkey']:>7}{r['pueyo_avg4_exclimm']:>8}{r['ratio_total_all']:>7}{r['ratio_total_excl_imm']:>7}{r['ratio_violent']:>7}{r['ratio_sexual']:>7}{r['ratio_murder']:>7}")
print('--- bottom 12 ---')
for r in big[-12:]:
    print(f"{r['bka_name'][:25]:26s}{r['pop_2025']:>9}{r['pueyo_avg4_murderkey']:>7}{r['pueyo_avg4_exclimm']:>8}{r['ratio_total_all']:>7}{r['ratio_total_excl_imm']:>7}{r['ratio_violent']:>7}{r['ratio_sexual']:>7}{r['ratio_murder']:>7}")
