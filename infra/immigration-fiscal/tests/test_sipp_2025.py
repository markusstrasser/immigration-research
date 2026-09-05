"""Annual benefit units, survey covariance and both official ZIP vintages."""
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'build'))
from public_mvp_io import SIPP_PERSON_MONTH_COLS, iter_sipp_allocated_sample_units
from analyze_sipp_2025 import analyze, annual_person, domain_names, estimate_domain, fay_se, read_replicate_weights


class Sipp2025Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.schema=self.root/'schema.json'
        self.schema.write_text(json.dumps([{'name':n} for n in SIPP_PERSON_MONTH_COLS]))

    def record(self,pnum,month,**changes):
        row=dict.fromkeys(SIPP_PERSON_MONTH_COLS,'')
        row.update(SSUID='001',PNUM=str(pnum),MONTHCODE=str(month),RIN_UNIV='1',
                   WPFINWGT='100',TAGE_EHC='30',EBORNUS='1',EEDUC='39',
                   TPEARN='0',TPTOTINC='0',RSNAP_MNYN='2',RTANF_MNYN='2',RSSI_MNYN='2')
        row.update({k:str(v) for k,v in changes.items()})
        return row

    def archive(self,names,rows=()):
        path=self.root/'data.zip'
        buffer=io.StringIO()
        writer=csv.writer(buffer,delimiter='|')
        writer.writerow(SIPP_PERSON_MONTH_COLS)
        for row in rows:
            writer.writerow([row[n] for n in SIPP_PERSON_MONTH_COLS])
        with zipfile.ZipFile(path,'w') as z:
            for name in names:
                z.writestr(name,buffer.getvalue())
        return path

    def test_unique_official_member_supports_2024_and_2025(self):
        for year in (2024,2025):
            with self.subTest(year=year):
                archive=self.archive([f'pu{year}.csv'],[self.record(101,12,WPFINWGT=2)])
                data=list(iter_sipp_allocated_sample_units(self.schema,archive))
                self.assertEqual(data[0][0].weight,2)
        for names in (['other.csv'],['pu2024.csv','pu2025.csv'],['pu25.csv']):
            with self.subTest(names=names),self.assertRaisesRegex(ValueError,'Expected one puYYYY'):
                list(iter_sipp_allocated_sample_units(self.schema,self.archive(names)))

    def test_child_allocation_december_weight_and_negative_earnings(self):
        rows=[]
        for month in range(1,13):
            rows.extend([
                self.record(101,month,WPFINWGT=1 if month==12 else 100,
                            RSNAP_MNYN=1,ESNAP_OWN=101,ESNAP_CNT=3,TSNAP_AMT=300,
                            ETANF_OWN=101,TTANF_AMT=600),
                self.record(102,month,WPFINWGT=3 if month==12 else 200,EBORNUS=2,TYRENTRY=2025,
                            TPEARN=-100,TPTOTINC=-100,RSNAP_MNYN=1,ESNAP_OWN=101),
                self.record(103,month,TAGE_EHC=8,EEDUC='',TPTOTINC=50,
                            RSNAP_MNYN=1,ESNAP_OWN=101,RTANF_MNYN=1,ETANF_OWN=101,
                            RSSI_MNYN=1,TSSI_AMT=50),
            ])
        sample=list(iter_sipp_allocated_sample_units(self.schema,self.archive(['pu2025.csv'],rows)))[0]
        native=annual_person([r for r in sample if r.person_number==101])
        foreign=annual_person([r for r in sample if r.person_number==102])
        self.assertIsNone(annual_person([r for r in sample if r.person_number==103]))
        self.assertEqual((native['weight'],foreign['weight']),(1,3))
        self.assertEqual(native['three_benefits_usd'],1200)
        self.assertEqual(foreign['three_benefits_usd'],1200)
        self.assertEqual(sum(r.allocated_tanf for r in sample if r.person_number==103),7200)
        self.assertEqual(foreign['person_earnings_usd'],-1200)
        self.assertEqual(native['zero_annual_earnings'],1)
        self.assertEqual(foreign['negative_annual_earnings'],1)
        self.assertIn('foreign_born_entry_2022_25_code',domain_names(foreign))

    def test_partial_exposure_is_summed_not_annualized_and_bad_code_fails(self):
        rows=[self.record(101,m,EBORNUS=2,TYRENTRY=2025,TPEARN=100,TPTOTINC=100) for m in range(7,13)]
        sample=list(iter_sipp_allocated_sample_units(self.schema,self.archive(['pu2025.csv'],rows)))[0]
        person=annual_person(sample)
        self.assertEqual(person['person_earnings_usd'],600)
        self.assertEqual(person['in_frame_months'],6)
        self.assertEqual(person['partial_frame_year'],1)
        self.assertNotIn('foreign_born_full_frame_year',domain_names(person))
        sample[-1].entry_year=2024
        with self.assertRaisesRegex(ValueError,'TYRENTRY'):
            annual_person(sample)

    def test_fay_ratio_and_covariance_have_independent_expected_values(self):
        reps=np.tile(np.array([[.5,1.5],[1.5,.5]]),(1,120))
        estimates=estimate_domain(np.array([[0.],[10.]]),np.array([1.,1.]),reps)
        self.assertEqual(estimates['point'][0],5)
        self.assertEqual(estimates['se'][0],5)
        identical_gap=fay_se(0,estimates['replicates'][:,0]-estimates['replicates'][:,0])
        self.assertEqual(identical_gap,0)
        self.assertEqual(fay_se(4,np.tile([3.,5.],120)),2)

    def test_missing_replicate_person_and_wrong_full_weight_fail(self):
        names=['SSUID','PNUM','SPANEL','SWAVE','MONTHCODE','REPWGT0']+[f'REPWGT{i}' for i in range(1,241)]
        schema=self.root/'rw_schema.json'
        schema.write_text(json.dumps([{'name':n} for n in names]))
        archive=self.root/'rw.zip'
        def write(pnum,weight):
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('rw2025.csv','|'.join(names).lower()+'\n'+'|'.join(['001',str(pnum),'2024','2','12',str(weight)]+['2']*240)+'\n')
        people=[dict(sample_id='001',person_number=101,weight=2)]
        write(101,2)
        reps,audit=read_replicate_weights(schema,archive,people)
        self.assertEqual(reps.shape,(1,240))
        self.assertEqual(audit['matched_selected_adults'],1)
        write(102,2)
        with self.assertRaisesRegex(ValueError,'Missing or invalid'):
            read_replicate_weights(schema,archive,people)
        write(101,3)
        with self.assertRaisesRegex(ValueError,'REPWGT0 disagrees'):
            read_replicate_weights(schema,archive,people)

    def test_zero_sample_event_warning_survives_contrast_output(self):
        rows=[self.record(101,m,WPFINWGT=2,RSSI_MNYN=1,TSSI_AMT=100) for m in range(1,13)]
        rows += [self.record(102,m,WPFINWGT=2,EBORNUS=2,TYRENTRY=2025) for m in range(1,13)]
        archive=self.archive(['pu2025.csv'],rows)
        names=['SSUID','PNUM','SPANEL','SWAVE','MONTHCODE','REPWGT0']+[f'REPWGT{i}' for i in range(1,241)]
        schema=self.root/'rw_schema.json'
        schema.write_text(json.dumps([{'name':n} for n in names]))
        replicate_zip=self.root/'rw.zip'
        with zipfile.ZipFile(replicate_zip,'w') as z:
            body='|'.join(names).lower()+'\n'
            for pnum in (101,102):
                body+='|'.join(['001',str(pnum),'2024','2','12','2']+['2']*240)+'\n'
            z.writestr('rw2025.csv',body)
        out=self.root/'output'
        analyze(self.schema,archive,schema,replicate_zip,out)
        with (out/'benefit_contrasts_2024.csv').open() as handle:
            contrast=next(r for r in csv.DictReader(handle) if r['left']=='foreign_born' and r['metric']=='three_benefits_usd')
        self.assertEqual(float(contrast['difference']),-1200)
        self.assertEqual(contrast['zero_observation_warning'],'True')


if __name__=='__main__':
    unittest.main()
