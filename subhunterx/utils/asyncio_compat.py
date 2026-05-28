"""
Asyncio compatibility helpers for platform-specific runtime behavior.
"""

import asyncio
import sys


def configure_windows_event_loop() -> None:
    """Use the selector event loop on Windows to avoid noisy Proactor SSL resets."""
    if not sys.platform.startswith("win"):
        return

    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        return
