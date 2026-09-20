from pathlib import Path
import xml.etree.ElementTree as ET
import json

ROOT=Path(__file__).resolve().parent
(ROOT/'derived').mkdir(exist_ok=True)
for year in (2018,2023):
 tree=ET.parse(ROOT/'_cache'/f'metadata{year}.xml')
 root=tree.getroot()
 for e in root.iter(): e.tag=e.tag.split('}')[-1]
 files={f.attrib.get('ID'):f.findtext('fileTxt/fileName') for f in root.iter('fileDscr')}
 selected=[]
 for v in root.iter('var'):
  file=(files.get(v.attrib.get('files'),'') or '').strip().split('.')[0]
  name=v.attrib.get('name','')
  if file.lower() not in ('tmigrante','tsdem'): continue
  categories=[{'value':(c.findtext('catValu') or '').strip(),'label':(c.findtext('labl') or '').strip()} for c in v.findall('catgry')]
  entry={'file':file,'name':name,'label':(v.findtext('labl') or '').strip(),'question':(v.findtext('qstn/qstnLit') or '').strip(),'categories':categories}
  selected.append(entry)
 if not selected: raise ValueError(f'No migration/resident fields parsed for {year}')
 print(f'{year}: {len(selected)} migration/resident field definitions')
 (ROOT/'derived'/f'field_mapping_{year}.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
