import pytest
from nonebug import App

from pathlib import Path
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from nonebot.plugin import Plugin

@pytest.fixture
def load_plugins(nonebug_init: None) -> Set['Plugin']
    import nonebot

    return nonebot.load_plugin("yakumo/plugin/nonebot-plugin-Niuzi")



