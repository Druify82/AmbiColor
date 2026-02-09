from __future__ import annotations

import pytest

from ambicolor.color_naming import ColorNameStore


def test_set_get_overwrite_delete() -> None:
    store = ColorNameStore()

    store.set_name("#AABBCC", "Calm Sky")
    assert store.get_name("#AABBCC") == "Calm Sky"

    store.set_name("#AABBCC", "Evening Sky")
    assert store.get_name("#AABBCC") == "Evening Sky"

    store.set_name("#AABBCC", "")
    assert store.get_name("#AABBCC") is None


def test_hex_normalization() -> None:
    store = ColorNameStore()
    store.set_name("aabbcc", "Named")
    assert store.get_name("#AABBCC") == "Named"
    assert store.get_name("#aabbcc") == "Named"


@pytest.mark.parametrize("value", ["", "#12", "#GGHHII"])
def test_invalid_hex_raises(value: str) -> None:
    store = ColorNameStore()
    with pytest.raises(ValueError):
        store.set_name(value, "x")
