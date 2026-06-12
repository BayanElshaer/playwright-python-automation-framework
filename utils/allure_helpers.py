"""
Allure helper decorators and context managers used in tests.
"""
import functools
import logging
from typing import Callable

import allure

logger = logging.getLogger(__name__)


def allure_step(title: str):
    """Decorator: wraps a function in an @allure.step and logs it."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @allure.step(title)
        def wrapper(*args, **kwargs):
            logger.info("STEP: %s", title)
            return func(*args, **kwargs)
        return wrapper
    return decorator
