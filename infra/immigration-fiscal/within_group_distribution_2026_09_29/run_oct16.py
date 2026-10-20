"""Run only the live oct16 household consumers; retain every historical output.

Native-First: ordered subprocess calls with Python timing and exact child exits.
"""
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from oct16_households import require_adopted


def main():
    require_adopted('oct16')
    cache=HERE/'_cache/oct16'
    cache.mkdir(parents=True,exist_ok=True)
    python=['uv','run','--no-project','python3']
    commands=[['node',str(HERE/'export_lines.cjs'),'--case','oct16'],
              ['node',str(HERE/'export_lines.cjs'),'--case','oct16','--allocation','shared']]
    for allocation in ('personal','shared'):
        for basis in ('set','cash'):
            for extra in ([],['--accrual','person'],['--accrual','person','--payroll','onbooks']):
                commands.append(python+[str(HERE/'oct16_households.py'),'--allocation',allocation,'--basis',basis]+extra)
    commands += [python+[str(HERE/'oct16_households.py'),'--basis',basis,'--placement','uniform'] for basis in ('set','cash')]
    items=['none','veterans_compensation','income_security_administration','public_college_response',
           'native_minor_calibration','coverage_tenure','consumption_tax_bases','one_rate','health_residual_key']
    for allocation in ('personal','shared'):
        for item in items:
            commands.append(['node',str(HERE/'export_controls_oct16.cjs'),'--allocation',allocation,'--control-item',item])
            for basis in ('set','cash'):
                commands.append(python+[str(HERE/'oct16_households.py'),'--allocation',allocation,'--basis',basis,'--control-item',item])
    commands += [python+[str(HERE/'oct16_full_controls.py')]]
    commands += [python+[str(HERE/'oct16_claims.py')]]
    commands += [['node',str(HERE/'test_export_oct16.cjs')],python+['-m','pytest',
        str(HERE/'test_oct16_households.py'),str(HERE/'test_oct15_contract.py'),
        str(HERE/'test_oct16_outputs.py'),
        str(HERE/'test_person_accrual.py'),str(HERE/'test_reporter_b_routes.py'),
        str(HERE/'test_completion_publication.py'),'-q','-p','no:cacheprovider']]
    timings=[]
    for index,command in enumerate(commands):
        started=time.perf_counter()
        log=cache/f'command-{index:02d}.log'
        with log.open('w') as stream:
            result=subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,
                env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
        row=dict(command=command,returncode=result.returncode,elapsed_seconds=time.perf_counter()-started,
                 diagnostic_child_maxrss=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,log=str(log))
        timings.append(row)
        print(json.dumps(row),flush=True)
        if result.returncode:
            print('\n'.join(log.read_text().splitlines()[-60:]),flush=True)
            (cache/'timings.json').write_text(json.dumps(timings,indent=2)+'\n')
            raise SystemExit(result.returncode)
    (cache/'timings.json').write_text(json.dumps(timings,indent=2)+'\n')


if __name__=='__main__':
    main()
