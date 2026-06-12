"""
tests/test_login.py
===================
Comprehensive positive & negative login scenarios for SauceDemo.

Covers
------
- Valid login for each user type (data-driven)
- All invalid credential combinations (data-driven)
- Error message visibility and dismissal
- UI element presence on login page
"""
import logging

import allure
import pytest
from playwright.sync_api import Page

from config.settings import STANDARD_USER, PASSWORD
from pages.login_page import LoginPage
from test_data.test_data import VALID_LOGIN_USERS, INVALID_LOGIN_CASES

logger = logging.getLogger(__name__)


@allure.feature("Authentication")
@allure.story("Login")
class TestLogin:
    """Suite: Login page functional tests."""

    # ── Positive tests ─────────────────────────────────────────────────────────

    @allure.title("Valid login – {username}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("username, password", VALID_LOGIN_USERS)
    def test_valid_login_redirects_to_inventory(
        self, login_page: LoginPage, username: str, password: str
    ):
        """Successful logins for standard, problem, and performance-glitch users."""
        with allure.step(f"Login as {username}"):
            login_page.login(username, password)

        with allure.step("Verify redirect to inventory page"):
            login_page.assert_url_contains("inventory")

    @allure.title("Login page – UI elements are visible")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_elements_visible(self, login_page: LoginPage):
        with allure.step("Verify username field, password field and button are visible"):
            from playwright.sync_api import expect
            expect(login_page.page.locator(login_page.USERNAME_INPUT)).to_be_visible()
            expect(login_page.page.locator(login_page.PASSWORD_INPUT)).to_be_visible()
            expect(login_page.page.locator(login_page.LOGIN_BUTTON)).to_be_visible()

    # ── Negative tests ─────────────────────────────────────────────────────────

    @allure.title("Invalid login – {username!r} / {password!r}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("username, password, expected_error", INVALID_LOGIN_CASES)
    def test_invalid_login_shows_error(
        self,
        login_page: LoginPage,
        username: str,
        password: str,
        expected_error: str,
    ):
        """Covers empty credentials, wrong password, unknown user, and locked-out user."""
        with allure.step(f"Attempt login with username='{username}'"):
            login_page.login(username, password)

        with allure.step(f"Verify error: {expected_error}"):
            login_page.assert_error_message(expected_error)

        with allure.step("Verify user stays on login page"):
            login_page.assert_on_login_page()

    @allure.title("Error message can be dismissed")
    @allure.severity(allure.severity_level.MINOR)
    def test_error_message_can_be_dismissed(self, login_page: LoginPage):
        with allure.step("Trigger an error"):
            login_page.login("", "")

        with allure.step("Close error banner"):
            login_page.close_error()

        with allure.step("Error banner is gone"):
            login_page.assert_error_is_hidden()

    @allure.title("SQL injection attempt is safely rejected")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_sql_injection_is_rejected(self, login_page: LoginPage):
        with allure.step("Attempt SQL injection in username"):
            login_page.login("' OR '1'='1", PASSWORD)

        with allure.step("Verify login is rejected"):
            login_page.assert_on_login_page()
