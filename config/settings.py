"""
Central configuration for the SauceDemo QA Automation Framework.
Values can be overridden via environment variables.
"""
import os
from pathlib import Path

# ── Project roots ──────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent
LOGS_DIR = ROOT_DIR / "logs"
REPORTS_DIR = ROOT_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"
VIDEOS_DIR = REPORTS_DIR / "videos"

for _dir in (LOGS_DIR, REPORTS_DIR, SCREENSHOTS_DIR, ALLURE_RESULTS_DIR, VIDEOS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ── Application ────────────────────────────────────────────────────────────────
BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")

# ── Browser ────────────────────────────────────────────────────────────────────
BROWSER: str = os.getenv("BROWSER", "chromium")           # chromium | firefox | webkit
HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))             # ms between actions
DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "10000"))  # ms

# ── Viewport ───────────────────────────────────────────────────────────────────
VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1280"))
VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "720"))

# ── Credentials (public test site – no secrets) ────────────────────────────────
STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
LOCKED_OUT_USER: str = os.getenv("LOCKED_OUT_USER", "locked_out_user")
PROBLEM_USER: str = os.getenv("PROBLEM_USER", "problem_user")
PERFORMANCE_GLITCH_USER: str = os.getenv("PERFORMANCE_GLITCH_USER", "performance_glitch_user")
PASSWORD: str = os.getenv("PASSWORD", "secret_sauce")
WRONG_PASSWORD: str = "wrong_password"
