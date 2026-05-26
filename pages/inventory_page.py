from playwright.sync_api import Page

class Invetory:
    def __init__(self, page : Page):
        self.page = page

    def add_to_cart(self, item):
        """
        Add item to cart when click "Add to cart" button
        """
        add_btn = item.locator("button")
        add_btn.click()

    def remove_from_cart(self, item):
        """
        Remove item from cart after added
        it when click on "Remove" button
        """
        remove_btn = item.locator("button")
        remove_btn.click()

    def get_cart_badge_count(self, css_locator="[data-test='shopping-cart-badge']"):
        """
        Get the number of items that are added to cart.
        """
        badge_count = self.page.locator(css_locator)
        return badge_count

    def get_inventory_count(self):
        """
        Get the number of items in the inventory page.
        """
        inventory_count = self.page.locator(".inventory_item")
        return inventory_count.count()

    def get_inventory_list(self):
        """
        REturn the list of items in the inventory page.
        """
        inventory_list = self.page.locator(".inventory_item")
        return inventory_list
    
    def get_items_names(self, inventory_list):
        """
        Get items names from invetory page.
        """
        item_name_list = list()
        count = inventory_list.count()
        for i in range(count):
            item = inventory_list.nth(i)
            # Get item name
            name = item.locator("[data-test='inventory-item-name']")
            item_name_list.append(name.text_content().strip())

        print("Names\n", item_name_list)
        return item_name_list

    def get_item_prices(self, inventory_list):
        """
        Get items price.
        """
        item_price_list = list()
        count = inventory_list.count()
        for i in range(count):
            item = inventory_list.nth(i)
            # Get item price
            price = item.locator("[data-test='inventory-item-price']")
            price = float(price.text_content().strip().replace("$", ""))
            item_price_list.append(price)

        print("Prices\n", item_price_list)
        return item_price_list

    def sort_items(self, sort_type):
        """
        choose sort type depending on what user choose
        """
        dropdown = self.page.locator(
        "[data-test='product-sort-container']"
        )

        dropdown.select_option(label=sort_type)
