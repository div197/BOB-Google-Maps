"""bob_core.utils

Shared helper utilities for Selenium interaction and safe extraction.
"""

from __future__ import annotations

import time
from typing import Any, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

__all__ = [
    "safe_find_element",
    "safe_get_text",
    "safe_get_attribute",
]

def safe_find_element(
    driver: WebDriver,
    by: str | By,
    value: str,
    timeout: int = 10,
    required: bool = False,
):
    """Wait for an element to appear and return it.

    Parameters
    ----------
    driver : WebDriver
        Selenium driver instance.
    by : str | By
        Locator strategy (e.g., By.CSS_SELECTOR).
    value : str
        Locator string.
    timeout : int, default 10
        Seconds to wait before giving up.
    required : bool, default False
        If *True* and element is not found, raise TimeoutException.
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        if required:
            raise
        return None  # type: ignore[return-value]

def safe_get_text(element: Optional[Any], default: str = "") -> str:
    """Return trimmed text of an element or *default* if element is None."""
    try:
        return element.text.strip() if element else default
    except Exception:
        return default

def safe_get_attribute(element: Optional[Any], attr: str, default: str = "") -> str:
    """Return an element attribute value (trimmed) or *default* if missing."""
    try:
        result = element.get_attribute(attr) if element else None
        return result.strip() if result else default
    except Exception:
        return default 