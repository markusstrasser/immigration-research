"""Regenerate the primary-source measurements; case evaluation runs separately.

uv run --no-project python3 infra/immigration-fiscal/spending_keys_r5_2026_10_15/build.py
"""
from pathlib import Path
import json
import resource
import time

from veterans import build_item as veterans
from income_security import build_item as administration
from college import build_item as college

HERE = Path(__file__).resolve().parent


def main():
    start = time.perf_counter()
    out = HERE / 'derived'
    out.mkdir(exist_ok=True)
    for number, builder in [(13, veterans), (14, administration), (15, college)]:
        item = builder()
        (out / f'item{number}.json').write_text(json.dumps(item, indent=2, sort_keys=True, allow_nan=False) + '\n')
        print(f'item {number}: {item["status"]}')
    usage = resource.getrusage(resource.RUSAGE_SELF)
    if usage.ru_maxrss > 2_500_000_000:
        raise ValueError('[BLOCKED] process exceeded 2.5GB physical-memory budget')
    print(json.dumps({'elapsed_seconds': time.perf_counter()-start, 'maxrss_bytes': usage.ru_maxrss}))


if __name__ == '__main__':
    main()
