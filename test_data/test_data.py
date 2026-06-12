"""
Centralised test-data for data-driven tests.
Each entry is a pytest.param with id & marks for clarity in reports.
"""
import pytest
from config.settings import (
    STANDARD_USER,
    LOCKED_OUT_USER,
    PROBLEM_USER,
    PERFORMANCE_GLITCH_USER,
    PASSWORD,
    WRONG_PASSWORD,
)

# ── Login – positive ───────────────────────────────────────────────────────────
VALID_LOGIN_USERS = [
    pytest.param(STANDARD_USER, PASSWORD, id="standard_user"),
    pytest.param(PROBLEM_USER, PASSWORD, id="problem_user"),
    pytest.param(PERFORMANCE_GLITCH_USER, PASSWORD, id="performance_glitch_user"),
]

# ── Login – negative ───────────────────────────────────────────────────────────
INVALID_LOGIN_CASES = [
    pytest.param(
        "",
        "",
        "Epic sadface: Username is required",
        id="empty_credentials",
    ),
    pytest.param(
        STANDARD_USER,
        "",
        "Epic sadface: Password is required",
        id="empty_password",
    ),
    pytest.param(
        "",
        PASSWORD,
        "Epic sadface: Username is required",
        id="empty_username",
    ),
    pytest.param(
        STANDARD_USER,
        WRONG_PASSWORD,
        "Epic sadface: Username and password do not match any user in this service",
        id="wrong_password",
    ),
    pytest.param(
        "nonexistent_user",
        PASSWORD,
        "Epic sadface: Username and password do not match any user in this service",
        id="unknown_username",
    ),
    pytest.param(
        LOCKED_OUT_USER,
        PASSWORD,
        "Epic sadface: Sorry, this user has been locked out.",
        id="locked_out_user",
    ),
]

# ── Sorting options ────────────────────────────────────────────────────────────
SORT_OPTIONS = [
    pytest.param("az", "Name (A to Z)", id="sort_az"),
    pytest.param("za", "Name (Z to A)", id="sort_za"),
    pytest.param("lohi", "Price (low to high)", id="sort_price_low_high"),
    pytest.param("hilo", "Price (high to low)", id="sort_price_high_low"),
]

# ── Products ───────────────────────────────────────────────────────────────────
EXPECTED_PRODUCT_COUNT = 6

EXPECTED_PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)",
]
