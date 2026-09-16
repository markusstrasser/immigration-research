import csv, os, json
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=[r for r in csv.DictReader(open(os.path.join(D,'de_nationality_rates.csv'))) if int(r['pop_2025'])>=10000]
PUEYO={'Algerien':25.5,'Gambia':12.3,'Tunesien':12.0,'Guinea':11.6,'Libyen':11.1,'Georgien':10.3,
 'Sudan (ohne Südsudan)':9.4,'Somalia':8.6,'Moldau':8.0,'Libanon':7.4,'Jemen':7.3,'Marokko':7.2,
 'Afghanistan':7.1,'Syrien':6.8,'Irak':6.4,'Albanien':5.1,'Eritrea':4.9,'Jordanien':4.9,
 'Kolumbien':4.4,'Nigeria':4.2}
EN={'Algerien':'Algeria','Gambia':'Gambia','Tunesien':'Tunisia','Guinea':'Guinea','Libyen':'Libya',
 'Georgien':'Georgia','Sudan (ohne Südsudan)':'Sudan','Somalia':'Somalia','Moldau':'Moldova',
 'Libanon':'Lebanon','Jemen':'Yemen','Marokko':'Morocco','Afghanistan':'Afghanistan','Syrien':'Syria',
 'Irak':'Iraq','Albanien':'Albania','Eritrea':'Eritrea','Jordanien':'Jordan','Kolumbien':'Colombia',
 'Nigeria':'Nigeria','Thailand':'Thailand','Luxemburg':'Luxembourg','Mexiko':'Mexico',
 'Australien':'Australia','Philippinen':'Philippines','Korea, Republik':'South Korea',
 'Indonesien':'Indonesia','Taiwan':'Taiwan','Finnland':'Finland','Japan':'Japan','Kanada':'Canada',
 'Österreich':'Austria'}
for r in rows:
    r['h']=float(r['pueyo_avg4_homicide']); r['hx']=float(r['pueyo_avg4_exclimm'])
by_h=sorted(rows,key=lambda r:-r['h']); by_hx=sorted(rows,key=lambda r:-r['hx'])
rank_h={r['bka_name']:i+1 for i,r in enumerate(by_h)}
rank_hx={r['bka_name']:i+1 for i,r in enumerate(by_hx)}

lines=[]
lines.append('| # | Country | Residents 31.12.2025 | Pueyo chart | Repro avg4 | Repro avg4 excl. imm. offences | Rank excl. | Total ratio incl. | Total ratio excl. | Δ total |')
lines.append('|---|---|---|---|---|---|---|---|---|---|')
for i,r in enumerate(by_h[:20],1):
    n=r['bka_name']; p=PUEYO.get(n,'')
    ti=float(r['ratio_total_all']); te=float(r['ratio_total_excl_imm'])
    lines.append(f"| {i} | {EN.get(n,n)} | {int(r['pop_2025']):,} | {p if p else '—'} | {r['h']:.1f} | {r['hx']:.1f} | {rank_hx[n]} | {ti:.1f} | {te:.1f} | {100*(te/ti-1):+.0f}% |")
lines.append('')
lines.append('| Bottom 10 | Country | Residents | Repro avg4 | Repro avg4 excl. |')
lines.append('|---|---|---|---|---|')
for i,r in enumerate(by_h[-10:],len(by_h)-9):
    n=r['bka_name']
    lines.append(f"| {i} | {EN.get(n,n)} | {int(r['pop_2025']):,} | {r['h']:.2f} | {r['hx']:.2f} |")
open(os.path.join(D,'build','tables.md'),'w').write('\n'.join(lines))
print('\n'.join(lines))
print()
# aggregate denominator arithmetic
t61={r['offence']:r for r in csv.DictReader(open(os.path.join(D,'t61_residence_status_2025.csv')))}
AZR=14070230; GER=71036222
for key in ['total_all','total_excl_imm','violent','sexual']:
    r=t61[key]; nd=int(r['nd_anzahl']); out=int(r['unerlaubt'])+int(r['kein_aufenthalt'])
    ger_n={'total_all':1231246,'total_excl_imm':1230432,'violent':109674,'sexual':70704}[key]
    gr=ger_n/GER*1e5
    print(f"{key:16s} nd={nd:>7} not_in_AZR={out:>7} ({out/nd:5.1%})  ratio_raw={nd/AZR*1e5/gr:5.2f}  ratio_adj={(nd-out)/AZR*1e5/gr:5.2f}  drop={100*((nd-out)/nd-1):+.1f}%")
