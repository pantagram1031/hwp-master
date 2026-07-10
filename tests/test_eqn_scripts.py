from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE = Path(__file__).parents[1] / "scripts" / "eqn.py"
SPEC = importlib.util.spec_from_file_location("eqn", MODULE)
eqn = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(eqn)


def test_bare_superscript_does_not_consume_following_expression():
    script, warnings = eqn.latex_to_hwpeqn(r"D(x^2)=D(x\cdot x)")
    assert script == "D(x^{2})=D(x cdot x)"
    assert warnings == []


def test_bare_subscripts_are_single_atoms():
    script, warnings = eqn.latex_to_hwpeqn(r"D_pD_q-D_qD_p")
    assert script == "D_{p}D_{q}-D_{q}D_{p}"
    assert warnings == []


def test_existing_group_and_command_atoms_remain_semantic():
    script, warnings = eqn.latex_to_hwpeqn(r"x^\infty+a_{k-1}")
    assert script == "x^{inf}+a_{k-1}"
    assert warnings == []
