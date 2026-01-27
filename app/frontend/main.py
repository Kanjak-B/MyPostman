from __future__ import annotations

import sys
from pathlib import Path

from PySide6 import QtWidgets

from app.frontend.ui.main_window import MainWindow


def load_stylesheet() -> str:
    style_path = Path(__file__).resolve().parent / "assets" / "style.qss"
    if style_path.exists():
        return style_path.read_text(encoding="utf-8")
    return ""


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
