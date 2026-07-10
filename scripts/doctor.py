#!/usr/bin/env python3
"""Check whether a fresh machine can run hwp-master's portable and COM paths."""
from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SCRIPTS = (
    "build_report.py", "charpr_check.py", "contact_sheet.py", "eqn.py",
    "fill_report.py", "form_inspect.py", "layout_plan_check.py",
    "layout_qa.py", "style_diff.py", "tidy_hwpx.py",
)


def _module_check(name: str, required: bool) -> dict:
    available = importlib.util.find_spec(name) is not None
    return {"name": name, "ok": available or not required, "available": available, "required": required}


def _hancom_check() -> dict:
    """Detect a locally installed Hancom HWP COM server without launching it."""
    if sys.platform != "win32":
        return {"ok": False, "installed": False, "required": False, "detail": "Windows only"}
    try:
        import winreg

        for prog_id in ("HWPFrame.HwpObject", "HWPFrame.HwpObject.2"):
            try:
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, prog_id):
                    return {"ok": True, "installed": True, "required": False, "detail": prog_id}
            except FileNotFoundError:
                continue
    except OSError as exc:
        return {"ok": False, "installed": False, "required": False, "detail": str(exc)}
    return {"ok": False, "installed": False, "required": False, "detail": "HWP COM registration not found"}


def collect_checks(require_com: bool = False, require_proof: bool = False, report_pipeline: Path | None = None) -> dict:
    scripts = []
    for name in REQUIRED_SCRIPTS:
        path = ROOT / "scripts" / name
        scripts.append({"name": name, "ok": path.is_file(), "path": str(path)})

    windows = sys.platform == "win32"
    modules = [
        _module_check("fitz", require_proof),
        _module_check("PIL", require_proof),
        _module_check("pyhwpx", require_com),
        _module_check("win32com", require_com),
    ]
    hancom = _hancom_check()
    hancom["required"] = require_com
    hancom["ok"] = hancom["installed"] or not require_com
    pipeline_check = None
    if report_pipeline is not None:
        expected = report_pipeline.resolve() / "pipeline" / "scripts" / "pipeline_ctl.py"
        pipeline_check = {"ok": expected.is_file(), "path": str(expected)}

    python_ok = sys.version_info >= (3, 10)
    com_ready = windows and all(item["available"] for item in modules if item["name"] in {"pyhwpx", "win32com"})
    checks_ok = python_ok and all(item["ok"] for item in scripts + modules)
    if pipeline_check is not None:
        checks_ok = checks_ok and pipeline_check["ok"]
    if require_com:
        checks_ok = checks_ok and com_ready and hancom["installed"]

    return {
        "ok": checks_ok,
        "python": {"ok": python_ok, "version": platform.python_version()},
        "platform": {"system": platform.system(), "win32": windows},
        "scripts": scripts,
        "modules": modules,
        "hancom_hwp": hancom,
        "com_ready": com_ready,
        "report_pipeline": pipeline_check,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-com", action="store_true", help="fail unless Windows COM dependencies are installed")
    parser.add_argument("--require-proof", action="store_true", help="fail unless optional PDF proof dependencies are installed")
    parser.add_argument("--report-pipeline", type=Path, help="also verify a report-pipeline checkout")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = collect_checks(args.require_com, args.require_proof, args.report_pipeline)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"hwp-master doctor: {'PASS' if result['ok'] else 'FAIL'}")
        print(f"Python {result['python']['version']}: {'ok' if result['python']['ok'] else '3.10+ required'}")
        print(f"Platform: {result['platform']['system']} (COM ready: {result['com_ready']})")
        hancom = result["hancom_hwp"]
        print(f"Hancom HWP: {'installed' if hancom['installed'] else 'not detected'} ({hancom['detail']})")
        for item in result["modules"]:
            state = "ok" if item["available"] else "missing"
            suffix = " (required)" if item["required"] else " (optional)"
            print(f"- {item['name']}: {state}{suffix}")
        if result["report_pipeline"] is not None:
            print(f"- report-pipeline: {'ok' if result['report_pipeline']['ok'] else 'missing'}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
