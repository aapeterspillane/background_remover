"""Splash screen with progress indicator for app startup."""

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class ModelLoaderThread(QThread):
    """Background thread to pre-load the rembg model."""

    progress = Signal(int, str)  # progress value, status message
    finished = Signal(object)  # passes the loaded processor

    def run(self):
        """Load the model in background."""
        self.progress.emit(10, "Initializing...")

        # Import here to avoid slow import at app start
        self.progress.emit(30, "Loading libraries...")
        from background_remover.image_processor import ImageProcessor

        self.progress.emit(50, "Loading AI model (first run downloads ~176MB)...")

        # Create processor and trigger model load
        processor = ImageProcessor()

        self.progress.emit(70, "Initializing AI model...")
        # Access session property to trigger lazy load
        _ = processor.session

        self.progress.emit(100, "Ready!")
        self.finished.emit(processor)


class SplashScreen(QWidget):
    """Splash screen shown during app initialization."""

    startup_complete = Signal(object)  # emits the pre-loaded processor

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._loader_thread = None

    def _setup_ui(self):
        """Set up the splash screen UI."""
        self.setWindowTitle("Background Remover")
        self.setFixedSize(400, 200)

        # Remove window frame, keep on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        # Center on screen
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #ffffff;
            }
            QLabel#status {
                font-size: 13px;
                color: #aaaaaa;
            }
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #404040;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # App title
        title = QLabel("Background Remover")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addStretch()

        # Status label
        self._status_label = QLabel("Starting...")
        self._status_label.setObjectName("status")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status_label)

        # Progress bar
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(False)
        layout.addWidget(self._progress_bar)

        layout.addStretch()

    def start_loading(self):
        """Start loading the model in background."""
        self._loader_thread = ModelLoaderThread()
        self._loader_thread.progress.connect(self._on_progress)
        self._loader_thread.finished.connect(self._on_finished)
        self._loader_thread.start()

    def _on_progress(self, value: int, message: str):
        """Update progress display."""
        self._progress_bar.setValue(value)
        self._status_label.setText(message)
        QApplication.processEvents()

    def _on_finished(self, processor):
        """Called when loading is complete."""
        self.startup_complete.emit(processor)

    def center_on_screen(self):
        """Center the splash screen on the primary screen."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
