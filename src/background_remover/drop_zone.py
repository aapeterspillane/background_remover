"""Drag-and-drop widget for image files."""

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from background_remover.image_processor import ImageProcessor


class DropZone(QFrame):
    """A widget that accepts dropped image files."""

    files_dropped = Signal(list)  # list[Path]

    NORMAL_STYLE = """
        DropZone {
            border: 2px dashed #aaaaaa;
            border-radius: 10px;
            background-color: #f5f5f5;
        }
    """

    HOVER_STYLE = """
        DropZone {
            border: 2px dashed #4a90d9;
            border-radius: 10px;
            background-color: #e3f2fd;
        }
    """

    def __init__(self, parent=None):
        """Initialize the drop zone."""
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumHeight(150)
        self._setup_ui()
        self.setStyleSheet(self.NORMAL_STYLE)

    def _setup_ui(self):
        """Set up the widget layout."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._label = QLabel("Drop images here\nor click 'Add Files' to browse")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet("color: #666666; font-size: 14px;")
        layout.addWidget(self._label)

        formats = ", ".join(
            ext.upper() for ext in sorted(ImageProcessor.SUPPORTED_FORMATS)
        )
        self._format_label = QLabel(f"Supported: {formats}")
        self._format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._format_label.setStyleSheet("color: #999999; font-size: 11px;")
        layout.addWidget(self._format_label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter - check if we can accept the data."""
        if event.mimeData().hasUrls():
            # Check if any URL is a valid image
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    path = Path(url.toLocalFile())
                    if ImageProcessor.is_supported_format(path):
                        event.acceptProposedAction()
                        self.setStyleSheet(self.HOVER_STYLE)
                        return
        event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        """Handle drag leave - reset styling."""
        self.setStyleSheet(self.NORMAL_STYLE)

    def dropEvent(self, event: QDropEvent):
        """Handle drop - emit signal with valid image paths."""
        self.setStyleSheet(self.NORMAL_STYLE)

        valid_files = []
        for url in event.mimeData().urls():
            if url.isLocalFile():
                path = Path(url.toLocalFile())
                if path.is_file() and ImageProcessor.is_supported_format(path):
                    valid_files.append(path)

        if valid_files:
            event.acceptProposedAction()
            self.files_dropped.emit(valid_files)
        else:
            event.ignore()
