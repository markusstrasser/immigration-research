"""rerun_lane.py flags new or modified lane scripts that no rerun command runs.

On 2026-09-28 the parent committed the PISA lane (3589a4f) while its worker was still running: the
rerun covered the listed scripts and came back identical, and the commit also took a half-written
arrival_microdata.py that no command ran. Each test copies rerun_lane.py into a throwaway repository.

    uv run --no-project --with pytest python3 -m pytest scripts/test_rerun_lane.py -q
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "rerun_lane.py"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                   check=True, capture_output=True)


def lane_repo(tmp: Path) -> Path:
    (tmp / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp / "scripts" / "rerun_lane.py")
    lane = tmp / "lane"
    (lane / "derived").mkdir(parents=True)
    (lane / "build.py").write_text("open('lane/derived/out.txt', 'w').write('1\\n')\n")
    (lane / "derived" / "out.txt").write_text("1\n")
    git(tmp, "init", "-q")
    git(tmp, "add", ".")
    git(tmp, "commit", "-q", "-m", "init")
    return tmp


def rerun(repo: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "scripts/rerun_lane.py", "lane", f"{sys.executable} {{lane}}/build.py",
                           *extra], cwd=repo, capture_output=True, text=True)


def test_clean_lane_passes(tmp_path: Path) -> None:
    r = rerun(lane_repo(tmp_path))
    assert r.returncode == 0, r.stdout
    assert "IDENTICAL" in r.stdout and "NOT RUN" not in r.stdout


def test_untracked_script_no_command_runs_is_flagged(tmp_path: Path) -> None:
    repo = lane_repo(tmp_path)
    (repo / "lane" / "helper.py").write_text("x = 1\n")
    r = rerun(repo)
    assert r.returncode == 3, r.stdout
    assert "NOT RUN lane/helper.py" in r.stdout


def test_modified_tracked_script_is_flagged_and_can_be_allowed(tmp_path: Path) -> None:
    repo = lane_repo(tmp_path)
    (repo / "lane" / "fetch.py").write_text("x = 1\n")
    git(repo, "add", "lane/fetch.py")
    git(repo, "commit", "-q", "-m", "fetch")
    (repo / "lane" / "fetch.py").write_text("x = 2\n")
    assert rerun(repo).returncode == 3
    assert rerun(repo, "--allow-unrun", "lane/fetch.py").returncode == 0


def test_cache_files_are_ignored(tmp_path: Path) -> None:
    repo = lane_repo(tmp_path)
    (repo / "lane" / "_cache").mkdir()
    (repo / "lane" / "_cache" / "raw.py").write_text("x = 1\n")
    assert rerun(repo).returncode == 0


def test_changed_output_outside_derived_is_caught(tmp_path: Path) -> None:
    # The 2026-09-28 school lane also wrote credentials/derived/ and design_table/*.csv.
    repo = lane_repo(tmp_path)
    (repo / "lane" / "sub" / "derived").mkdir(parents=True)
    (repo / "lane" / "sub" / "derived" / "table.csv").write_text("a\n")
    (repo / "lane" / "build.py").write_text("open('lane/derived/out.txt', 'w').write('1\\n')\n"
                                            "open('lane/sub/derived/table.csv', 'w').write('b\\n')\n")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "nested output")
    r = rerun(repo)
    assert r.returncode == 1, r.stdout
    assert "CHANGED lane/sub/derived/table.csv" in r.stdout


def test_new_committable_output_is_listed(tmp_path: Path) -> None:
    repo = lane_repo(tmp_path)
    (repo / "lane" / "build.py").write_text("open('lane/derived/out.txt', 'w').write('1\\n')\n"
                                            "open('lane/extra.csv', 'w').write('x\\n')\n")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "extra output")
    r = rerun(repo)
    assert r.returncode == 1, r.stdout
    assert "NEW lane/extra.csv" in r.stdout
