"""
CartPage – encapsulates all interactions with /cart.html.
"""
import logging
from typing import List

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Page Object for the SauceDemo shopping cart page."""

    # ── Locators ───────────────────────────────────────────────────────────────
    PAGE_TITLE = ".title"
    CART_ITEMS = ".cart_item"
    CART_ITEM_NAMES = ".inventory_item_name"
    CART_ITEM_PRICES = ".inventory_item_price"
    CART_ITEM_QUANTITIES = ".cart_quantity"
    REMOVE_BUTTONS = "button[data-test^='remove']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Navigation ─────────────────────────────────────────────────────────────
    def open(self) -> "CartPage":
        self.navigate("/cart.html")
        return self

    def continue_shopping(self) -> None:
        logger.info("Clicking Continue Shopping")
        self.page.click(self.CONTINUE_SHOPPING_BUTTON)

    def proceed_to_checkout(self) -> None:
        logger.info("Clicking Checkout")
        self.page.click(self.CHECKOUT_BUTTON)

    # ── Actions ────────────────────────────────────────────────────────────────
    def remove_item_by_name(self, product_name: str) -> "CartPage":
        logger.info("Removing from cart: %s", product_name)
        safe = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "").replace("'", "")
        self.page.click(f"[data-test='remove-{safe}']")
        return self

    def remove_all_items(self) -> "CartPage":
        logger.info("Removing all items from cart")
        while True:
            remove_buttons = self.page.locator(self.REMOVE_BUTTONS)
            if remove_buttons.count() == 0:
                break

            current_count = remove_buttons.count()
            expect(remove_buttons.first).to_be_visible(timeout=15000)
            remove_buttons.first.click()
            expect(remove_buttons).to_have_count(current_count - 1, timeout=15000)
        return self

    # ── Getters ────────────────────────────────────────────────────────────────
    def get_cart_item_names(self) -> List[str]:
        return [el.inner_text() for el in self.page.locator(self.CART_ITEM_NAMES).all()]

    def get_cart_item_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count()

    def get_cart_item_prices(self) -> List[float]:
        texts = [el.inner_text() for el in self.page.locator(self.CART_ITEM_PRICES).all()]
        return [float(t.replace("$", "")) for t in texts]

    # ── Assertions ─────────────────────────────────────────────────────────────
    def assert_on_cart_page(self) -> None:
        self.assert_url_contains("cart")
        expect(self.page.locator(self.PAGE_TITLE)).to_have_text("Your Cart")

    def assert_item_in_cart(self, product_name: str) -> None:
        logger.debug("Asserting item in cart: %s", product_name)
        expect(self.page.locator(self.CART_ITEM_NAMES).filter(has_text=product_name)).to_be_visible()

    def assert_item_not_in_cart(self, product_name: str) -> None:
        logger.debug("Asserting item not in cart: %s", product_name)
        expect(self.page.locator(self.CART_ITEM_NAMES).filter(has_text=product_name)).to_be_hidden()

    def assert_cart_is_empty(self) -> None:
        logger.debug("Asserting cart is empty")
        expect(self.page.locator(self.CART_ITEMS)).to_have_count(0)

    def assert_cart_item_count(self, expected: int) -> None:
        expect(self.page.locator(self.CART_ITEMS)).to_have_count(expected)
