# ADR-0001: UI Toolkit Selection

## Status
Accepted

## Date
2026-01-17

## Context
AmbiColor requires a desktop UI that is:

- keyboard accessible
- screen reader compatible (NVDA)
- suitable for continuous visual updates
- well supported on Windows 11

The UI must be generatable and maintainable with AI assistance.

---

## Decision
We use **Python with Qt (PySide6)** as the primary UI framework.

---

## Rationale
- Qt widgets expose accessible names and roles
- Keyboard navigation is robust and predictable
- Python enables rapid prototyping with AI-generated code
- PySide6 is actively maintained and Windows-friendly

---

## Consequences
Positive:
- Fast iteration
- Good accessibility baseline
- Clear separation of UI and logic

Negative:
- Application size larger than native Win32
- Requires Python runtime or packaging step later

---

## Alternatives Considered
- C# / WPF (rejected: higher complexity, slower AI iteration)
- Electron (rejected: accessibility overhead, resource usage)
- Tkinter (rejected: accessibility inconsistencies)

---

## Notes
This decision may be revisited in future versions,
but v0.1 is locked to this choice.
