"""October CPS public K–12 measurement and replicate estimates.

Positions are one-based inclusive from cpsoct24.pdf attachments 6–7. Schools
outside the edited regular-school question universe are not imputed as K–12.
"""
import hashlib
import json
from pathlib import Path
import re
import zipfile

import numpy as np
import pandas as pd

FIELDS = dict(GESTFIPS=(93,94), PRTAGE=(122,123), PRDTHSP=(141,142),
              PEHSPNON=(157,158), PRPERTYP=(161,162), PENATVTY=(163,165),
              PEMNTVTY=(166,168), PEFNTVTY=(169,171), PRCITSHP=(172,173),
              QSTNUM=(815,819), OCCURNUM=(820,821), PESSCHOL=(1001,1002),
              PEPUBLIC=(1003,1004), PRGRADE=(1005,1006), PESCH35=(1027,1028),
              PESCH614=(1029,1030), PECHPUB=(1031,1032), PECHGRDE=(1033,1034),
              PRENPUPR=(1039,1040), PWSUPWGT=(1081,1090))
AGE_BANDS = [('3_4',3,4), ('5_13',5,13), ('14_17',14,17), ('18_24',18,24), ('25_plus',25,99)]

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def fixed_records(path, width):
    with zipfile.ZipFile(path) as archive:
        members = [n for n in archive.namelist() if n.lower().endswith('.dat')]
        if len(members) != 1:
            raise ValueError(f'Expected one ASCII member: {members}')
        lines = archive.read(members[0]).splitlines()
    if not lines or any(len(row) != width for row in lines):
        raise ValueError(f'Wrong fixed-record width {path}: {sorted(set(map(len,lines)))}')
    return np.asarray(lines, dtype=f'S{width}')

def field(records, start, end):
    return np.ndarray((len(records),), dtype=f'S{end-start+1}', buffer=records,
                      offset=start-1, strides=(records.dtype.itemsize,)).astype(np.int64)

def origin_masks(d):
    native = d.PRCITSHP.isin([1,2,3])
    parents_us = d.PEFNTVTY.isin([57,60,66,69,73,78]) & d.PEMNTVTY.isin([57,60,66,69,73,78])
    parent_mex = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    canonical = ((d.PRCITSHP.isin([4,5]) & d.PENATVTY.eq(303)) |
                 (native & parent_mex) | (native & parents_us & d.PRDTHSP.eq(1)))
    broad = d.PRDTHSP.eq(1) | d.PENATVTY.eq(303) | parent_mex
    return dict(all=np.ones(len(d),bool), target=canonical.to_numpy(),
                rest=(~canonical).to_numpy(), broad_or=broad.to_numpy(),
                selfid_or_birth=(d.PRDTHSP.eq(1)|d.PENATVTY.eq(303)).to_numpy(),
                hispanic=d.PEHSPNON.eq(1).to_numpy())

def public_k12(d):
    child = (d.PRTAGE.between(3,14) & d.PRPERTYP.eq(1) &
             (d.PESCH35.eq(1)|d.PESCH614.eq(1)) & d.PECHPUB.eq(1) & d.PECHGRDE.between(3,16))
    older = (d.PRTAGE.ge(15) & d.PRPERTYP.eq(2) & d.PESSCHOL.eq(1) &
             d.PEPUBLIC.eq(1) & d.PRGRADE.between(7,12))
    if (child & older).any():
        raise ValueError('Question branches overlap')
    return (child|older).to_numpy()

def sdr(values):
    v=np.asarray(values,float)
    if v.shape[-1]!=161:
        raise ValueError('Expected full +160 CPS replicates')
    return np.sqrt(4/160*np.square(v[...,1:]-v[...,:1]).sum(axis=-1))

def missing_replicate_guard(joined):
    missing=joined.row.isna()
    nonperson=joined.PWSUPWGT.eq(0)&joined.PRPERTYP.eq(-1)&joined.PRTAGE.eq(-1)
    if (missing&~nonperson).any():
        raise ValueError('Actual supplement person without replicate weights')
    return ~missing

