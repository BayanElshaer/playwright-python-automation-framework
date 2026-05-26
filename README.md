# playwright-python-automation-framework
UI test automation framework built using Python, Playwright, and Pytest.

The framework automates end-to-end testing scenarios for the SauceDemo e-commerce application using the Page Object Model (POM) design pattern and reusable Pytest fixtures.

---

# Application Under Test

https://www.saucedemo.com/

---

# Tech Stack

- Python
- Playwright
- Pytest
- Pytest Fixtures
- Page Object Model (POM)
- Git
- GitHub

---

# Project Structure

```bash
project/
│
├── pages/
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│
├── data/
│
├── conftest.py
├── requirements.txt
├── README.md

Implemented Test Scenarios
  Login Tests
   - Valid login
   - Invalid login
   - Locked user validation
   - Empty credentials validation

 Inventory Tests
  - Verify inventory contains 6 items
  - Verify each product contains:
  - Image
  - Product name
  - Product price
  - Add-to-cart button
  - Verify add/remove cart functionality
  - Verify cart badge updates dynamically
 Verify sorting:
  - Name A-Z
  - Name Z-A
  - Price Low-High
  - Price High-Low
 Cart Tests
  - Verify added items appear in cart
  - Verify remove item from cart
  - Verify cart state updates correctly

 Framework Features
  - Page Object Model (POM)
  - Reusable Pytest Fixtures
  - Clean test structure
  - Dynamic validations using Python
  - Reusable page methods

 Parameterized test scenarios
 Installation
  - Bash
  - pip install -r requirements.txt
  - playwright install

 Run Tests
  Run all tests:
   - Bash
   - pytest

Run tests with verbose mode:
 - Bash
 - pytest -v

Future Improvements
 - HTML reports
 - Screenshots on failure
 - CI/CD integration using GitHub Actions
 - API testing
 - Docker support
 - Parallel execution

Author
Byan Alshaer Senior QA Automation Engineer
