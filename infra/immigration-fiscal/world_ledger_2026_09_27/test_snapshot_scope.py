"""A new case's simultaneous production cannot contaminate the oct15 receipt."""
import json
from pathlib import Path
import subprocess


def test_snapshot_tracks_selected_inputs_and_ignores_other_case(tmp_path):
    names = [f"generation_{kind}_oct15{cash}.{extension}"
             for kind, extension in (("corrections", "json"), ("results", "csv"), ("summary", "json"))
             for cash in ("", "_cash")]
    names += [f"model_{prefix}{generation}.json"
              for generation in ("G1", "G2", "G3plus") for prefix in ("", "b_")]
    for name in names:
        (tmp_path / name).write_text("selected input\n")
    other = tmp_path / "generation_corrections_oct16.json"
    other.write_text("new case in progress\n")
    script = """
const fs=require('fs'),crypto=require('crypto');
const api=require(process.argv[1]);
const files=api.generationOutputs(process.argv[2],'oct15');
console.log(JSON.stringify(files.map(p=>[p,crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')])));
"""
    command = ["node", "-e", script, str(Path(__file__).with_name("v8_snapshot.cjs")), str(tmp_path)]
    before = subprocess.run(command, capture_output=True, text=True, check=True).stdout
    other.write_text("different unfinished inputs\n")
    after = subprocess.run(command, capture_output=True, text=True, check=True).stdout
    assert before == after
    assert {Path(p).name for p, _ in json.loads(before)} == set(names)
    (tmp_path / names[0]).write_text("changed selected source\n")
    assert subprocess.run(command, capture_output=True, text=True, check=True).stdout != before
    (tmp_path / names[0]).unlink()
    missing = subprocess.run(command, capture_output=True, text=True)
    assert missing.returncode != 0
    assert "[BLOCKED] missing selected generation input" in missing.stderr
