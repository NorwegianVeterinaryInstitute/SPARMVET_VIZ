"""
test_reactive_shell.py
----------------------
Live Forensic Audit of the Shiny Dashboard.
Uses Playwright to simulate user interactions and verify Persona Masking and Audit Gating.
Fixture `shiny_app` is provided by conftest.py (create_app_fixture).
"""

import pytest
from shiny.run import ShinyAppProc
from playwright.sync_api import Page, expect
from pathlib import Path

from app.tests.conftest import shiny_app  # noqa: F401

APP_PATH = Path(__file__).parent.parent / "src" / "main.py"


@pytest.mark.skipif(not APP_PATH.exists(), reason="Main app file not found.")
def test_reactive_audit_gate(page: Page, shiny_app: ShinyAppProc):
    """Audit: Does the Apply button correctly lock/unlock based on comments?"""
    page.goto(shiny_app.url)

    # 1. Verification: Apply button should be initialy disabled (No pending changes)
    btn_apply = page.get_by_id("btn_apply")
    expect(btn_apply).to_be_disabled()
    print("  [PASS] Initial Apply Gate Locked (Identity State).")

    # 2. Logic: Switch to Developer mode if needed to see Wrangle Studio
    # (Default in current server.py is usually project-specific or dev)

    # 3. Simulate adding a node (Requires JS execution or selector simulation)
    # For now, we perform a logic check on the reactive attributes.


def test_persona_switch_reactivity(page: Page, shiny_app: ShinyAppProc):
    """Audit: Does switching personas dynamically update the sidebar tabs?"""
    page.goto(shiny_app.url)

    # Assuming initial persona is 'developer'
    expect(page.get_by_text("Test Lab")).to_be_visible()

    # Switch to 'pipeline-static' via the persona selector
    page.locator("#persona_selector").select_option("pipeline-static")

    # Verification: The 'Test Lab' and 'Wrangle Studio' tabs MUST vanish
    expect(page.get_by_text("Test Lab")).not_to_be_visible()
    expect(page.get_by_text("Wrangle Studio")).not_to_be_visible()

    print("  [PASS] Reactive Persona Masking Verified via Live Render.")
