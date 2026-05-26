from pages.inventory_page import Invetory
from playwright.sync_api import expect
from conftest import login_page
import random

def test_add_remove_to_cart(login_page):
    """
    Test add remove elemnts in the cart.
    """
    # Create inventory page
    inventroy = Invetory(login_page)
    inventory_list = inventroy.get_inventory_list()
    added_items = list()

    # Choose random number to buy inventory items.
    count = inventory_list.count()
    added_elements_count = random.randint(1, count)

    # Add to cart from random list.
    for i in range(added_elements_count):
        item = inventory_list.nth(i)
        inventroy.add_to_cart(item)
        added_items.append(item)
    
    # Get badge count and check the count equal bought items.
    badge_count = inventroy.get_cart_badge_count()
    expect(badge_count).to_have_text(str(added_elements_count))

    # Choose random item from bought list to remove it from cart.
    random_item = random.choice(added_items)
    inventroy.remove_from_cart(random_item)

    # Check the cart count changed.
    count = inventroy.get_cart_badge_count(".shopping_cart_badge")
    expect(count).to_have_text(str(added_elements_count - 1))

def test_inventory_count(login_page):
    """
      Check the number of items in the inventory page is 6.
    """
    
    inventroy = Invetory(login_page)
    assert inventroy.get_inventory_count() == 6

def test_iamge_name_price_in_inventory_items(login_page):
    """
    Check the name, price, image and add to cart
     button for each item in inventory
    """
    inventroy = Invetory(login_page)
    inventory_list = inventroy.get_inventory_list()
    count = inventory_list.count()
    for i in range(count):
        item = inventory_list.nth(i)

        # Check name
        name = item.locator("[data-test='inventory-item-name']")
        expect(name).to_be_visible()
      
        assert name.text_content().strip() != ""

        # Check price
        price = item.locator("[data-test='inventory-item-price']")
        expect(price).to_be_visible()
        expect(price).to_contain_text("$")

        # Check image is visible 
        image = item.locator("img")
        expect(image).to_be_visible()
        src = image.get_attribute("src")
        assert src is not None
        assert "static/media" in src

        # Check "Add to cart" button
        button = item.locator("button")
        expect(button).to_be_visible()


def test_sorting(login_page):
    """
    Sorting test to check different sorting types:
    Name A - Z
    Name Z - A
    Price high - low
    Price low - high
    """ 
    # Get items list from inventory page before sorting
    inventroy = Invetory(login_page)
    inventory_list = inventroy.get_inventory_list()
    items_name_list = inventroy.get_items_names(inventory_list)
    items_price_list = inventroy.get_item_prices(inventory_list)

    # Sort items using Name A-Z
    inventroy.sort_items("Name (A to Z)")
    sorted_items = inventroy.get_items_names(inventory_list)
    assert sorted_items == sorted(items_name_list)

    # Sort Z to A
    inventroy.sort_items("Name (Z to A)")
    sorted_items = inventroy.get_items_names(inventory_list)
    assert sorted_items == sorted(items_name_list, reverse=True)

    # Sort price low to high
    inventroy.sort_items("Price (low to high)")
    sorted_items = inventroy.get_item_prices(inventory_list)
    assert sorted_items == sorted(items_price_list)

    # Sort price high to low
    inventroy.sort_items("Price (high to low)")
    sorted_items = inventroy.get_item_prices(inventory_list)
    assert sorted_items == sorted(items_price_list, reverse=True)
