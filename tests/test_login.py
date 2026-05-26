from pages.login_page import Login
from playwright.sync_api import expect, Page




def test_valid_standard_user_login(login_page):
    expect(login_page).to_have_url("https://www.saucedemo.com/inventory.html")
    
def test_locked_user_login(page: Page):
    user = Login(page)
    user.login("locked_out_user", "secret_sauce")
    error_locator = user.page.locator("h3")
    expect(error_locator).to_contain_text("Epic sadface: Sorry, this user has been locked out.")
