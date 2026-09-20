"""Retain raw identifiers and timing fields; do not infer a fiscal calendar."""
from pathlib import Path
import hashlib,json,zipfile
import pandas as pd

ROOT=Path(__file__).parent / 'work'
archive=ROOT/'gfd-school-validated.zip'
manifest=json.loads((Path(__file__).parent/'SOURCES.json').read_text())
expected='33e3d7682c9c8d5642406fb4452233dc5ede70edbb0c66dcf0a91ce95f7d52eb'
if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected or manifest['sha256']!=expected:
    raise ValueError('Wrong GFD publisher snapshot')
fields=['SurveyYr','Year4','YearofData','ID','IDChanged','State_Code','Type_Code','County','Name',
        'FIPS_Code_State','FYEndDate','YearPop','SchLevCode','Enrollment','Total_Revenue',
        'Total_Rev_Own_Sources','Total_Taxes','Property_Tax','Total_IG_Revenue','Total_Fed_IG_Revenue',
        'Total_State_IG_Revenue','Tot_Local_IG_Rev','Total_Expenditure','Total_Current_Oper',
        'Total_Current_Expend','Total_Capital_Outlays','Total_Interest_on_Debt','Total_Debt_Outstanding']
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:
        raise ValueError('Damaged GFD ZIP member')
    with z.open('SchoolDistrictData.csv') as raw:
        chunks=[]
        for chunk in pd.read_csv(raw,usecols=fields,dtype=str,na_values=['.'],chunksize=30000,encoding='latin1'):
            years=pd.to_numeric(chunk.Year4,errors='coerce')
            chunks.append(chunk[years.between(1967,1992)].copy())
    for name in ['Appendix For The Government Finance Database.pdf','2006_classification_manual.pdf']:
        (ROOT/('gfd-appendix.pdf' if name.startswith('Appendix') else 'census-classification-2006.pdf')).write_bytes(z.read(name))
df=pd.concat(chunks,ignore_index=True)
if len(df)!=268798 or df.duplicated(['ID','Year4']).any():
    raise ValueError('Unexpected source coverage or duplicate school-years')
df.to_csv(ROOT/'schools-1967-1992-raw-selected.csv',index=False)
large=df[(df.Year4=='1980') & (pd.to_numeric(df.Enrollment,errors='coerce')>50000)]
large.to_csv(ROOT/'schools-1980-large-candidates.csv',index=False)
miami=df[(df.FIPS_Code_State.astype(str).str.zfill(2)=='12') & df.Name.str.contains('DADE',case=False,na=False)]
miami.to_csv(ROOT/'miami-raw-timing.csv',index=False)
summary={'rows':len(df),'units':df.ID.nunique(),'years':df.Year4.value_counts().sort_index().to_dict(),
         'large_1980':len(large),'large_names':large[['ID','Name','SchLevCode','Enrollment']].to_dict('records'),
         'timing_examples':df[['SurveyYr','Year4','YearofData','FYEndDate']].drop_duplicates().head(40).to_dict('records'),
         'miami_timing':miami[['ID','Name','SurveyYr','Year4','YearofData','FYEndDate','YearPop','Enrollment','Total_Expenditure']].to_dict('records'),
         'raw_duplicate_id_year4':int(df.duplicated(['ID','Year4']).sum())}
(ROOT/'panel-inspection.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Selected',len(df),'rows from',df.ID.nunique(),'units; metadata in panel-inspection.json')
