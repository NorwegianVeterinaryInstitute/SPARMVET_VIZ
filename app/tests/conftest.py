"""conftest.py — shared pytest fixtures for SPARMVET_VIZ tests.

Provides:
  - `shiny_app`: ShinyAppProc fixture for Playwright-based UI tests
  - `page`: Playwright Page fixture (from pytest-playwright)
"""

from pathlib import Path
import pytest
from shiny.pytest import create_app_fixture

APP_PATH = Path(__file__).parent.parent / "src" / "main.py"

# Module-scoped so the app process starts once per test module (fast).
# Change to scope="session" if you want one process for all tests in a run.
shiny_app = create_app_fixture(str(APP_PATH), scope="module")
