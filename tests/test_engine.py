from __future__ import annotations

from ambicolor.engine import ColorCycleEngine
from ambicolor.models import PlaybackState


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.value = start

    def now(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


def test_state_transitions_and_freeze_behavior() -> None:
    clock = FakeClock()
    engine = ColorCycleEngine(clock=clock.now)

    engine.start()
    assert engine.state == PlaybackState.RUNNING

    clock.advance(2.0)
    engine._on_timer_tick()
    running_hex = engine.current_snapshot()["hex"]

    engine.pause()
    assert engine.state == PlaybackState.PAUSED
    clock.advance(2.0)
    engine._on_timer_tick()
    paused_hex = engine.current_snapshot()["hex"]
    assert paused_hex == running_hex

    engine.resume()
    assert engine.state == PlaybackState.RUNNING
    clock.advance(2.0)
    engine._on_timer_tick()
    resumed_hex = engine.current_snapshot()["hex"]
    assert resumed_hex != paused_hex

    engine.stop_standstill()
    assert engine.state == PlaybackState.STANDSTILL
    stopped_hex = engine.current_snapshot()["hex"]
    clock.advance(2.0)
    engine._on_timer_tick()
    assert engine.current_snapshot()["hex"] == stopped_hex


def test_cycle_duration_changes_hue_speed() -> None:
    clock = FakeClock()
    slow = ColorCycleEngine(clock=clock.now)
    fast = ColorCycleEngine(clock=clock.now)

    slow.set_random_start_hue(False)
    fast.set_random_start_hue(False)
    slow.set_cycle_duration(120)
    fast.set_cycle_duration(60)

    slow.start()
    fast.start()

    clock.advance(10.0)
    slow._on_timer_tick()
    fast._on_timer_tick()

    slow_hue = slow.current_snapshot()["hue_deg"]
    fast_hue = fast.current_snapshot()["hue_deg"]
    assert fast_hue > slow_hue


def test_random_start_hue_is_within_bounds() -> None:
    clock = FakeClock()
    engine = ColorCycleEngine(clock=clock.now)

    engine.set_random_start_hue(True)
    engine.start()
    hue = engine.current_snapshot()["hue_deg"]
    assert 0.0 <= hue < 360.0


def test_restricted_hue_range_bounces_without_hard_wrap() -> None:
    clock = FakeClock()
    engine = ColorCycleEngine(clock=clock.now)

    engine._hue_min_deg = 18.0
    engine._hue_max_deg = 95.0
    engine._current_hue_deg = 94.0
    engine._bounded_direction = 1.0
    engine._state = PlaybackState.RUNNING
    engine._last_tick_s = clock.now()
    engine.set_cycle_duration(60.0)

    clock.advance(1.0)
    engine._on_timer_tick()
    hue_after_bounce = engine.current_snapshot()["hue_deg"]
    assert 18.0 <= hue_after_bounce <= 95.0
    assert hue_after_bounce < 95.0

    clock.advance(1.0)
    engine._on_timer_tick()
    hue_next = engine.current_snapshot()["hue_deg"]
    assert hue_next < hue_after_bounce
