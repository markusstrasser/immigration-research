"""List changed topic notes, research/decisions and lane documents in the window.

This is a discovery inventory, not an automated judgment that each file was
substantively new or independently verified. The memo's coverage table supplies
the human-readable dispositions.
"""
import csv
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = '0d6ae56150f70ca16c9e723d70250065af59a7b0'
END = 'beefbba'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode()

rows = []
changes = git('diff', '--name-status', BASE, END, '--', 'research', 'decisions', 'notes',
              'infra/immigration-fiscal').splitlines()
for line in changes:
    status, *paths = line.split('\t')
    path = paths[-1]
    top = path.startswith(('research/', 'decisions/')) and path.endswith('.md')
    note = path.startswith('notes/') and path.endswith('.md')
    lane = path.startswith('infra/immigration-fiscal/') and Path(path).name in ('RESULT.md', 'README.md')
    brief = path.startswith('infra/immigration-fiscal/') and Path(path).name == 'BRIEF.md'
    if not (top or note or lane or brief):
        continue
    rev = BASE if status == 'D' else END
    doc = git('show', f'{rev}:{path}')
    title = next((x.lstrip('# ') for x in doc.splitlines() if x.startswith('# ')), '')
    rows.append({'status': status, 'path': path, 'title': title,
                 'kind': ('research_or_decision' if top else 'note' if note
                          else 'lane_result' if lane else 'lane_brief'),
                 'opening': ' '.join(doc.split())[:1100]})
out = HERE / '_cache'
out.mkdir(parents=True, exist_ok=True)
with (out / 'weekly_inventory.tsv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
commits = git('log', '--format=%h %ad %s', '--date=iso-strict', f'{BASE}..{END}')
(out / 'commits.txt').write_text(commits)
for kind in ('research_or_decision', 'note', 'lane_result', 'lane_brief'):
    print(kind, sum(r['kind'] == kind for r in rows))
print('commits', len(commits.splitlines()))
