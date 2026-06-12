"""
InventoryPage – encapsulates all interactions with /inventory.html.
"""
import logging
from typing import List

from playwright.sync_api import Page, expect

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class InventoryPage(BasePage):
    """Page Object for the SauceDemo product listing page."""

    # ── Locators ───────────────────────────────────────────────────────────────
    PAGE_TITLE = ".title"
    PRODUCT_ITEMS = ".inventory_item"
    PRODUCT_NAMES = ".inventory_item_name"
    PRODUCT_PRICES = ".inventory_item_price"
    PRODUCT_IMAGES = ".inventory_item_img img"
    PRODUCT_DESCRIPTIONS = ".inventory_item_desc"
    ADD_TO_CART_BUTTONS = "button[data-test^='add-to-cart']"
    REMOVE_BUTTONS = "button[data-test^='remove']"
    SORT_DROPDOWN = 'select[data-test="product-sort-container"]'
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    BURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Navigation ─────────────────────────────────────────────────────────────
    def open(self) -> "InventoryPage":
        self.navigate("/inventory.html")
        return self

    def go_to_cart(self) -> None:
        logger.info("Navigating to cart")
        self.page.click(self.CART_LINK)

    def logout(self) -> None:
        logger.info("Logging out")
        self.page.click(self.BURGER_MENU)
        self.page.click(self.LOGOUT_LINK)

    # ── Actions ────────────────────────────────────────────────────────────────
    def sort_by(self, option: str) -> "InventoryPage":
        """Sort products using the visible inventory dropdown."""
        logger.info("Sorting by: %s", option)
        self.assert_url_contains("inventory")

        dropdown = self.page.locator(self.SORT_DROPDOWN)
        expect(dropdown).to_be_visible(timeout=15000)
        dropdown.select_option(value=option)
        expect(dropdown).to_have_value(option)
        return self

    def add_item_to_cart_by_name(self, product_name: str) -> "InventoryPage":
        logger.info("Adding to cart: %s", product_name)
        safe_name = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "").replace("'", "")
        self.page.click(f"[data-test='add-to-cart-{safe_name}']")
        return self

    def remove_item_from_cart_by_name(self, product_name: str) -> "InventoryPage":
        logger.info("Removing from cart: %s", product_name)
        safe_name = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "").replace("'", "")
        self.page.click(f"[data-test='remove-{safe_name}']")
        return self

    def add_all_items_to_cart(self) -> "InventoryPage":
        logger.info("Adding all items to cart")
        for btn in self.page.locator(self.ADD_TO_CART_BUTTONS).all():
            btn.click()
        return self

    # ── Getters ────────────────────────────────────────────────────────────────
    def get_product_names(self) -> List[str]:
        return [el.inner_text() for el in self.page.locator(self.PRODUCT_NAMES).all()]

    def get_product_prices(self) -> List[float]:
        texts = [el.inner_text() for el in self.page.locator(self.PRODUCT_PRICES).all()]
        return [float(t.replace("$", "")) for t in texts]

    def get_cart_item_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0:
            return 0
        return int(badge.inner_text())

    def get_product_count(self) -> int:
        return self.page.locator(self.PRODUCT_ITEMS).count()

    # ── Assertions ─────────────────────────────────────────────────────────────
    def assert_on_inventory_page(self) -> None:
        self.assert_url_contains("inventory")
        expect(self.page.locator(self.PAGE_TITLE)).to_have_text("Products")

    def assert_product_count(self, expected: int) -> None:
        logger.debug("Asserting product count == %d", expected)
        expect(self.page.locator(self.PRODUCT_ITEMS)).to_have_count(expected)

    def assert_cart_badge_count(self, expected: int) -> None:
        logger.debug("Asserting cart badge == %d", expected)
        if expected == 0:
            expect(self.page.locator(self.CART_BADGE)).to_be_hidden()
        else:
            expect(self.page.locator(self.CART_BADGE)).to_have_text(str(expected))

    def assert_products_sorted_az(self) -> None:
        names = self.get_product_names()
        assert names == sorted(names), f"Products not sorted A-Z: {names}"

    def assert_products_sorted_za(self) -> None:
        names = self.get_product_names()
        assert names == sorted(names, reverse=True), f"Products not sorted Z-A: {names}"

    def assert_products_sorted_price_low_high(self) -> None:
        prices = self.get_product_prices()
        assert prices == sorted(prices), f"Products not sorted price low-high: {prices}"

    def assert_products_sorted_price_high_low(self) -> None:
        prices = self.get_product_prices()
        assert prices == sorted(prices, reverse=True), f"Products not sorted price high-low: {prices}"

    def assert_all_products_have_image(self) -> None:
        for img in self.page.locator(self.PRODUCT_IMAGES).all():
            expect(img).to_be_visible()
            src = img.get_attribute("src")
            assert src and len(src) > 0, "Product image has no src"

    def assert_all_products_have_price(self) -> None:
        for price in self.page.locator(self.PRODUCT_PRICES).all():
            text = price.inner_text()
            assert text.startswith("$"), f"Unexpected price format: {text}"
