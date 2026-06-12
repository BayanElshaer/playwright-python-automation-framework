"""
conftest.py – root-level fixtures shared across the entire test suite.

Fixtures provided
-----------------
browser_context_args   – viewport + slow_mo from config
page                   – overrides pytest-playwright's page with screenshot on fail
login_page             – LoginPage instance (lands on /)
authenticated_page     – Page already logged in as standard_user (lands on inventory)
inventory_page         – InventoryPage instance (logged in, on inventory)
cart_page              – CartPage instance (logged in, on cart)
"""
import logging
from typing import Generator

import allure
import pytest
from api.api_client import APIClient
from playwright.sync_api import Browser, BrowserContext, Page

from config.settings import (
    BROWSER,
    HEADLESS,
    SLOW_MO,
    STANDARD_USER,
    PASSWORD,
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
    VIDEOS_DIR,
)
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.logger import setup_logging

# Initialise logging once for the entire session
setup_logging()
logger = logging.getLogger(__name__)


# ── pytest-playwright browser config ──────────────────────────────────────────

def pytest_configure(config):
    """Register custom Allure environment info."""
    config.addinivalue_line("markers", "ui: UI/browser automation tests")


def pytest_collection_modifyitems(config, items):
    """Mark non-API tests as UI tests so browser-only hooks apply only where needed."""
    for item in items:
        if "api" not in item.keywords:
            item.add_marker(pytest.mark.ui)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"headless": HEADLESS, "slow_mo": SLOW_MO}


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        "ignore_https_errors": True,
        "record_video_dir": str(VIDEOS_DIR),
        "record_video_size": {"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
    }


# ── Screenshot on failure ──────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    """Attach a screenshot to Allure for UI test failures only."""
    yield

    if request.node.get_closest_marker("ui") is None:
        return

    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        page = request.getfixturevalue("page")
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name=f"FAILED – {request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )
        logger.warning("Test FAILED – screenshot captured: %s", request.node.name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ── Page Object fixtures ───────────────────────────────────────────────────────

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.open()
    logger.info("Fixture: login_page ready")
    return lp


@pytest.fixture
def authenticated_page(page: Page) -> Page:
    """Returns a Page that is already authenticated as standard_user."""
    lp = LoginPage(page)
    lp.login(STANDARD_USER, PASSWORD)
    logger.info("Fixture: authenticated_page – logged in as %s", STANDARD_USER)
    return page


@pytest.fixture
def inventory_page(authenticated_page: Page) -> InventoryPage:
    ip = InventoryPage(authenticated_page)
    ip.assert_on_inventory_page()
    logger.info("Fixture: inventory_page ready")
    return ip


@pytest.fixture
def cart_page(authenticated_page: Page) -> CartPage:
    cp = CartPage(authenticated_page)
    cp.open()
    cp.assert_on_cart_page()
    logger.info("Fixture: cart_page ready")
    return cp

@pytest.fixture(scope="session")
def api_base_url():
    return "https://dummyjson.com"

@pytest.fixture(scope="session")
def api_client(api_base_url) -> APIClient:
    client = APIClient(api_base_url)
    logger.info("Fixture: APIClient ready with base URL %s", api_base_url)
    return client
