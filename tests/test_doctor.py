from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE = Path(__file__).parents[1] / "scripts" / "doctor.py"
SPEC = importlib.util.spec_from_file_location("doctor", MODULE)
doctor = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(doctor)


def test_doctor_finds_every_release_script():
    result = doctor.collect_checks()
    assert all(item["ok"] for item in result["scripts"])
    assert {item["name"] for item in result["scripts"]} == set(doctor.REQUIRED_SCRIPTS)
    assert not any(item["required"] for item in result["modules"])


def test_proof_dependencies_are_only_required_on_request():
    result = doctor.collect_checks(require_proof=True)
    proof = {item["name"]: item for item in result["modules"]}
    assert proof["fitz"]["required"]
    assert proof["PIL"]["required"]


def test_optional_report_pipeline_check(tmp_path: Path):
    missing = doctor.collect_checks(report_pipeline=tmp_path)
    assert not missing["report_pipeline"]["ok"]
    expected = tmp_path / "pipeline" / "scripts"
    expected.mkdir(parents=True)
    (expected / "pipeline_ctl.py").write_text("# fixture", encoding="utf-8")
    present = doctor.collect_checks(report_pipeline=tmp_path)
    assert present["report_pipeline"]["ok"]
