from __future__ import annotations

from .color_math import normalize_hex


class ColorNameStore:
    """In-memory mapping between hex colors and user-defined names."""

    def __init__(self) -> None:
        self._names: dict[str, str] = {}

    def set_name(self, hex_color: str, name: str) -> None:
        key = normalize_hex(hex_color)
        cleaned = name.strip()
        if cleaned:
            self._names[key] = cleaned
        elif key in self._names:
            del self._names[key]

    def get_name(self, hex_color: str) -> str | None:
        key = normalize_hex(hex_color)
        return self._names.get(key)
