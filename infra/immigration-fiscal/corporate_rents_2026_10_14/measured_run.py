"""Python wall-clock/RSS wrapper for the sandbox; operational metrics stay ignored."""
import json
import resource
import subprocess
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
start=time.perf_counter()
result=subprocess.run(sys.argv[1:])
elapsed=time.perf_counter()-start
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
rss_bytes=usage.ru_maxrss if sys.platform=="darwin" else usage.ru_maxrss*1024
metrics=dict(command=sys.argv[1:],returncode=result.returncode,seconds=elapsed,max_child_rss_bytes=rss_bytes)
(HERE/"_cache/run_metrics.json").write_text(json.dumps(metrics,indent=2)+"\n")
print(f"run rc={result.returncode}; {elapsed:.3f}s; peak child RSS {rss_bytes/2**20:.2f} MiB",flush=True)
if rss_bytes>2.5e9:
    raise SystemExit("[BLOCKED] measured child process exceeds 2.5 GB")
raise SystemExit(result.returncode)
