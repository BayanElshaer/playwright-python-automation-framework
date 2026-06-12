"""
tests/test_cart.py
==================
Functional tests for the SauceDemo shopping cart.

Covers
------
- Item appears in cart after add from inventory
- Item removed from cart updates state
- Cart persists items across navigation
- Empty cart state
- Checkout button navigation
"""
import logging

import allure
import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

logger = logging.getLogger(__name__)


@allure.feature("Cart")
class TestCart:
    """Suite: Shopping cart functionality."""

    @allure.title("Added item appears in cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_item_added_to_inventory_appears_in_cart(
        self, inventory_page: InventoryPage
    ):
        product = "Sauce Labs Backpack"
        with allure.step(f"Add '{product}' from inventory"):
            inventory_page.add_item_to_cart_by_name(product)

        with allure.step("Navigate to cart"):
            inventory_page.go_to_cart()

        with allure.step(f"'{product}' is visible in cart"):
            cart = CartPage(inventory_page.page)
            cart.assert_item_in_cart(product)

    @allure.title("Multiple items added appear in cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("products", [
        pytest.param(
            ["Sauce Labs Backpack", "Sauce Labs Bike Light"],
            id="two_items",
        ),
        pytest.param(
            ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie"],
            id="three_items",
        ),
    ])
    def test_multiple_items_appear_in_cart(
        self, inventory_page: InventoryPage, products: list
    ):
        with allure.step("Add items from inventory"):
            for p in products:
                inventory_page.add_item_to_cart_by_name(p)

        with allure.step("Go to cart"):
            inventory_page.go_to_cart()

        cart = CartPage(inventory_page.page)
        with allure.step(f"Cart contains {len(products)} items"):
            cart.assert_cart_item_count(len(products))
        with allure.step("Each added item is listed"):
            for p in products:
                cart.assert_item_in_cart(p)

    @allure.title("Removing item from cart updates cart state")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_item_from_cart(self, inventory_page: InventoryPage):
        products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        with allure.step("Add two items and go to cart"):
            for p in products:
                inventory_page.add_item_to_cart_by_name(p)
            inventory_page.go_to_cart()

        cart = CartPage(inventory_page.page)
        with allure.step("Remove first item"):
            cart.remove_item_by_name(products[0])

        with allure.step("Removed item is gone, second item remains"):
            cart.assert_item_not_in_cart(products[0])
            cart.assert_item_in_cart(products[1])
            cart.assert_cart_item_count(1)

    @allure.title("Empty cart has no items")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_cart_has_no_items(self, cart_page: CartPage):
        with allure.step("Cart is empty on fresh session"):
            cart_page.assert_cart_is_empty()

    @allure.title("Continue Shopping returns to inventory")
    @allure.severity(allure.severity_level.MINOR)
    def test_continue_shopping_navigates_back(self, cart_page: CartPage):
        with allure.step("Click Continue Shopping"):
            cart_page.continue_shopping()

        with allure.step("User is back on inventory page"):
            cart_page.assert_url_contains("inventory")

    @allure.title("All items removed – cart is empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_all_items_leaves_empty_cart(self, inventory_page: InventoryPage):
        with allure.step("Add multiple items"):
            inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
            inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
            inventory_page.go_to_cart()

        cart = CartPage(inventory_page.page)
        with allure.step("Remove all items"):
            cart.remove_all_items()

        with allure.step("Cart is now empty"):
            cart.assert_cart_is_empty()
