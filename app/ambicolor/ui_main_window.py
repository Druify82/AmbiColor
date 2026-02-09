from __future__ import annotations

from PySide6.QtCore import QSignalBlocker, Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from .engine import ColorCycleEngine
from .i18n import tr
from .models import PlaybackState, PresetConfig, preset_catalog
from .ui_color_surface import ColorSurface
from .ui_controls import ControlPanel


class MainWindow(QMainWindow):
    def __init__(self, *, language: str = "en") -> None:
        super().__init__()
        self._language = language
        self._initial_focus_done = False
        self._fullscreen_enabled = False

        self.setWindowTitle(tr(self._language, "app.title"))
        self._engine = ColorCycleEngine(language=self._language)
        self._presets: list[PresetConfig] = preset_catalog()

        self._surface = ColorSurface(self)
        self.controls = ControlPanel(language=self._language, parent=self._surface)
        self.controls.setFixedWidth(420)

        overlay = QVBoxLayout(self._surface)
        overlay.setContentsMargins(16, 16, 16, 16)
        top_row = QHBoxLayout()
        top_row.addWidget(self.controls, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        top_row.addStretch(1)
        overlay.addLayout(top_row)
        overlay.addStretch(1)

        self.setCentralWidget(self._surface)
        self.showMaximized()

        self._fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
        self._fullscreen_shortcut.activated.connect(self.toggle_fullscreen)

        self._setup_presets()
        self._connect_signals()
        self._set_tab_order()
        self._sync_controls_from_engine(self._engine.current_snapshot())
        self._refresh_playback_buttons(self._engine.state)
        self._refresh_fullscreen_button()
        self._update_status()

    def _setup_presets(self) -> None:
        self.controls.preset_combo.clear()
        for preset in self._presets:
            self.controls.preset_combo.addItem(tr(self._language, preset.label_key), preset.preset_id.value)

        default_index = 0
        self.controls.preset_combo.setCurrentIndex(default_index)
        default_preset = self._presets[default_index]
        self._engine.apply_preset(default_preset)
        self._update_preset_description(default_preset)

    def _connect_signals(self) -> None:
        self.controls.preset_combo.currentIndexChanged.connect(self._on_preset_changed)

        self.controls.speed_slider.valueChanged.connect(self._on_speed_slider_changed)
        self.controls.speed_spin.valueChanged.connect(self._on_speed_spin_changed)

        self.controls.saturation_slider.valueChanged.connect(self._on_saturation_slider_changed)
        self.controls.saturation_spin.valueChanged.connect(self._on_saturation_spin_changed)

        self.controls.brightness_slider.valueChanged.connect(self._on_brightness_slider_changed)
        self.controls.brightness_spin.valueChanged.connect(self._on_brightness_spin_changed)

        self.controls.random_start_checkbox.toggled.connect(self._on_random_start_toggled)

        self.controls.playback_button.clicked.connect(self._on_playback_clicked)
        self.controls.stop_button.clicked.connect(self._on_stop_clicked)
        self.controls.fullscreen_button.clicked.connect(
            lambda: self._invoke_action(self.controls.fullscreen_button, self.toggle_fullscreen)
        )

        self.controls.save_name_button.clicked.connect(self._save_color_name)
        self.controls.color_name_input.returnPressed.connect(self._save_color_name)

        self._engine.color_changed.connect(self._on_color_changed)
        self._engine.state_changed.connect(self._on_state_changed)
        self._engine.params_changed.connect(self._sync_controls_from_engine)

    def _set_tab_order(self) -> None:
        order = [
            self.controls.preset_combo,
            self.controls.preset_description_edit,
            self.controls.speed_slider,
            self.controls.speed_spin,
            self.controls.saturation_slider,
            self.controls.saturation_spin,
            self.controls.brightness_slider,
            self.controls.brightness_spin,
            self.controls.random_start_checkbox,
            self.controls.playback_button,
            self.controls.stop_button,
            self.controls.fullscreen_button,
            self.controls.color_name_input,
            self.controls.save_name_button,
        ]

        for idx in range(len(order) - 1):
            self.setTabOrder(order[idx], order[idx + 1])

    def _on_preset_changed(self, index: int) -> None:
        if index < 0 or index >= len(self._presets):
            return
        preset = self._presets[index]
        self._engine.apply_preset(preset)
        self._update_preset_description(preset)
        if not preset.implemented:
            preset_name = tr(self._language, preset.label_key)
            self._update_status(note=tr(self._language, "status.preset_fallback", preset=preset_name))
            return
        self._update_status()

    def _on_speed_slider_changed(self, value: int) -> None:
        with QSignalBlocker(self.controls.speed_spin):
            self.controls.speed_spin.setValue(float(value))
        self._engine.set_cycle_duration(float(value))

    def _on_speed_spin_changed(self, value: float) -> None:
        ivalue = int(round(value))
        with QSignalBlocker(self.controls.speed_slider):
            self.controls.speed_slider.setValue(ivalue)
        self._engine.set_cycle_duration(float(ivalue))

    def _on_saturation_slider_changed(self, value: int) -> None:
        with QSignalBlocker(self.controls.saturation_spin):
            self.controls.saturation_spin.setValue(float(value))
        self._engine.set_saturation(value)

    def _on_saturation_spin_changed(self, value: float) -> None:
        ivalue = int(round(value))
        with QSignalBlocker(self.controls.saturation_slider):
            self.controls.saturation_slider.setValue(ivalue)
        self._engine.set_saturation(ivalue)

    def _on_brightness_slider_changed(self, value: int) -> None:
        with QSignalBlocker(self.controls.brightness_spin):
            self.controls.brightness_spin.setValue(float(value))
        self._engine.set_brightness(value)

    def _on_brightness_spin_changed(self, value: float) -> None:
        ivalue = int(round(value))
        with QSignalBlocker(self.controls.brightness_slider):
            self.controls.brightness_slider.setValue(ivalue)
        self._engine.set_brightness(ivalue)

    def _save_color_name(self) -> None:
        snapshot = self._engine.current_snapshot()
        entered_name = self.controls.color_name_input.text().strip()
        self._engine.set_hue_name(snapshot["hex"], entered_name)
        if entered_name:
            note = tr(self._language, "status.color_name_saved", name=entered_name, hex_color=snapshot["hex"])
        else:
            note = tr(self._language, "status.color_name_cleared", hex_color=snapshot["hex"])
        self._update_status(note=note)

    def _on_color_changed(self, color, _hex: str, display_name: str) -> None:
        self._surface.set_color(color)
        self.controls.set_current_color_text(display_name)

    def _on_state_changed(self, text: str) -> None:
        del text
        self._update_status()
        self._refresh_playback_buttons(self._engine.state)

    def _refresh_playback_buttons(self, state: PlaybackState) -> None:
        self.controls.stop_button.setEnabled(True)
        if state == PlaybackState.STANDSTILL:
            playback_label = tr(self._language, "button.start")
        elif state == PlaybackState.RUNNING:
            playback_label = tr(self._language, "button.pause")
        else:
            playback_label = tr(self._language, "button.resume")

        self.controls.playback_button.setText(playback_label)
        self.controls.playback_button.setAccessibleName(playback_label)
        self.controls.playback_button.setAccessibleDescription(
            f"Playback control, action: {playback_label.lower()}"
        )

        # "Checked" represents active playback only. Paused should not look active.
        self.controls.playback_button.setChecked(state == PlaybackState.RUNNING)
        self.controls.stop_button.setChecked(state == PlaybackState.STANDSTILL)
        self.controls.playback_button.setCheckable(True)
        self.controls.stop_button.setAccessibleDescription(
            f"Playback control, active: {self.controls.stop_button.isChecked()}"
        )

    def _sync_controls_from_engine(self, snapshot: dict) -> None:
        with QSignalBlocker(self.controls.speed_slider):
            self.controls.speed_slider.setValue(int(round(snapshot["cycle_duration_s"])))
        with QSignalBlocker(self.controls.speed_spin):
            self.controls.speed_spin.setValue(float(snapshot["cycle_duration_s"]))

        with QSignalBlocker(self.controls.saturation_slider):
            self.controls.saturation_slider.setValue(int(snapshot["saturation_pct"]))
        with QSignalBlocker(self.controls.saturation_spin):
            self.controls.saturation_spin.setValue(float(snapshot["saturation_pct"]))

        with QSignalBlocker(self.controls.brightness_slider):
            self.controls.brightness_slider.setValue(int(snapshot["brightness_pct"]))
        with QSignalBlocker(self.controls.brightness_spin):
            self.controls.brightness_spin.setValue(float(snapshot["brightness_pct"]))

        with QSignalBlocker(self.controls.random_start_checkbox):
            self.controls.random_start_checkbox.setChecked(bool(snapshot["random_start_hue"]))

        if not self.controls.status_label.text():
            self._update_status(note=tr(self._language, "status.ready"))

    def _on_random_start_toggled(self, checked: bool) -> None:
        self._engine.set_random_start_hue(checked)
        note_key = "status.random_start_on" if checked else "status.random_start_off"
        self._update_status(note=tr(self._language, note_key))
        self._focus_later(self.controls.random_start_checkbox)

    def _on_playback_clicked(self) -> None:
        state = self._engine.state
        if state == PlaybackState.STANDSTILL:
            self._engine.start()
        elif state == PlaybackState.RUNNING:
            self._engine.pause()
        else:
            self._engine.resume()
        self._focus_later(self.controls.playback_button)

    def _on_stop_clicked(self) -> None:
        previous_state = self._engine.state
        self._engine.stop_standstill()
        if self._engine.state == previous_state:
            # Prevent visual toggle changes when stop does not cause a state transition.
            self._refresh_playback_buttons(self._engine.state)
        self._focus_later(self.controls.stop_button)

    def _invoke_action(self, source_widget: QWidget, action) -> None:
        action()
        if source_widget.isEnabled():
            self._focus_later(source_widget)

    def _focus_later(self, widget: QWidget) -> None:
        QTimer.singleShot(0, widget.setFocus)

    def _update_status(self, note: str | None = None) -> None:
        playback_text = tr(self._language, f"state.{self._engine.state.value}")
        fullscreen_text = tr(self._language, "status.on" if self._fullscreen_enabled else "status.off")
        status_text = tr(
            self._language,
            "status.combined",
            playback=playback_text,
            fullscreen=fullscreen_text,
        )
        if note:
            status_text = f"{status_text}. {note}"
        self.controls.set_status(status_text)
        self._refresh_fullscreen_button()

    def _update_preset_description(self, preset: PresetConfig) -> None:
        self.controls.set_preset_description(tr(self._language, preset.description_key))

    def _refresh_fullscreen_button(self) -> None:
        self.controls.fullscreen_button.setChecked(self._fullscreen_enabled)
        fullscreen_key = "button.fullscreen_on" if self._fullscreen_enabled else "button.fullscreen_off"
        button_text = tr(self._language, fullscreen_key)
        self.controls.fullscreen_button.setText(button_text)
        self.controls.fullscreen_button.setAccessibleName(button_text)
        self.controls.fullscreen_button.setAccessibleDescription(
            f"Toggle fullscreen mode, active: {self.controls.fullscreen_button.isChecked()}"
        )

    def toggle_fullscreen(self) -> None:
        focus_widget = self.focusWidget()

        if self.isFullScreen():
            self.showMaximized()
            self._fullscreen_enabled = False
            self._update_status(note=tr(self._language, "status.fullscreen_off"))
        else:
            self.showFullScreen()
            self._fullscreen_enabled = True
            self._update_status(note=tr(self._language, "status.fullscreen_on"))

        if focus_widget is not None:
            QTimer.singleShot(0, focus_widget.setFocus)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        if not self._initial_focus_done:
            self._initial_focus_done = True
            QTimer.singleShot(0, self.controls.preset_combo.setFocus)
