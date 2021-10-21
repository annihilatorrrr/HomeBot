"""Homebot module."""

__version__ = "4.0.0"

from homebot.core.mdlintf import register_modules
from pathlib import Path

# I'm sorry
try:
    from config import config
except ModuleNotFoundError:
    config = {}

bot_path = Path(__file__).parent
modules_path = bot_path / "modules"

register_modules(modules_path)
