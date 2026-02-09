from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PlaybackState(str, Enum):
    STANDSTILL = "standstill"
    RUNNING = "running"
    PAUSED = "paused"


class PresetId(str, Enum):
    CLASSIC = "classic"
    AMBIENT_LAMP = "ambient_lamp"
    SPECTRUM_SWEEP = "spectrum_sweep"
    NATURAL_ARTISTIC = "natural_artistic"


@dataclass(slots=True)
class PresetConfig:
    preset_id: PresetId
    label_key: str
    description_key: str
    cycle_duration_s: float
    saturation_pct: int
    brightness_pct: int
    random_start_hue: bool
    hue_min_deg: float
    hue_max_deg: float
    implemented: bool


def preset_catalog() -> list[PresetConfig]:
    return [
        PresetConfig(
            preset_id=PresetId.CLASSIC,
            label_key="preset.classic",
            description_key="preset.desc.classic",
            cycle_duration_s=120.0,
            saturation_pct=80,
            brightness_pct=60,
            random_start_hue=True,
            hue_min_deg=0.0,
            hue_max_deg=360.0,
            implemented=True,
        ),
        PresetConfig(
            preset_id=PresetId.AMBIENT_LAMP,
            label_key="preset.ambient_lamp",
            description_key="preset.desc.ambient_lamp",
            cycle_duration_s=210.0,
            saturation_pct=35,
            brightness_pct=42,
            random_start_hue=False,
            hue_min_deg=25.0,
            hue_max_deg=205.0,
            implemented=False,
        ),
        PresetConfig(
            preset_id=PresetId.SPECTRUM_SWEEP,
            label_key="preset.spectrum_sweep",
            description_key="preset.desc.spectrum_sweep",
            cycle_duration_s=75.0,
            saturation_pct=95,
            brightness_pct=68,
            random_start_hue=False,
            hue_min_deg=0.0,
            hue_max_deg=360.0,
            implemented=False,
        ),
        PresetConfig(
            preset_id=PresetId.NATURAL_ARTISTIC,
            label_key="preset.natural_artistic",
            description_key="preset.desc.natural_artistic",
            cycle_duration_s=300.0,
            saturation_pct=48,
            brightness_pct=52,
            random_start_hue=False,
            hue_min_deg=18.0,
            hue_max_deg=95.0,
            implemented=False,
        ),
    ]


def preset_by_id(preset_id: PresetId) -> PresetConfig:
    for preset in preset_catalog():
        if preset.preset_id == preset_id:
            return preset
    raise ValueError(f"Unknown preset id: {preset_id}")
