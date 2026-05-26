import pytest
from playwright.sync_api import Page
from pages.login_page import Login
from config import STANDARD_USER, PASSWORD

@pytest.fixture
def login_page(page: Page):
    login_page = Login(page)
    login_page.login(STANDARD_USER, PASSWORD)
    yield page

