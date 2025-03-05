import pathlib
from typing import Mapping

import pytest


def pytest_make_parametrize_id(config, val):
    """
    Parametrized tests that provide an ID will use it as the test case name."""
    if isinstance(val, Mapping):
        return val.get("id", None)
    return None



def pytest_collection_modifyitems(config, items):
    """
    Automatically marks unit and integration tests based on their parent directory tree
    """
    rootdir = pathlib.Path(config.rootdir)
    for item in items:
        relative_path = pathlib.Path(item.fspath).relative_to(rootdir)
        mark_name = next((part for part in relative_path.parts if part in ["unit", "integration"]))
        if mark_name:
            mark = getattr(pytest.mark, mark_name)
            item.add_marker(mark)