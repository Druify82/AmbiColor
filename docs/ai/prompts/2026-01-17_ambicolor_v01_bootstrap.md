# Codex Prompt – AmbiColor v0.1 Bootstrap

## Date
2026-01-17

## Context
This prompt initializes the first working prototype of AmbiColor v0.1.

The authoritative specification is defined in:
- docs/SPEC.md
- docs/TEST_NVDA.md
- docs/presets/preset_01_classic_color_cycle.md

Accessibility and keyboard-only usability are mandatory.

---

## Objective
Create a minimal but functional desktop application prototype that:

- runs on Windows 11
- displays a single full-window color
- implements Preset 01 (Classic Color Cycle)
- provides a keyboard-accessible UI skeleton
- is screen-reader friendly (NVDA)

This is an alpha prototype, not a finished product.

---

## Technical Constraints
- Preferred language: Python
- Preferred UI toolkit: Qt via PySide6
- No mouse interaction required
- No external services
- No persistence required in this step

---

## Required Features (v0.1 – Step 1)
- Main window (maximized)
- Color fills entire window
- Hue rotates continuously (HSV model)
- Fixed saturation and brightness (configurable via UI)
- Start / Pause / Resume / Stop buttons
- Speed control (seconds per full cycle)

---

## Accessibility Requirements
- All controls reachable via Tab / Shift+Tab
- All controls have accessible labels
- State changes are announced (running / paused / standstill)
- No visual-only feedback

---

## Non-Goals
- No gradients or spatial effects
- No preset import/export
- No advanced timing curves

---

## Output Expectations
- Project folder structure under `app/`
- Clear separation between UI code and logic
- Readable, commented code
- Application must start without errors

---

## Notes
If any requirement is unclear, ask for clarification instead of guessing.
