"""Qt application setup."""

import sys

from PySide6.QtWidgets import QApplication

from background_remover.splash_screen import SplashScreen


def run_app() -> int:
    """Initialize and run the Qt application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Background Remover")
    app.setApplicationVersion("1.1.0")

    # Show splash screen and load model in background
    splash = SplashScreen()
    splash.center_on_screen()
    splash.show()
    app.processEvents()

    # Store reference to main window (created after model loads)
    main_window = None

    def on_startup_complete(processor):
        nonlocal main_window
        # Import here to avoid slow import before splash shows
        from background_remover.main_window import MainWindow

        main_window = MainWindow(processor)
        main_window.show()
        splash.close()

    splash.startup_complete.connect(on_startup_complete)
    splash.start_loading()

    return app.exec()
