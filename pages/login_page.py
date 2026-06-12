"""
LoginPage – encapsulates all interactions with the SauceDemo login screen.
"""
import logging

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page Object for https://www.saucedemo.com (login screen)."""

    # ── Locators ───────────────────────────────────────────────────────────────
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_CLOSE_BUTTON = ".error-button"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ────────────────────────────────────────────────────────────────
    def open(self) -> "LoginPage":
        self.navigate("/")
        return self

    def enter_username(self, username: str) -> "LoginPage":
        logger.debug("Entering username: %s", username)
        self.page.fill(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        logger.debug("Entering password")
        self.page.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        logger.info("Clicking login button")
        self.page.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Full login flow in one call."""
        logger.info("Logging in as '%s'", username)
        self.open()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def close_error(self) -> None:
        self.page.click(self.ERROR_CLOSE_BUTTON)

    # ── Assertions ─────────────────────────────────────────────────────────────
    def assert_error_message(self, expected_text: str) -> None:
        logger.debug("Asserting error message: %s", expected_text)
        expect(self.page.locator(self.ERROR_MESSAGE)).to_be_visible()
        expect(self.page.locator(self.ERROR_MESSAGE)).to_have_text(expected_text)

    def assert_error_is_hidden(self) -> None:
        expect(self.page.locator(self.ERROR_MESSAGE)).to_be_hidden()

    def assert_on_login_page(self) -> None:
        self.assert_url_contains("/")
        expect(self.page.locator(self.LOGIN_BUTTON)).to_be_visible()

    # ── Getters ────────────────────────────────────────────────────────────────
    def get_error_message(self) -> str:
        return self.page.locator(self.ERROR_MESSAGE).inner_text()
