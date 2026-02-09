# Preset 01 – Classic Color Cycle

## Purpose

This preset reproduces the behavior of classic decorative
RGB color-changing lamps (orbs, eggs, globes).

It serves as the **baseline reference** for AmbiColor.
If this preset does not feel correct, all other presets are invalid.

---

## Conceptual Model

The color changes continuously by rotating through the hue dimension
of a circular color space.

- Brightness remains constant
- Saturation remains constant
- Only the hue changes over time

There are:
- no jumps
- no flashing
- no dark phases
- no aggressive neon colors

---

## Color Model

- Primary model: HSV (or equivalent)
- Hue: circular, continuous (0° → 360° → 0°)
- Saturation: fixed
- Brightness / Value: fixed

Internal interpolation must avoid muddy transitions.

---

## Default Parameters

| Parameter        | Default Value | Notes |
|------------------|---------------|-------|
| Saturation       | 80 %          | High, but not neon |
| Brightness       | 60 %          | Comfortable in dark rooms |
| Cycle Duration   | 120 seconds   | One full hue rotation |
| Start Hue        | Random        | Optional toggle |
| Loop Mode        | Infinite      | No automatic stop |

---

## Playback Behavior

- The cycle runs continuously until paused or stopped
- Pausing freezes the current color
- Stopping enters standstill mode at the current color

There is no automatic reset unless explicitly triggered.

---

## User Controls (v0.1)

Mandatory controls for this preset:

- Start
- Pause
- Resume
- Stop (standstill)
- Cycle duration (seconds)
- Saturation (percentage)
- Brightness (percentage)
- Toggle: random start hue

All controls must be accessible via keyboard.

---

## Accessibility Expectations

- Screen reader announces:
  - current state (running / paused / standstill)
  - numeric parameter values when changed
- No visual-only feedback
- No mouse interaction required

---

## Visual Expectations

Qualitative expectations:

- Colors change smoothly and predictably
- No flicker
- No visible stepping
- Transitions feel calm and ornamental

This preset should immediately evoke recognition:
“this behaves like a classic color-changing lamp”.

---

## Test Reference

This preset is used as the primary reference for:

- timing accuracy
- smoothness of transitions
- correctness of pause/standstill behavior
- accessibility testing

All other presets build on this one.
