"""The message for a rejected import file is readable and styled from the palette (issue #14).

Run: PYTHONPATH=. ./.venv/bin/python -m pytest app/tests/test_import_error_block.py -q
"""
import re
from pathlib import Path

from app.handlers.data_import_handlers import import_error_block

THEME = Path(__file__).resolve().parents[2] / "config" / "ui" / "theme.css"


def test_message_and_hint_are_on_separate_lines():
    html = str(import_error_block("Validation Failed. Missing columns: ['x']. — Did you mean 'y'?"))
    assert "spv-import-error-message" in html and "Missing columns" in html
    assert "spv-import-error-hint" in html and "Did you mean" in html
    assert 'role="alert"' in html


def test_message_without_a_hint_has_no_hint_line():
    html = str(import_error_block("Could not read file: boom"))
    assert "spv-import-error-message" in html and "spv-import-error-hint" not in html


def test_style_uses_the_error_palette_and_the_secondary_text_size():
    css = THEME.read_text()
    block = re.search(r"\.spv-import-error \{([^}]*)\}", css).group(1)
    assert "font-size: 0.8rem" in block      # Secondary scale, rules_css_style_spec section 2
    assert "#ffe0e0" in block and "#d62828" in block   # error tint and error red, section 1e
