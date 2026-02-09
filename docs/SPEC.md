# AmbiColor – Specification v0.1

## 1. Purpose

AmbiColor generates continuous ambient color transitions
displayed as a full-screen or maximized window.

It must be usable without sight and without a mouse.

---

## 2. Platform

- Operating System: Windows 11
- Primary implementation target: desktop application
- Programming language and toolkit are implementation details
  (recommended: Python + Qt / PySide)

---

## 3. Display Modes

- Maximized window (default)
- Full-screen mode (toggleable)

The entire window is filled with a single color at any given time
(v0.1 does NOT include spatial patterns).

---

## 4. Color Models

Supported color representations (input/output):

- RGB (0–255)
- HEX (#RRGGBB)
- HSL / HSV (degrees, percentages)

Internal interpolation should be perceptually smooth.
(Exact model left to implementation, but must avoid muddy transitions.)

---

## 5. Preset System

### 5.1 Preset Philosophy

Presets provide **reliable starting points**.
They must always be customizable.

Presets are not locked modes.

---

### 5.2 Preset 01 – Classic Color Cycle (Baseline)

**Name:** Classic Color Cycle  
**Concept:** Emulates classic RGB color-changing decorative lamps.

**Logic:**
- Hue rotates continuously from 0° to 360°
- Saturation: fixed
- Brightness / Lightness: fixed

**Default values:**
- Saturation: 80%
- Brightness: 60%
- Cycle duration: 120 seconds per full rotation
- Start hue: random (optional toggle)

**Controls:**
- Start / Pause
- Resume
- Stop on current color (standstill mode)

This preset is the reference baseline for all testing.

---

### 5.3 Preset 02 – Ambient Lamp (Soft)

- Reduced saturation and brightness
- Restricted hue range
- Designed to avoid aggressive or neon colors

---

### 5.4 Preset 03 – Spectrum Sweep (Numeric)

- Linear, technical traversal through the color space
- Intended for testing and debugging perception

---

### 5.5 Preset 04 – Natural / Artistic Logic

- Predefined palette with internal order
- Optional non-linear timing curve
- Inspired by natural light changes (sunset, dusk)

---

## 6. Timing & Speed Control

Speed must be adjustable via:

- Seconds per full cycle
- Optional BPM-based interpretation (color change rhythm)

Advanced curves (acceleration/deceleration) are optional but allowed
within v0.1 if simple.

---

## 7. Controls & UI Requirements

### 7.1 Mandatory Controls

- Preset selection (list or combo box)
- Start
- Pause
- Resume
- Stop / Standstill
- Speed control (numeric + slider)
- Color parameter controls (depending on preset)

### 7.2 Accessibility Rules

- All controls reachable by Tab / Shift+Tab
- Logical tab order
- Screen reader-readable labels
- Clear state announcements (e.g. “paused”, “running”)

---

## 8. Color Naming (v0.1 Minimal)

- Users may assign custom names to colors
- Color values and names must stay synchronized
- Automatic naming is NOT required in v0.1

---

## 9. Non-Goals for v0.1

Explicitly excluded:
- Spatial effects (waves, gradients)
- Sequencer matrices
- External hardware control
- Audio synchronization
- Preset import/export

(See `ROADMAP.md`.)

---

## 10. Acceptance Criterion

AmbiColor v0.1 is complete when:

- Preset 01 behaves identically to classic color-cycle lamps
- All functions are usable with keyboard only
- NVDA reports all controls meaningfully
- No visual-only state exists
