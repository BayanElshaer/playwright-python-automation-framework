"""
BasePage – shared browser interactions for all Page Objects.
All page classes inherit from this to get uniform wait/action wrappers.
"""
import logging
import re

import allure
from playwright.sync_api import Page, expect

from config.settings import BASE_URL, DEFAULT_TIMEOUT, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)


class BasePage:
    """Provides shared Playwright helpers and Allure attachment utilities."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(DEFAULT_TIMEOUT)

    # ── Navigation ─────────────────────────────────────────────────────────────
    def navigate(self, path: str = "") -> None:
        url = f"{BASE_URL}{path}"
        logger.info("Navigating to %s", url)
        self.page.goto(url)

    # ── Screenshot helper ──────────────────────────────────────────────────────
    def take_screenshot(self, name: str) -> bytes:
        path = SCREENSHOTS_DIR / f"{name}.png"
        screenshot = self.page.screenshot(path=str(path), full_page=True)
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
        logger.info("Screenshot saved: %s", path)
        return screenshot

    # ── Assertions (wrapped for better logging) ────────────────────────────────
    def assert_url_contains(self, fragment: str) -> None:
        logger.debug("Asserting URL contains: %s", fragment)
        expect(self.page).to_have_url(re.compile(f".*{re.escape(fragment)}.*", re.IGNORECASE))

    def assert_title(self, title: str) -> None:
        logger.debug("Asserting page title: %s", title)
        expect(self.page).to_have_title(title)
