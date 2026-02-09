from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from ambicolor.ui_main_window import MainWindow


def _normalize_focus(widget, known):
    current = widget
    while current is not None and current not in known:
        current = current.parentWidget()
    return current


def test_initial_focus_and_default_preset(qtbot) -> None:
    window = MainWindow(language="en")
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(120)

    assert window.controls.preset_combo.hasFocus()
    assert "Classic" in window.controls.preset_combo.currentText()
    assert "Baseline lamp behavior" in window.controls.preset_description_edit.toPlainText()


def test_all_controls_have_accessible_names(qtbot) -> None:
    window = MainWindow(language="en")
    qtbot.addWidget(window)

    controls = [
        window.controls.preset_combo,
        window.controls.preset_description_edit,
        window.controls.speed_slider,
        window.controls.speed_spin,
        window.controls.saturation_slider,
        window.controls.saturation_spin,
        window.controls.brightness_slider,
        window.controls.brightness_spin,
        window.controls.random_start_checkbox,
        window.controls.playback_button,
        window.controls.stop_button,
        window.controls.fullscreen_button,
        window.controls.color_name_input,
        window.controls.save_name_button,
        window.controls.status_label,
    ]

    for control in controls:
        assert control.accessibleName().strip()


def test_tab_navigation_reaches_all_required_controls(qtbot) -> None:
    window = MainWindow(language="en")
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(120)

    ordered_controls = [
        window.controls.preset_combo,
        window.controls.preset_description_edit,
        window.controls.speed_slider,
        window.controls.speed_spin,
        window.controls.saturation_slider,
        window.controls.saturation_spin,
        window.controls.brightness_slider,
        window.controls.brightness_spin,
        window.controls.random_start_checkbox,
        window.controls.playback_button,
        window.controls.stop_button,
        window.controls.fullscreen_button,
        window.controls.color_name_input,
        window.controls.save_name_button,
    ]
    required_controls = [control for control in ordered_controls if control.isEnabled()]

    seen = set()
    window.controls.preset_combo.setFocus()

    for _ in range(60):
        focused = _normalize_focus(window.focusWidget(), required_controls)
        if focused is not None:
            seen.add(focused)
        QTest.keyClick(window, Qt.Key.Key_Tab)

    assert all(control in seen for control in required_controls)


def test_f11_toggles_fullscreen_and_keeps_focus(qtbot) -> None:
    window = MainWindow(language="en")
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(120)

    window.controls.preset_combo.setFocus()
    assert window.focusWidget() is not None

    qtbot.keyClick(window, Qt.Key.Key_F11)
    qtbot.wait(120)
    assert window.isFullScreen()
    assert window.focusWidget() is not None
    assert window.controls.fullscreen_button.isChecked()
    assert "On" in window.controls.fullscreen_button.text()

    qtbot.keyClick(window, Qt.Key.Key_F11)
    qtbot.wait(120)
    assert not window.isFullScreen()
    assert not window.controls.fullscreen_button.isChecked()
    assert "Off" in window.controls.fullscreen_button.text()


def test_status_messages_for_playback_controls(qtbot) -> None:
    window = MainWindow(language="en")
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(120)

    window.controls.playback_button.click()
    qtbot.wait(20)
    start_status = window.controls.status_label.text().lower()
    assert "playback" in start_status
    assert "running" in start_status
    assert "fullscreen" in start_status
    assert window.controls.playback_button.isChecked()
    assert not window.controls.stop_button.isChecked()
    assert "Pause" in window.controls.playback_button.text()

    window.controls.playback_button.click()
    qtbot.wait(20)
    assert "paused" in window.controls.status_label.text().lower()
    assert "Resume" in window.controls.playback_button.text()
    assert not window.controls.playback_button.isChecked()

    window.controls.playback_button.click()
    qtbot.wait(20)
    assert "running" in window.controls.status_label.text().lower()
    assert "Pause" in window.controls.playback_button.text()

    window.controls.stop_button.click()
    qtbot.wait(20)
    assert "standstill" in window.controls.status_label.text().lower()
    assert not window.controls.playback_button.isChecked()
    assert window.controls.stop_button.isChecked()
    assert "Start" in window.controls.playback_button.text()

    # Clicking Stop again while already in standstill must not toggle visual state.
    window.controls.stop_button.click()
    qtbot.wait(20)
    assert window.controls.stop_button.isChecked()


def test_random_start_toggle_keeps_focus(qtbot) -> None:
    window = MainWindow(language="en")
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(120)

    window.controls.random_start_checkbox.setFocus()
    qtbot.wait(20)
    assert window.controls.random_start_checkbox.hasFocus()

    qtbot.keyClick(window.controls.random_start_checkbox, Qt.Key.Key_Space)
    qtbot.wait(80)
    assert window.controls.random_start_checkbox.hasFocus()
