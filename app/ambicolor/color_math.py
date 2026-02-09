from __future__ import annotations

from PySide6.QtGui import QColor


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def normalize_hue(hue_deg: float) -> float:
    return hue_deg % 360.0


def hsv_to_qcolor(hue_deg: float, saturation_pct: int, brightness_pct: int) -> QColor:
    h = normalize_hue(hue_deg) / 360.0
    s = clamp(float(saturation_pct), 0.0, 100.0) / 100.0
    v = clamp(float(brightness_pct), 0.0, 100.0) / 100.0
    return QColor.fromHsvF(h, s, v)


def qcolor_to_hex(color: QColor) -> str:
    return color.name(QColor.HexRgb).upper()


def normalize_hex(hex_color: str) -> str:
    value = hex_color.strip().upper()
    if not value:
        raise ValueError("hex color must not be empty")
    if not value.startswith("#"):
        value = f"#{value}"
    if len(value) != 7:
        raise ValueError(f"invalid hex length: {hex_color}")
    allowed = set("0123456789ABCDEF#")
    if any(ch not in allowed for ch in value):
        raise ValueError(f"invalid hex value: {hex_color}")
    return value