def load_october(cache, lock):
    for source in json.loads(Path(lock).read_text())['files']:
        if sha(Path(cache)/source['file']) != source['sha256']:
            raise ValueError(f"Source checksum changed: {source['file']}")
    raw=fixed_records(Path(cache)/'oct24pub.zip',1090)
    if len(raw)!=126387:
        raise ValueError('October row count differs from source abstract')
    d=pd.DataFrame({name:field(raw,*span) for name,span in FIELDS.items()})
    rep=fixed_records(Path(cache)/'oct24rep.zip',1617)
    keys=pd.DataFrame(dict(QSTNUM=field(rep,1,5),OCCURNUM=field(rep,6,7),row=np.arange(len(rep))))
    if keys.duplicated(['QSTNUM','OCCURNUM']).any() or d.duplicated(['QSTNUM','OCCURNUM']).any():
        raise ValueError('Duplicate monthly person key')
    weights=np.ndarray((len(rep),161),dtype='S10',buffer=rep,offset=7,
                       strides=(1617,10)).astype(float)/10000
    documented={int(k):float(v) for k,v in re.findall(r'repwgt(\d+)\s*=\s*([\d.]+)',(Path(cache)/'cps_school_repwgt_oct24.sas').read_text())}
    if set(documented)!=set(range(161)):
        raise ValueError('Missing official weight control')
    controls=np.array([documented[i] for i in range(161)])
    residual=float(np.abs(weights.sum(axis=0)-controls).max())
    if residual>.005:
        raise ValueError(f'Official 161 weight totals failed: {residual}')
    joined=d.merge(keys,on=['QSTNUM','OCCURNUM'],how='left',validate='one_to_one')
    keep=missing_replicate_guard(joined)
    raw_count=len(d)
    d=d[keep].reset_index(drop=True)
    joined=joined[keep]
    weights=weights[joined.row.to_numpy(int)]
    if not np.allclose(weights[:,0],d.PWSUPWGT/10000,rtol=0,atol=.00011):
        raise ValueError('PWSUPWGT and replicate0 mismatch')
    valid=d.PRPERTYP.isin([1,2]).to_numpy() & (weights[:,0]>0)
    # The combined public/private recode is an independent published field.
    enrolled_public=((d.PESSCHOL.eq(1)&d.PEPUBLIC.eq(1))|
                     ((d.PESCH35.eq(1)|d.PESCH614.eq(1))&d.PECHPUB.eq(1)))
    if not np.array_equal(enrolled_public[valid],d.loc[valid,'PRENPUPR'].eq(2)):
        raise ValueError('Branch construction disagrees with published combined enrollment recode')
    audit=dict(raw_records=raw_count,zero_weight_nonperson_records_excluded=int((~keep).sum()),replicate_records=len(rep),valid_records=int(valid.sum()),
               official_weight_sum=controls[0],max_official_161_weight_residual=residual)
    return d[valid].reset_index(drop=True),weights[valid],audit

def cells(d, pooled=False):
    """Pool rare 3–4/25+ cells across origin; other cells retain target/rest."""
    origin=origin_masks(d)['target']
    result=np.full(len(d),'out',object)
    for label,low,high in AGE_BANDS:
        age=d.PRTAGE.between(low,high).to_numpy()
        if pooled or label in {'3_4','25_plus'}:
            result[age]=label+':all'
        else:
            result[age & origin]=label+':target'
            result[age & ~origin]=label+':rest'
    return result

def fit_rates(d,w,pooled=False,fit_mask=None):
    codes=cells(d,pooled)
    pupil=public_k12(d)
    fit=np.ones(len(d),bool) if fit_mask is None else fit_mask
    values,rows={},[]
    for code in sorted(set(codes)-{'out'}):
        use=(codes==code)&fit
        den=w[use].sum(axis=0)
        num=w[use&pupil].sum(axis=0)
        neff=float(den[0]**2/np.square(w[use,0]).sum())
        if use.sum()<50 or neff<50 or (den<=0).any():
            raise ValueError(f'Unsupported predeclared cell {code}: n={use.sum()}, neff={neff}')
        rates=num/den
        values[code]=rates
        rows.append(dict(cell=code,n=int(use.sum()),n_public=int((use&pupil).sum()),kish_neff=neff,
                         population=den[0],pupils=num[0],rate=rates[0],se=float(sdr(rates))))
    values['out']=np.zeros(161)
    return values,rows
