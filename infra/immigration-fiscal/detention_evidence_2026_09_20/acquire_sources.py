"""Acquire manifest-pinned bytes, optionally resolving held files explicitly."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import uuid
from source_contract import load_manifest,require,verify

def acquire(root,source_repo=None,offline=False):
    records=load_manifest(root)
    for record in records:
        if record.get('producer'):
            continue
        destination=root/record['local_file']
        if destination.exists():
            verify(destination,record)
            continue
        destination.parent.mkdir(parents=True,exist_ok=True)
        temp=destination.with_name(f'.{destination.name}.{uuid.uuid4().hex}.partial')
        held=source_repo/record['source_path'] if source_repo and record.get('source_path') else None
        if held and held.is_file():
            print(f'HELD {held} -> {destination}')
            shutil.copyfile(held,temp)
        else:
            require(not offline,f'Offline source unavailable: {record["file"]}; provide --source-repo or cached pinned bytes')
            require(record.get('url'),f'Missing public source URL: {record["file"]}')
            print(f'FETCH {record["url"]}')
            subprocess.run(['curl','--fail','--location','--silent','--show-error','--max-time','90',
                            '--output',str(temp),record['url']],check=True)
        verify(temp,record)
        os.link(temp,destination)  # Existing completed evidence is never replaced.
        temp.unlink()
    from parse_scaap import parse
    for record in records:
        if record.get('producer'):
            require(record['producer']=='parse_scaap.py','Unknown derived producer')
            destination=root/record['local_file']
            temp=destination.with_suffix('.partial')
            parse(root/'_cache/scaap_fy2024_awards.pdf',temp)
            verify(temp,record)
            temp.replace(destination)
    print(f'PASS: {len(records)} pinned inputs and derived records available')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--source-repo',type=Path,help='Explicit repository root for manifest source_path reuse')
    p.add_argument('--offline',action='store_true',help='Never fetch; fail if no held pinned copy exists')
    args=p.parse_args()
    acquire(args.root,args.source_repo,args.offline)
