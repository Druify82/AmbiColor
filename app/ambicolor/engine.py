from __future__ import annotations

import random
import time
from collections.abc import Callable

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QColor

from .color_math import clamp, hsv_to_qcolor, normalize_hue, qcolor_to_hex
from .color_naming import ColorNameStore
from .i18n import tr
from .models import PlaybackState, PresetConfig, preset_catalog


class ColorCycleEngine(QObject):
    color_changed = Signal(QColor, str, str)
    state_changed = Signal(str)
    params_changed = Signal(dict)

    def __init__(
        self,
        *,
        language: str = "en",
        clock: Callable[[], float] | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._clock = clock or time.monotonic
        self._timer = QTimer(self)
        self._timer.setInterval(33)
        self._timer.timeout.connect(self._on_timer_tick)

        self._state = PlaybackState.STANDSTILL
        self._cycle_duration_s = 120.0
        self._saturation_pct = 80
        self._brightness_pct = 60
        self._random_start_hue = True
        self._hue_min_deg = 0.0
        self._hue_max_deg = 360.0
        self._bounded_direction = 1.0

        self._current_hue_deg = 0.0
        self._current_color = hsv_to_qcolor(self._current_hue_deg, self._saturation_pct, self._brightness_pct)
        self._last_tick_s: float | None = None

        self._name_store = ColorNameStore()

        self.apply_preset(preset_catalog()[0])

    @property
    def state(self) -> PlaybackState:
        return self._state

    def set_language(self, language: str) -> None:
        self._language = language
        self._emit_state_changed()
        self._emit_color_changed()

    def apply_preset(self, config: PresetConfig) -> None:
        self._cycle_duration_s = float(clamp(config.cycle_duration_s, 1.0, 3600.0))
        self._saturation_pct = int(clamp(config.saturation_pct, 0, 100))
        self._brightness_pct = int(clamp(config.brightness_pct, 0, 100))
        self._random_start_hue = bool(config.random_start_hue)
        self._hue_min_deg = normalize_hue(config.hue_min_deg)
        self._hue_max_deg = normalize_hue(config.hue_max_deg)
        self._bounded_direction = 1.0

        if self._state == PlaybackState.STANDSTILL:
            if self._random_start_hue:
                self._current_hue_deg = self._random_hue()
            else:
                self._current_hue_deg = self._hue_min_deg

        self._emit_color_changed()
        self.params_changed.emit(self.current_snapshot())

    def start(self) -> None:
        if self._state == PlaybackState.RUNNING:
            return
        if self._state == PlaybackState.PAUSED:
            self.resume()
            return

        if self._random_start_hue:
            self._current_hue_deg = self._random_hue()
        else:
            self._current_hue_deg = self._hue_min_deg

        self._last_tick_s = self._clock()
        self._state = PlaybackState.RUNNING
        self._timer.start()
        self._emit_color_changed()
        self._emit_state_changed()

    def pause(self) -> None:
        if self._state != PlaybackState.RUNNING:
            return
        self._timer.stop()
        self._last_tick_s = None
        self._state = PlaybackState.PAUSED
        self._emit_state_changed()

    def resume(self) -> None:
        if self._state != PlaybackState.PAUSED:
            return
        self._last_tick_s = self._clock()
        self._state = PlaybackState.RUNNING
        self._timer.start()
        self._emit_state_changed()

    def stop_standstill(self) -> None:
        if self._state == PlaybackState.STANDSTILL:
            return
        self._timer.stop()
        self._last_tick_s = None
        self._state = PlaybackState.STANDSTILL
        self._emit_state_changed()
        self._emit_color_changed()

    def set_cycle_duration(self, seconds: float) -> None:
        self._cycle_duration_s = float(clamp(seconds, 1.0, 3600.0))
        self.params_changed.emit(self.current_snapshot())

    def set_saturation(self, percent: int) -> None:
        self._saturation_pct = int(clamp(percent, 0, 100))
        self._emit_color_changed()
        self.params_changed.emit(self.current_snapshot())

    def set_brightness(self, percent: int) -> None:
        self._brightness_pct = int(clamp(percent, 0, 100))
        self._emit_color_changed()
        self.params_changed.emit(self.current_snapshot())

    def set_random_start_hue(self, enabled: bool) -> None:
        self._random_start_hue = bool(enabled)
        self.params_changed.emit(self.current_snapshot())

    def set_hue_name(self, hex_color: str, name: str) -> None:
        self._name_store.set_name(hex_color, name)
        self._emit_color_changed()

    def current_snapshot(self) -> dict:
        return {
            "state": self._state.value,
            "cycle_duration_s": self._cycle_duration_s,
            "saturation_pct": self._saturation_pct,
            "brightness_pct": self._brightness_pct,
            "random_start_hue": self._random_start_hue,
            "hue_deg": self._current_hue_deg,
            "hex": qcolor_to_hex(self._current_color),
        }

    def _on_timer_tick(self) -> None:
        if self._state != PlaybackState.RUNNING:
            return
        now = self._clock()
        if self._last_tick_s is None:
            self._last_tick_s = now
            return

        dt = max(0.0, now - self._last_tick_s)
        self._last_tick_s = now

        if self._cycle_duration_s <= 0:
            return

        span = self._hue_span()
        delta_hue = 360.0 * dt / self._cycle_duration_s
        if span < 360.0:
            self._current_hue_deg = self._advance_bounded_hue(delta_hue, span)
        else:
            self._current_hue_deg = normalize_hue(self._current_hue_deg + delta_hue)

        self._emit_color_changed()

    def _hue_span(self) -> float:
        span = (self._hue_max_deg - self._hue_min_deg) % 360.0
        return 360.0 if span == 0 else span

    def _random_hue(self) -> float:
        span = self._hue_span()
        if span >= 360.0:
            return random.uniform(0.0, 360.0)
        return normalize_hue(self._hue_min_deg + random.uniform(0.0, span))

    def _advance_bounded_hue(self, delta_hue: float, span: float) -> float:
        # Convert to a local coordinate within [0, span] and bounce at edges
        # to avoid a hard jump from max back to min.
        local = (self._current_hue_deg - self._hue_min_deg) % 360.0
        local = clamp(local, 0.0, span)
        local += delta_hue * self._bounded_direction

        while local > span or local < 0.0:
            if local > span:
                local = span - (local - span)
                self._bounded_direction = -1.0
            elif local < 0.0:
                local = -local
                self._bounded_direction = 1.0

        return normalize_hue(self._hue_min_deg + local)

    def _display_name_for_hex(self, hex_color: str) -> str:
        user_name = self._name_store.get_name(hex_color)
        if user_name:
            return f"{user_name} ({hex_color})"
        return f"{tr(self._language, 'text.unnamed')} ({hex_color})"

    def _emit_color_changed(self) -> None:
        self._current_color = hsv_to_qcolor(self._current_hue_deg, self._saturation_pct, self._brightness_pct)
        hex_color = qcolor_to_hex(self._current_color)
        display_name = self._display_name_for_hex(hex_color)
        self.color_changed.emit(self._current_color, hex_color, display_name)

    def _emit_state_changed(self) -> None:
        if self._state == PlaybackState.RUNNING:
            key = "state.running"
        elif self._state == PlaybackState.PAUSED:
            key = "state.paused"
        else:
            key = "state.standstill"
        self.state_changed.emit(tr(self._language, key))
