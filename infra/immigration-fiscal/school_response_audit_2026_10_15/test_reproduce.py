import hashlib

import pytest

import reproduce


def test_principal_input_copy_requires_exact_bytes(tmp_path, monkeypatch):
    data, case = tmp_path / "data", tmp_path / "case"
    data.mkdir()
    source = data / "model.json"
    payload = b'{"value": 7}\n'
    monkeypatch.setattr(reproduce, "BASE_INPUTS", {"model.json": hashlib.sha256(payload).hexdigest()})
    with pytest.raises(ValueError, match="missing frozen-case input"):
        reproduce.copy_principal_inputs(data, case)
    source.write_bytes(payload)
    reproduce.copy_principal_inputs(data, case)
    assert (case / "model.json").read_bytes() == payload
    source.write_bytes(b'{"value": 8}\n')
    with pytest.raises(ValueError, match="changed frozen-case input"):
        reproduce.copy_principal_inputs(data, case)
    assert (case / "model.json").read_bytes() == payload
