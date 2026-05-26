from playwright.sync_api import Page

class Login:
    def __init__(self, page: Page):
        self.page = page
        self.page.goto("https://www.saucedemo.com/")
        self.user_name = self.page.get_by_placeholder("Username")
        self.password = self.page.get_by_placeholder("Password")
        self.login_btn = self.page.locator("input#login-button")

    def login(self, userName, password):
        self.user_name.fill(userName)
        self.password.fill(password)
        self.login_btn.click()


