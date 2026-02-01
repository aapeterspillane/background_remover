"""Qt application setup."""

import sys

from PySide6.QtWidgets import QApplication

from background_remover.main_window import MainWindow


def run_app() -> int:
    """Initialize and run the Qt application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Background Remover")
    app.setApplicationVersion("1.0.0")

    window = MainWindow()
    window.show()

    return app.exec()
