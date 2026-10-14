"""List every created path, including ignored diagnostics and the handoff.

Run: uv run --no-project python3 {lane}/final_paths.py
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
HANDOFF = Path("/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/p7/lanes/mortality-result.md")


def main():
    manifest = HERE / "changed-paths.txt"
    paths = {str(p) for p in HERE.rglob("*") if p.is_file()}
    paths.add(str(manifest))
    paths.add(str(HANDOFF))
    # Early default pytest runs wrote these shared ignored caches. Preserve peer
    # contents and list the exception; lane pytest.ini now disables the writer.
    paths.update(str(HERE.parents[2] / ".pytest_cache/v/cache" / n) for n in ("lastfailed", "nodeids"))
    manifest.write_text("\n".join(sorted(paths)) + "\n"
                        + "REMOVED AFTER REJECTED ACQUISITION: "
                        + str(HERE / "inputs/salmon_turra_elo_2008.html") + "\n"
                        + "".join("MOVED TO .py.txt ARCHIVE: " + str(HERE / "inputs/route_archive" / name) + "\n"
                                  for name in ("mortality_comparators.py", "accrual_white.py", "accrual_black.py")))
    print(f"[paths] {len(paths)} current changed paths plus one rejected acquisition removed")


if __name__ == "__main__":
    main()
