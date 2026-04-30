"""conftest.py — shared pytest fixtures for SPARMVET_VIZ tests.

Provides:
  - `shiny_app`: ShinyAppProc fixture for Playwright-based UI tests
  - `page`: module-scoped Playwright Page (one browser session per test module)

`page` is intentionally module-scoped (not the default function-scope) so all
tests in a module share one Shiny WebSocket session. This prevents session
accumulation on resource-constrained machines where 10+ concurrent sessions
cause T1 materialization timeouts.
"""

from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from shiny.pytest import create_app_fixture

APP_PATH = Path(__file__).parent.parent / "src" / "main.py"

shiny_app = create_app_fixture(str(APP_PATH), scope="module")


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture(scope="module")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
