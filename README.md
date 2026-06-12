# 🧪 SauceDemo QA Automation Framework

> **Production-grade UI test automation** built with Python · Playwright · Pytest · Allure  
> Demonstrating enterprise-level QA engineering for the [SauceDemo](https://www.saucedemo.com) e-commerce application.
>
> Current capabilities include: Allure reporting, GitHub Actions CI, failure screenshots, video recording, structured logging, Page Object Model, and data-driven parametrized tests.

[![CI – QA Automation](https://github.com/<YOUR_USERNAME>/playwright-python-automation-framework/actions/workflows/qa-automation.yml/badge.svg)](https://github.com/<YOUR_USERNAME>/playwright-python-automation-framework/actions)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.44+-green?logo=playwright)
![Pytest](https://img.shields.io/badge/Pytest-8.x-orange)
![Allure](https://img.shields.io/badge/Allure-2.27-yellow)

---

## 📑 Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Test Coverage](#test-coverage)
- [Setup & Installation](#setup--installation)
- [Running Tests](#running-tests)
- [Reporting](#reporting)
- [CI/CD](#cicd)
- [Future Improvements](#future-improvements)

---

## Architecture

The framework follows a **layered architecture** separating concerns cleanly:

```
┌─────────────────────────────────────────────────────┐
│                    TESTS LAYER                      │
│          test_login  test_inventory  test_cart      │
├─────────────────────────────────────────────────────┤
│                  FIXTURES LAYER                     │
│         conftest.py – shared pytest fixtures        │
├─────────────────────────────────────────────────────┤
│               PAGE OBJECTS LAYER                    │
│     LoginPage  InventoryPage  CartPage  BasePage    │
├─────────────────────────────────────────────────────┤
│              INFRASTRUCTURE LAYER                   │
│   config/settings.py  utils/logger  test_data/     │
└─────────────────────────────────────────────────────┘
```

**Design patterns applied:**
- **Page Object Model (POM)** – each page is a class, tests never touch raw selectors
- **Base Page** – shared helpers (navigate, screenshot, assert_url) inherited by all pages
- **Fixture composition** – `login_page → authenticated_page → inventory_page` chain
- **Data-driven testing** – `pytest.mark.parametrize` with `test_data/test_data.py`
- **Builder / fluent API** – page methods return `self` for chaining

---

## What This Framework Covers

This project already includes the core QA engineering pillars expected in a modern UI automation suite:

- ✅ Allure reports with rich test steps and failure evidence
- ✅ GitHub Actions CI pipeline for automated validation
- ✅ Automatic screenshots on failed tests
- ✅ Video recording for debugging and retraceability
- ✅ Structured logging to console and file
- ✅ Page Object Model (POM) for reusable, maintainable selectors and flows
- ✅ Parametrized pytest tests for login, sorting, and cart scenarios

This makes the README accurate for the current implementation, not just the future roadmap.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Language |
| Playwright | Browser automation (Chromium, Firefox, WebKit) |
| Pytest 8 | Test runner, parametrize, fixtures |
| pytest-playwright | Playwright ↔ Pytest integration |
| Allure | Rich HTML reports with steps & screenshots |
| pytest-xdist | Parallel test execution |
| pytest-timeout | Per-test timeout guard |
| GitHub Actions | CI/CD pipeline |

---

## Project Structure

```
saucedemo-qa-framework/
│
├── .github/
│   └── workflows/
│       └── qa-automation.yml       # CI/CD pipeline (Ubuntu, Pytest, Allure, artifact upload)
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Env-configurable settings (URL, browser, creds)
│
├── pages/                          # Page Object Model
│   ├── __init__.py
│   ├── base_page.py                # Shared helpers (navigate, screenshot, asserts)
│   ├── login_page.py               # Login screen interactions
│   ├── inventory_page.py           # Product listing interactions
│   └── cart_page.py                # Shopping cart interactions
│
├── tests/                          # Test suites
│   ├── __init__.py
│   ├── test_login.py               # 10 login scenarios (positive + negative)
│   ├── test_inventory.py           # Product count, sorting, cart badge tests
│   └── test_cart.py                # Cart add/remove/persist/empty tests
│
├── test_data/
│   ├── __init__.py
│   └── test_data.py                # Centralised parametrize datasets
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                   # Rotating file + console structured logging
│   └── allure_helpers.py           # @allure_step decorator
│
├── reports/                        # Generated – gitignored
│   ├── allure-results/
│   ├── allure-report/
│   ├── screenshots/
│   └── videos/
│
├── logs/                           # Generated – gitignored
│   └── test_execution.log
│
├── conftest.py                     # Root fixtures + screenshot-on-failure hook
├── pytest.ini                      # Pytest configuration
├── requirements.txt
└── README.md
```

---

## Test Coverage

### Login (`test_login.py`)
| Scenario | Type |
|----------|------|
| Standard / Problem / Performance-glitch user login | Positive · Parametrized |
| Login page UI elements visible | Positive |
| Empty username + empty password | Negative · Parametrized |
| Empty password only | Negative |
| Empty username only | Negative |
| Wrong password | Negative |
| Unknown username | Negative |
| Locked-out user | Negative |
| Error banner dismissal | UX |
| SQL injection attempt | Security |

### Inventory (`test_inventory.py`)
| Scenario | Type |
|----------|------|
| 6 products displayed | Validation |
| All expected products present | Validation |
| All products have images | Validation |
| All products have price tags | Validation |
| All prices > 0 | Validation |
| Sort A–Z / Z–A / Low–High / High–Low | Functional · Parametrized |
| Add single item → badge = 1 | Functional |
| Add then remove → badge = 0 | Functional |
| Add 2 / 3 items → badge count matches | Functional · Parametrized |

### Cart (`test_cart.py`)
| Scenario | Type |
|----------|------|
| Added item appears in cart | Functional |
| Multiple items (2 / 3) appear in cart | Functional · Parametrized |
| Remove one item, other remains | Functional |
| Empty cart on fresh session | Validation |
| Continue Shopping → back to inventory | Navigation |
| Remove all items → cart empty | Functional |

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/<YOUR_USERNAME>/playwright-python-automation-framework.git
cd playwright-python-automation-framework
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install                # installs all three browser binaries
```

### 4. Optional – configure via environment variables
```bash
export BASE_URL=https://www.saucedemo.com
export BROWSER=chromium           # chromium | firefox | webkit
export HEADLESS=true
export SLOW_MO=0                  # ms between actions; useful for debugging
```

---

## Running Tests

### Run the full suite
```bash
pytest
```

### Run in parallel (recommended for CI)
```bash
pytest -n auto
```

### Run a specific module
```bash
pytest tests/test_login.py -v
```

### Run with a specific browser
```bash
pytest --browser firefox
pytest --browser webkit
```

### Run headed (visible browser window)
```bash
pytest --headed
```

### Run by marker
```bash
pytest -m smoke
pytest -m security
pytest -m "not slow"
```

### Run a specific test by name
```bash
pytest -k "test_valid_login"
pytest -k "locked_out"
```

---

## Reporting

### Allure (rich interactive report)

> Requires [Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline) installed.

```bash
# Tests automatically write results to reports/allure-results/
pytest

# Generate and open HTML report
allure serve reports/allure-results
```

The Allure report includes:
- ✅ Test pass/fail status with duration
- 📋 Allure steps (`@allure.step`) inside each test
- 🖼️ Screenshots automatically attached on failure
- 🏷️ Features, Stories, Severities and custom markers
- 📊 Trend graphs across multiple CI runs

### Logs

Structured logs are written to `logs/test_execution.log` and printed to the console.
Log rotation is configured at 5 MB with 3 backups.

---

## CI/CD

The GitHub Actions workflow (`.github/workflows/qa-automation.yml`) is now set up to run on:
- push to `main`
- pull requests
- manual `workflow_dispatch`

**What is currently covered in the pipeline:**

1. Ubuntu latest runner with Python 3.12
2. Dependency installation via `pip install -r requirements.txt`
3. Playwright browser/runtime setup for UI execution
4. Pytest execution with parallel workers (`pytest -n auto`)
5. Allure result generation and HTML report creation
6. Artifact upload for:
   - `allure-report`
   - `allure-results`
   - `screenshots`
   - `videos`
   - `logs`

**What is still planned for the future:**
- Browser matrix execution for Chromium, Firefox, and WebKit
- Scheduled nightly runs for regression confidence
- GitHub Pages deployment for Allure history/trend reporting
- Additional resilience features such as retry-on-flake handling

---

## Future Improvements

| Area | Improvement |
|------|------------|
| **Browser Matrix CI** | Add Chromium / Firefox / WebKit matrix jobs for wider cross-browser validation |
| **Scheduled Nightly Runs** | Run regression suites automatically overnight for early defect detection |
| **Allure Pages Publishing** | Deploy HTML reports to GitHub Pages with historical trend graphs |
| **Retry on Flake** | Add `pytest-rerunfailures` for flaky UI scenarios |
| **API Layer** | Add `requests`/`httpx` API tests to complement UI coverage |
| **Docker** | Add `Dockerfile` + `docker-compose` for fully reproducible local execution |
| **Checkout Flow** | Extend coverage to checkout step 1, step 2, and order confirmation |
| **Visual Testing** | Integrate `pytest-playwright-visual` for pixel-diff screenshots |
| **Accessibility** | Add `axe-playwright-python` for WCAG compliance checks |
| **Performance** | Add Playwright HAR capture and Lighthouse-style performance checks |
| **Security** | Add OWASP ZAP passive scanning in CI |

---

## Author

**Bayan Alshaer** · Senior QA Automation Engineer  
[LinkedIn](https://www.linkedin.com/in/byan-alshaer-19173421a) · [GitHub](https://github.com/BayanElshaer)
