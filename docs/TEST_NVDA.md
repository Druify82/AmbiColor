# AmbiColor v0.1 – NVDA & Keyboard Test Script

## Environment

- Windows 11
- NVDA (latest stable)
- No mouse usage

---

## 1. Startup

- Application launches without focus loss
- Initial focus is on first meaningful control
- NVDA announces application name and role

---

## 2. Navigation

- Tab moves forward through all controls
- Shift+Tab moves backward
- No focus traps
- Logical order:
  Preset → Speed → Color parameters → Start/Pause/Stop

---

## 3. Preset Selection

- Preset list announced correctly
- Changing preset announces new selection
- Default preset is “Classic Color Cycle”

---

## 4. Playback Control

- Start announces “running”
- Pause announces “paused”
- Resume announces “running”
- Stop announces “standstill”

---

## 5. Speed Control

- Numeric value announced
- Slider movement announced
- Changes affect color timing audibly (logical feedback)

---

## 6. Color Parameters

- Numeric changes announced
- Changes reflected immediately in behavior
- No silent state changes

---

## 7. Full-Screen / Maximized Mode

- Toggle reachable via keyboard
- Mode change announced
- Focus preserved

---

## 8. Failure Conditions

v0.1 fails if:
- Any control is unreachable by keyboard
- Any control is unlabeled
- State changes are silent
- App requires mouse input
