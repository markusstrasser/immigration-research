#!/bin/sh
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
lane=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
uv run --no-project python3 "$lane/adapter.py" --prepare
for subset in union latent; do
  uv run --no-project python3 "$lane/adapter.py" --policy health --group lineage --subset "$subset"
  uv run --no-project python3 "$lane/adapter.py" --policy snap --group lineage --subset "$subset"
done
uv run --no-project python3 "$lane/adapter.py" --tax lineage
for group in white black white_children black_children white_children_round3 black_children_round3 lineage_current lineage_children lineage_without_white_overlap lineage_without_black_overlap; do
  uv run --no-project python3 "$lane/adapter.py" --policy health --group "$group"
  uv run --no-project python3 "$lane/adapter.py" --policy snap --group "$group"
  uv run --no-project python3 "$lane/adapter.py" --tax "$group"
done
uv run --no-project python3 "$lane/finalize.py"
uv run --no-project python3 -m pytest -p no:cacheprovider "$lane/test_adapter.py" -q
