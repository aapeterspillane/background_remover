"""Main application window."""

from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from background_remover.drop_zone import DropZone
from background_remover.image_processor import ImageProcessor
from background_remover.ui.file_list_widget import FileListWidget
from background_remover.ui.progress_dialog import ProgressDialog
from background_remover.worker import ProcessingWorker


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, processor: Optional[ImageProcessor] = None):
        """
        Initialize the main window.

        Args:
            processor: Optional pre-loaded ImageProcessor instance for faster startup.
        """
        super().__init__()
        self._output_folder: Optional[Path] = None
        self._worker: Optional[ProcessingWorker] = None
        self._progress_dialog: Optional[ProgressDialog] = None
        self._processor = processor  # Pre-loaded processor from splash screen

        self._setup_ui()
        self._setup_menu()
        self._update_process_button()

    def _setup_ui(self):
        """Set up the main window UI."""
        self.setWindowTitle("Background Remover")
        self.setMinimumSize(600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Drop zone
        self._drop_zone = DropZone()
        self._drop_zone.files_dropped.connect(self._on_files_dropped)
        layout.addWidget(self._drop_zone)

        # Add files button
        add_btn = QPushButton("Add Files...")
        add_btn.clicked.connect(self._browse_files)
        layout.addWidget(add_btn)

        # File list
        self._file_list = FileListWidget()
        self._file_list.files_changed.connect(self._update_process_button)
        layout.addWidget(self._file_list, stretch=1)

        # Output folder selector
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output Folder:"))
        self._output_label = QLabel("Not selected")
        self._output_label.setStyleSheet("color: #666666;")
        output_layout.addWidget(self._output_label, stretch=1)
        output_btn = QPushButton("Select...")
        output_btn.clicked.connect(self._select_output_folder)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # Process button
        self._process_btn = QPushButton("Remove Backgrounds")
        self._process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90d9;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3a7fc8;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self._process_btn.clicked.connect(self._start_processing)
        layout.addWidget(self._process_btn)

    def _setup_menu(self):
        """Set up the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        open_action = file_menu.addAction("Open Images...")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._browse_files)

        output_action = file_menu.addAction("Select Output Folder...")
        output_action.setShortcut("Ctrl+Shift+O")
        output_action.triggered.connect(self._select_output_folder)

        file_menu.addSeparator()

        quit_action = file_menu.addAction("Quit")
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)

    @Slot(list)
    def _on_files_dropped(self, files: List[Path]):
        """Handle files dropped onto the drop zone."""
        self._file_list.add_files(files)

    def _browse_files(self):
        """Open file browser to select images."""
        formats = " ".join(
            f"*{ext}" for ext in sorted(ImageProcessor.SUPPORTED_FORMATS)
        )
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            f"Images ({formats});;All Files (*)",
        )
        if files:
            self._file_list.add_files([Path(f) for f in files])

    def _select_output_folder(self):
        """Open folder browser to select output location."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self._output_folder = Path(folder)
            self._output_label.setText(str(self._output_folder))
            self._output_label.setStyleSheet("color: #000000;")
            self._update_process_button()

    def _update_process_button(self):
        """Enable/disable process button based on state."""
        can_process = (
            self._file_list.file_count() > 0
            and self._output_folder is not None
            and self._worker is None
        )
        self._process_btn.setEnabled(can_process)

    def _start_processing(self):
        """Start background removal processing."""
        files = self._file_list.get_files()
        if not files or not self._output_folder:
            return

        # Create and show progress dialog
        self._progress_dialog = ProgressDialog(len(files), self)
        self._progress_dialog.cancel_requested.connect(self._cancel_processing)

        # Create worker thread (use pre-loaded processor if available)
        self._worker = ProcessingWorker(files, self._output_folder, self._processor)
        self._worker.progress_updated.connect(self._progress_dialog.update_progress)
        self._worker.file_started.connect(self._on_file_started)
        self._worker.file_completed.connect(self._on_file_completed)
        self._worker.all_completed.connect(self._on_processing_complete)
        self._worker.finished.connect(self._on_worker_finished)

        self._update_process_button()
        self._worker.start()
        self._progress_dialog.exec()

    @Slot(str)
    def _on_file_started(self, filename: str):
        """Handle file processing started."""
        if self._progress_dialog:
            self._progress_dialog.set_current_file(filename)
        self._file_list.update_file_status(filename, "Processing...")

    @Slot(str, bool, str)
    def _on_file_completed(self, filename: str, success: bool, message: str):
        """Handle file processing completed."""
        if self._progress_dialog:
            self._progress_dialog.log_result(filename, success, message)

        status = "Done" if success else f"Failed: {message}"
        self._file_list.update_file_status(filename, status)

    @Slot(int, int)
    def _on_processing_complete(self, successful: int, failed: int):
        """Handle all processing complete."""
        if self._progress_dialog:
            self._progress_dialog.processing_complete(successful, failed)

    def _on_worker_finished(self):
        """Handle worker thread finished."""
        self._worker = None
        self._update_process_button()

    def _cancel_processing(self):
        """Cancel the current processing."""
        if self._worker:
            self._worker.cancel()

    def closeEvent(self, event):
        """Handle window close - ensure worker is stopped."""
        if self._worker and self._worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Processing in Progress",
                "Processing is still in progress. Do you want to cancel and exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._worker.cancel()
                self._worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
