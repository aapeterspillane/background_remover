"""Progress dialog for batch processing feedback."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class ProgressDialog(QDialog):
    """Dialog showing progress during batch image processing."""

    cancel_requested = Signal()

    def __init__(self, total_files: int, parent=None):
        """
        Initialize the progress dialog.

        Args:
            total_files: Total number of files to process.
            parent: Parent widget.
        """
        super().__init__(parent)
        self._total = total_files
        self._cancelled = False
        self._setup_ui()

    def _setup_ui(self):
        """Set up the dialog layout."""
        self.setWindowTitle("Processing Images")
        self.setMinimumWidth(450)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Status label
        self._status_label = QLabel("Preparing...")
        self._status_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self._status_label)

        # Progress bar
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, self._total)
        self._progress_bar.setValue(0)
        layout.addWidget(self._progress_bar)

        # Progress text
        self._progress_label = QLabel(f"0 / {self._total}")
        self._progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._progress_label)

        # Log area
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setMaximumHeight(150)
        layout.addWidget(self._log)

        # Cancel button
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.clicked.connect(self._on_cancel)
        layout.addWidget(self._cancel_btn)

    def _on_cancel(self):
        """Handle cancel button click."""
        self._cancelled = True
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.setText("Cancelling...")
        self._status_label.setText("Cancelling...")
        self.cancel_requested.emit()

    def update_progress(self, current: int, total: int):
        """Update the progress bar."""
        self._progress_bar.setValue(current)
        self._progress_label.setText(f"{current} / {total}")

    def set_current_file(self, filename: str):
        """Set the currently processing file."""
        self._status_label.setText(f"Processing: {filename}")

    def log_result(self, filename: str, success: bool, message: str):
        """Log a processing result."""
        if success:
            self._log.append(f"✓ {filename}")
        else:
            self._log.append(f"✗ {filename}: {message}")

    def processing_complete(self, successful: int, failed: int):
        """Update dialog when processing is complete."""
        if self._cancelled:
            self._status_label.setText("Processing cancelled")
        else:
            self._status_label.setText("Processing complete")

        self._cancel_btn.setText("Close")
        self._cancel_btn.setEnabled(True)
        self._cancel_btn.clicked.disconnect()
        self._cancel_btn.clicked.connect(self.accept)

        # Summary
        summary = f"\nCompleted: {successful} successful"
        if failed > 0:
            summary += f", {failed} failed"
        self._log.append(summary)
