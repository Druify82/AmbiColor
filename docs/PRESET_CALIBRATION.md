# AmbiColor – Preset Calibration Notes (v0.1.x)

This document defines the current preset tuning pass and how to review it.

The goal is not to finish all advanced preset logic yet, but to make each preset
feel intentional and predictable even with the current linear engine.

---

## Why This Exists

Some preset transitions can feel different from expectation, especially for:
- Natural / Artistic
- Ambient Lamp

In v0.1, presets 02-04 are still marked as not fully implemented.
However, we can still calibrate their baseline parameters now.

---

## Current Calibration Baseline

| Preset | Duration (s) | Saturation (%) | Brightness (%) | Hue Range |
|---|---:|---:|---:|---|
| Classic Color Cycle | 120 | 80 | 60 | 0° to 360° |
| Ambient Lamp (Soft) | 210 | 35 | 42 | 25° to 205° |
| Spectrum Sweep (Numeric) | 75 | 95 | 68 | 0° to 360° |
| Natural / Artistic Logic | 300 | 48 | 52 | 18° to 95° |

Interpretation:
- Ambient Lamp avoids strong neon regions and runs slower.
- Spectrum Sweep is intentionally technical and wider/faster.
- Natural / Artistic (v0.1 placeholder) now uses smooth bounded motion without hard wrap jumps.

---

## Latest User Feedback Snapshot

The following scores and comments are the current reference for this calibration cycle:

| Preset | Smoothness | Calmness | Concept Match | Notes |
|---|---:|---:|---:|---|
| Classic | 5/5 | 5/5 | 5/5 | Matches expectation exactly; intentionally slow by concept. |
| Ambient Lamp (Soft) | 5/5 | 5/5 | 3/5 | Expected concept unclear; appears cooler and less varied. |
| Spectrum Sweep (Numeric) | 5/5 | 4/5 | 4/5 | Stronger than Classic; acceptable but concept should be clearer. |
| Natural / Artistic | 2/5 | 2/5 | 1/5 | Previous edge/kink between green and beige; concept unclear as mixed theme. |

Actions applied in this iteration:
- Added in-app preset descriptions (what it does and why it is named this way).
- Reworked bounded-range hue motion to bounce at edges instead of hard wrapping.
- Marked Natural/Artistic as an explicit v0.1 blend placeholder.

---

## Review Procedure (Manual)

1. Start app in `AmbiColor/`:
   - `conda activate devenv`
   - `python app/main.py`
2. For each preset, observe at least 60 seconds.
3. Rate each preset in 3 categories:
   - Smoothness (1-5)
   - Calmness (1-5)
   - Match to expected concept (1-5)
4. Add short notes:
   - What felt wrong?
   - Which color region felt too aggressive or too dull?
   - Should duration be faster/slower?

---

## Expected v0.1 Constraints

Still out of scope in this pass:
- Non-linear timing curves
- Multi-phase palette choreography
- Adaptive transitions

These remain roadmap items and should not block baseline tuning.

---

## Next Iteration Plan

After one manual review round, we tune per preset in this order:
1. Hue range
2. Saturation
3. Brightness
4. Cycle duration

This keeps changes understandable and avoids overfitting.
