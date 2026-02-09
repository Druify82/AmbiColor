from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from ambicolor.ui_main_window import MainWindow


def main() -> int:
    if not ((3, 14) <= sys.version_info[:2] < (3, 15)):
        raise RuntimeError(
            "AmbiColor v0.1 requires Python >=3.14 and <3.15 "
            f"(current: {sys.version.split()[0]})."
        )

    app = QApplication(sys.argv)
    window = MainWindow(language="en")
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
