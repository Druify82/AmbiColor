# AmbiColor

AmbiColor is a small, accessibility-first Windows application that generates
continuous ambient color transitions on the screen.

The focus is on:
- soft, non-aggressive color changes
- perceptually pleasing transitions
- full keyboard accessibility
- screen reader compatibility (NVDA tested)
- simple, transparent control via sliders, switches, and presets

AmbiColor is not a screensaver and not a design tool.
It is an ambient visual instrument.

The name “AmbiColor” is a deliberate wordplay:
ambient + ambiguity / ambivalence.

---

## Target Use

- Decorative ambient light on monitors or TVs
- Calm background visuals without distraction
- Accessible use for blind and visually impaired users
- Exploration of color perception and rhythm

---

## Version Scope

This repository currently defines **AmbiColor v0.1**.

v0.1 focuses on:
- full-screen or maximized window color display
- continuous color cycling
- a small set of well-defined presets
- basic customization of those presets
- strict keyboard and screen reader usability

More advanced visual effects are explicitly deferred
(see `ROADMAP.md`).

---

## Accessibility Philosophy

Accessibility is not an afterthought.

Design principles:
- All controls reachable via Tab / Shift+Tab
- All controls labeled for screen readers
- No mouse required
- No visual-only feedback
- Clear value reporting (numbers, names, states)

---

## Files Overview

- `SPEC.md` – formal specification of AmbiColor v0.1
- `TEST_NVDA.md` – acceptance tests for keyboard and NVDA usage
- `ROADMAP.md` – features planned beyond v0.1
- `presets/` – documentation of built-in presets

---

## Status

This project is currently in the **specification phase**.
Implementation is expected to be generated with AI assistance
and iterated through structured testing.

## Documentation
- [Specification](docs/SPEC.md)
- [Roadmap](docs/ROADMAP.md)
- [NVDA Test Script](docs/TEST_NVDA.md)
