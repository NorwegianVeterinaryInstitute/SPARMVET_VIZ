"""Renders are read-only (ADR-045, reactive write rule R1, ui_implementation_contract.md section 14).

A @render.* function must not call reactive.Value.set(). Writing state during a render makes Shiny
report 'output ... is in an unexpected state' and the widget snaps back. The one allowed pattern is
a write inside a callback the render hands to session.on_flushed(): it runs after the render, so
the callback is a nested function and is not counted here.

Found by the ADR behavioural audit of 2026-11-06 (wrangle_studio.architect_active_plot).

Run: PYTHONPATH=. ./.venv/bin/python -m pytest app/tests/test_render_purity.py -q
"""
import ast
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parents[1]


def _is_render(fn) -> bool:
    return any(ast.unparse(d).startswith("render.") or ".render." in ast.unparse(d) for d in fn.decorator_list)


def _own_calls(fn):
    """Calls in the body of fn, not inside nested functions (those run later)."""
    stack = list(fn.body)
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        if isinstance(node, ast.Call):
            yield node
        stack.extend(ast.iter_child_nodes(node))


def render_writes(source: str) -> list[str]:
    hits = []
    for fn in ast.walk(ast.parse(source)):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_render(fn):
            for call in _own_calls(fn):
                if isinstance(call.func, ast.Attribute) and call.func.attr == "set":
                    hits.append(f"{fn.name} line {call.lineno}: {ast.unparse(call)[:80]}")
    return hits


def test_the_scanner_finds_a_write_in_a_render():
    src = "@render.plot\ndef p():\n    err.set('x')\n    return 1\n"
    assert len(render_writes(src)) == 1


def test_a_write_in_a_deferred_callback_is_allowed():
    src = ("@render.plot\ndef p():\n    def later():\n        err.set('x')\n"
           "    session.on_flushed(later, once=True)\n")
    assert render_writes(src) == []


def test_a_write_in_an_effect_is_not_a_render():
    src = "@reactive.Effect\ndef e():\n    err.set('x')\n"
    assert render_writes(src) == []


@pytest.mark.parametrize("path", sorted(p for p in APP.rglob("*.py") if "tests" not in p.parts),
                         ids=lambda p: str(p.relative_to(APP)))
def test_no_render_in_app_writes_a_reactive_value(path):
    assert render_writes(path.read_text()) == []
