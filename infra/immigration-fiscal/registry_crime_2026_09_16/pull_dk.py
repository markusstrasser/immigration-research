import json, requests, pandas as pd, io
S=requests.Session(); S.headers.update({'User-Agent':'research-agent/1.0'}); P=print
YEARS=['2023','2024','2025']
def dst(body):
    r=S.post('https://api.statbank.dk/v1/data', json=body, timeout=180)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text), sep=';')
b_crime={"table":"STRAFNA9","format":"CSV","lang":"en","variables":[
  {"code":"KOEN","values":["M","K"]},
  {"code":"ALDER","values":["TOT","15-29","30-49","50-79"]},
  {"code":"HERKOMST","values":["TOT","1","21","24","25","31","34","35"]},
  {"code":"Tid","values":YEARS}]}
crime=dst(b_crime); crime.to_csv('dk_crime_raw.csv',index=False)
P("DK crime rows:",len(crime)); P(crime.head(3).to_string()); P("cols:",list(crime.columns))
ages=[str(a) for a in range(15,80)]
b_pop={"table":"FOLK1E","format":"CSV","lang":"en","variables":[
  {"code":"OMRÅDE","values":["000"]},
  {"code":"KØN","values":["1","2"]},
  {"code":"ALDER","values":ages},
  {"code":"HERKOMST","values":["TOT","1","24","25","34","35"]},
  {"code":"Tid","values":[y+"K1" for y in YEARS]}]}
pop=dst(b_pop); pop.to_csv('dk_pop_raw.csv',index=False)
P("DK pop rows:",len(pop)); P(pop.head(3).to_string()); P("cols:",list(pop.columns))
json.dump({'crime_body':b_crime,'pop_body':b_pop}, open('dk_bodies.json','w'))
