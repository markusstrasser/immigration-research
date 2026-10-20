"""Pin adopted oct16 case and matched decomposition, without changing history."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
FISCAL=HERE.parent


def main():
    case=FISCAL/'main_case_2026_10_16/derived/summary.json'
    summary=json.loads(case.read_text())
    records={'case_key':'oct16','bands':{},'excess':{},'source_hashes':{}}
    for basis,suffix in [('main',''),('cash','_cash')]:
        path=FISCAL/f'main_case_decomposition_2026_09_29/derived/summary_oct16{suffix}.json'
        d=json.loads(path.read_text())
        if d['case']['key']!='oct16'+suffix:
            raise ValueError('[BLOCKED] oct16 pin got another decomposition case')
        band=summary['main_case'] if basis=='main' else summary['cash_set']['band_bn']
        records['bands'][basis]=band
        records['excess'][basis]=[]
        for i,end in enumerate(('low','high')):
            parts=d['parts'][end]
            if abs(parts['shared']+sum(parts['shapley'].values())-band[i])>1e-9:
                raise ValueError('[BLOCKED] matched decomposition does not close to oct16')
            records['excess'][basis].append(band[i]-parts['shared'])
        records['source_hashes'][str(path.relative_to(FISCAL))]=hashlib.sha256(path.read_bytes()).hexdigest()
    records['source_hashes'][str(case.relative_to(FISCAL))]=hashlib.sha256(case.read_bytes()).hexdigest()
    (HERE/'inputs').mkdir(exist_ok=True)
    (HERE/'inputs/pins_oct16.json').write_text(json.dumps(records,indent=1)+'\n')
    print('oct16 case and matched set/cash decomposition pinned at 1e-9')


if __name__=='__main__':
    main()
