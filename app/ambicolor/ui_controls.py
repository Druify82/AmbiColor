from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from .i18n import tr


class ControlPanel(QWidget):
    def __init__(self, language: str = "en", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self.setObjectName("controlPanel")
        self.setAccessibleName("AmbiColor Control Panel")
        self.setStyleSheet(
            "#controlPanel {"
            "background-color: rgba(15, 15, 15, 200);"
            "border: 1px solid rgba(255, 255, 255, 80);"
            "border-radius: 8px;"
            "color: white;"
            "}"
            "QLabel { color: white; }"
            "QGroupBox { color: white; font-weight: bold; }"
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        preset_box = QGroupBox(tr(self._language, "label.preset"), self)
        preset_layout = QVBoxLayout(preset_box)
        self.preset_combo = QComboBox(preset_box)
        self.preset_combo.setAccessibleName(tr(self._language, "label.preset"))
        self.preset_combo.setAccessibleDescription("Select color transition preset")
        self.preset_description_edit = QPlainTextEdit(preset_box)
        self.preset_description_edit.setReadOnly(True)
        self.preset_description_edit.setPlainText("-")
        self.preset_description_edit.setMinimumHeight(88)
        self.preset_description_edit.setAccessibleName(tr(self._language, "label.preset_description"))
        self.preset_description_edit.setAccessibleDescription("Read-only preset explanation")
        preset_layout.addWidget(self.preset_combo)
        preset_layout.addWidget(self.preset_description_edit)
        root.addWidget(preset_box)

        speed_box = QGroupBox(tr(self._language, "label.speed"), self)
        speed_layout = QGridLayout(speed_box)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal, speed_box)
        self.speed_slider.setRange(5, 600)
        self.speed_slider.setAccessibleName(tr(self._language, "label.speed"))
        self.speed_slider.setAccessibleDescription("Adjust cycle duration in seconds")
        self.speed_spin = QDoubleSpinBox(speed_box)
        self.speed_spin.setRange(5, 600)
        self.speed_spin.setDecimals(0)
        self.speed_spin.setSuffix(" s")
        self.speed_spin.setAccessibleName(tr(self._language, "label.speed"))
        self.speed_spin.setAccessibleDescription("Cycle duration numeric input")
        speed_layout.addWidget(self.speed_slider, 0, 0)
        speed_layout.addWidget(self.speed_spin, 0, 1)
        root.addWidget(speed_box)

        color_box = QGroupBox("Color Parameters", self)
        color_layout = QGridLayout(color_box)

        sat_label = QLabel(tr(self._language, "label.saturation"), color_box)
        self.saturation_slider = QSlider(Qt.Orientation.Horizontal, color_box)
        self.saturation_slider.setRange(0, 100)
        self.saturation_slider.setAccessibleName(tr(self._language, "label.saturation"))
        self.saturation_slider.setAccessibleDescription("Adjust saturation percentage")
        self.saturation_spin = QDoubleSpinBox(color_box)
        self.saturation_spin.setRange(0, 100)
        self.saturation_spin.setDecimals(0)
        self.saturation_spin.setSuffix(" %")
        self.saturation_spin.setAccessibleName(tr(self._language, "label.saturation"))
        self.saturation_spin.setAccessibleDescription("Saturation numeric input")

        bri_label = QLabel(tr(self._language, "label.brightness"), color_box)
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal, color_box)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setAccessibleName(tr(self._language, "label.brightness"))
        self.brightness_slider.setAccessibleDescription("Adjust brightness percentage")
        self.brightness_spin = QDoubleSpinBox(color_box)
        self.brightness_spin.setRange(0, 100)
        self.brightness_spin.setDecimals(0)
        self.brightness_spin.setSuffix(" %")
        self.brightness_spin.setAccessibleName(tr(self._language, "label.brightness"))
        self.brightness_spin.setAccessibleDescription("Brightness numeric input")

        self.random_start_checkbox = QCheckBox(tr(self._language, "label.random_start"), color_box)
        self.random_start_checkbox.setAccessibleName(tr(self._language, "label.random_start"))
        self.random_start_checkbox.setAccessibleDescription("Enable random hue on start")

        color_layout.addWidget(sat_label, 0, 0)
        color_layout.addWidget(self.saturation_slider, 0, 1)
        color_layout.addWidget(self.saturation_spin, 0, 2)
        color_layout.addWidget(bri_label, 1, 0)
        color_layout.addWidget(self.brightness_slider, 1, 1)
        color_layout.addWidget(self.brightness_spin, 1, 2)
        color_layout.addWidget(self.random_start_checkbox, 2, 0, 1, 3)
        root.addWidget(color_box)

        playback_box = QGroupBox(tr(self._language, "label.playback"), self)
        playback_layout = QHBoxLayout(playback_box)
        self.playback_button = QPushButton(tr(self._language, "button.start"), playback_box)
        self.stop_button = QPushButton(tr(self._language, "button.stop"), playback_box)
        self.stop_button.setCheckable(True)

        for button in (self.playback_button, self.stop_button):
            button.setAccessibleName(button.text())
            button.setAccessibleDescription("Playback control")
            playback_layout.addWidget(button)
        root.addWidget(playback_box)

        self.fullscreen_button = QPushButton(tr(self._language, "button.toggle_fullscreen"), self)
        self.fullscreen_button.setCheckable(True)
        self.fullscreen_button.setAccessibleName(tr(self._language, "button.toggle_fullscreen"))
        self.fullscreen_button.setAccessibleDescription("Toggle fullscreen mode")
        root.addWidget(self.fullscreen_button)

        naming_box = QGroupBox(tr(self._language, "label.color_name"), self)
        naming_layout = QGridLayout(naming_box)

        current_title = QLabel(tr(self._language, "label.current_color"), naming_box)
        self.current_color_label = QLabel("-", naming_box)
        self.current_color_label.setAccessibleName(tr(self._language, "label.current_color"))

        self.color_name_input = QLineEdit(naming_box)
        self.color_name_input.setPlaceholderText(tr(self._language, "placeholder.color_name"))
        self.color_name_input.setAccessibleName(tr(self._language, "label.color_name"))
        self.color_name_input.setAccessibleDescription("Type a custom name for current color")

        self.save_name_button = QPushButton(tr(self._language, "button.save_name"), naming_box)
        self.save_name_button.setAccessibleName(tr(self._language, "button.save_name"))
        self.save_name_button.setAccessibleDescription("Save custom color name")
        self.color_name_help_label = QLabel(tr(self._language, "label.color_name_help"), naming_box)
        self.color_name_help_label.setWordWrap(True)
        self.color_name_help_label.setAccessibleName(tr(self._language, "label.color_name_help"))

        naming_layout.addWidget(current_title, 0, 0)
        naming_layout.addWidget(self.current_color_label, 0, 1)
        naming_layout.addWidget(self.color_name_input, 1, 0)
        naming_layout.addWidget(self.save_name_button, 1, 1)
        naming_layout.addWidget(self.color_name_help_label, 2, 0, 1, 2)
        root.addWidget(naming_box)

        status_box = QFrame(self)
        status_layout = QVBoxLayout(status_box)
        status_title = QLabel(tr(self._language, "label.status"), status_box)
        self.status_label = QLabel(tr(self._language, "status.ready"), status_box)
        self.status_label.setWordWrap(True)
        self.status_label.setAccessibleName(tr(self._language, "label.status"))
        self.status_label.setAccessibleDescription("Current playback and mode state")
        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_label)
        root.addWidget(status_box)

        root.addStretch(1)

    def set_status(self, text: str) -> None:
        self.status_label.setText(text)

    def set_current_color_text(self, text: str) -> None:
        self.current_color_label.setText(text)

    def set_preset_description(self, text: str) -> None:
        self.preset_description_edit.setPlainText(text)
