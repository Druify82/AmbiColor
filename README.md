# AmbiColor

AmbiColor is a small, accessibility-first Windows desktop app that generates
continuous ambient color transitions.

The focus is on:
- soft, non-aggressive color changes
- perceptually pleasing transitions
- full keyboard accessibility
- screen reader compatibility (NVDA tested)
- transparent control via sliders, switches, and presets

AmbiColor is not a screensaver and not a design tool.
It is an ambient visual instrument.

---

## Current Status

This repository now includes an initial **v0.1 implementation** for:
- Preset 01 (Classic Color Cycle)
- keyboard-only operation
- screen-reader friendly labels and state text
- basic color naming tied to exact color values
- in-app preset descriptions (what each preset is intended to do)
- combined playback control (`Start` / `Pause` / `Resume`) + explicit `Stop` state

Presets 02-04 are visible in the UI but intentionally not fully implemented yet.

Color naming in v0.1 is manual:
- you can assign your own name to the currently shown HEX color
- automatic naming is planned for future versions

---

## Runtime Requirement

Primary runtime target:
- Conda environment: `devenv`
- Python: `>=3.14,<3.15` (validated against `3.14.2` in `devenv`)

---

## Run (devenv)

Run the commands from the project root `AmbiColor/` (the folder that contains `requirements.txt`).

```bash
conda activate devenv
pip install -r requirements.txt
python app/main.py
```

If `conda activate` is unreliable in your WSL setup, use:

```bash
"/mnt/c/Users/wasch/anaconda3/Scripts/conda.exe" run -n devenv python -m pip install -r requirements.txt
"/mnt/c/Users/wasch/anaconda3/Scripts/conda.exe" run -n devenv python app/main.py
```

---

## Test

```bash
conda activate devenv
pytest -q
```

Alternative (WSL + Windows conda.exe):

```bash
"/mnt/c/Users/wasch/anaconda3/Scripts/conda.exe" run -n devenv pytest -q
```

Manual NVDA acceptance is defined in `docs/TEST_NVDA.md`.

---

## Accessibility Philosophy

Accessibility is not an afterthought.

Design principles:
- All controls reachable via Tab / Shift+Tab
- All controls labeled for screen readers
- No mouse required
- No visual-only feedback
- Clear state reporting (running / paused / standstill)

---

## Documentation

- [Specification](docs/SPEC.md)
- [Roadmap](docs/ROADMAP.md)
- [Preset Calibration Notes](docs/PRESET_CALIBRATION.md)
- [NVDA Test Script](docs/TEST_NVDA.md)
- [Preset 01 Details](docs/presets/preset_01_classic_color_cycle.md)

---

## License

This project is licensed under the MIT License.
See `LICENSE` for details.
