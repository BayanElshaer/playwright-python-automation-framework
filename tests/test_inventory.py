"""
tests/test_inventory.py
=======================
Functional tests for the SauceDemo product inventory page.

Covers
------
- Product count & content validation
- Add / remove single and multiple products
- Cart badge count updates
- All four sort modes (data-driven)
"""
import logging

import allure
import pytest

from pages.inventory_page import InventoryPage
from test_data.test_data import (
    EXPECTED_PRODUCT_COUNT,
    EXPECTED_PRODUCTS,
    SORT_OPTIONS,
)

logger = logging.getLogger(__name__)


@allure.feature("Inventory")
class TestInventoryProducts:
    """Suite: Product listing and attribute validation."""

    @allure.title("Inventory page displays exactly 6 products")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_count_is_six(self, inventory_page: InventoryPage):
        with allure.step(f"Assert {EXPECTED_PRODUCT_COUNT} products are displayed"):
            inventory_page.assert_product_count(EXPECTED_PRODUCT_COUNT)

    @allure.title("All expected products are present")
    @allure.severity(allure.severity_level.NORMAL)
    def test_all_expected_products_present(self, inventory_page: InventoryPage):
        with allure.step("Get displayed product names"):
            displayed = inventory_page.get_product_names()

        with allure.step("Verify each expected product is listed"):
            for product in EXPECTED_PRODUCTS:
                assert product in displayed, f"Product not found: {product}"

    @allure.title("Every product has a visible image")
    @allure.severity(allure.severity_level.NORMAL)
    def test_all_products_have_images(self, inventory_page: InventoryPage):
        with allure.step("Assert all product images are visible and have src"):
            inventory_page.assert_all_products_have_image()

    @allure.title("Every product has a valid price tag")
    @allure.severity(allure.severity_level.NORMAL)
    def test_all_products_have_prices(self, inventory_page: InventoryPage):
        with allure.step("Assert all product prices start with $"):
            inventory_page.assert_all_products_have_price()

    @allure.title("All product prices are positive numbers")
    @allure.severity(allure.severity_level.MINOR)
    def test_product_prices_are_positive(self, inventory_page: InventoryPage):
        prices = inventory_page.get_product_prices()
        with allure.step("Assert every price > 0"):
            for price in prices:
                assert price > 0, f"Non-positive price: {price}"


@allure.feature("Inventory")
@allure.story("Sorting")
class TestInventorySorting:
    """Suite: Product sorting functionality."""

    @allure.title("Sort products – {label}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("option, label", SORT_OPTIONS)
    def test_sort_products(self, inventory_page: InventoryPage, option: str, label: str):
        with allure.step(f"Select sort option: {label}"):
            inventory_page.sort_by(option)

        with allure.step("Verify products are in expected order"):
            if option == "az":
                inventory_page.assert_products_sorted_az()
            elif option == "za":
                inventory_page.assert_products_sorted_za()
            elif option == "lohi":
                inventory_page.assert_products_sorted_price_low_high()
            elif option == "hilo":
                inventory_page.assert_products_sorted_price_high_low()


@allure.feature("Inventory")
@allure.story("Cart Interaction")
class TestInventoryCart:
    """Suite: Add / Remove product interactions from inventory."""

    @allure.title("Add one item – cart badge shows 1")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_single_item_updates_badge(self, inventory_page: InventoryPage):
        product = "Sauce Labs Backpack"
        with allure.step(f"Add '{product}' to cart"):
            inventory_page.add_item_to_cart_by_name(product)

        with allure.step("Cart badge shows 1"):
            inventory_page.assert_cart_badge_count(1)

    @allure.title("Remove item resets badge to 0")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_item_resets_badge(self, inventory_page: InventoryPage):
        product = "Sauce Labs Backpack"
        with allure.step(f"Add then remove '{product}'"):
            inventory_page.add_item_to_cart_by_name(product)
            inventory_page.remove_item_from_cart_by_name(product)

        with allure.step("Cart badge is hidden (0 items)"):
            inventory_page.assert_cart_badge_count(0)

    @allure.title("Add multiple items – badge count equals items added")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("count,products", [
        pytest.param(2, ["Sauce Labs Backpack", "Sauce Labs Bike Light"], id="add_2"),
        pytest.param(3, ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"], id="add_3"),
    ])
    def test_add_multiple_items_badge_count(
        self, inventory_page: InventoryPage, count: int, products: list
    ):
        with allure.step(f"Add {count} items to cart"):
            for p in products:
                inventory_page.add_item_to_cart_by_name(p)

        with allure.step(f"Badge count equals {count}"):
            inventory_page.assert_cart_badge_count(count)
