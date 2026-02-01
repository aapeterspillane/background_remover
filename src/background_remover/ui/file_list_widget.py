"""Widget for displaying and managing the list of files to process."""

from pathlib import Path
from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FileListWidget(QWidget):
    """Widget showing queued files with management controls."""

    files_changed = Signal()  # Emitted when file list changes

    def __init__(self, parent=None):
        """Initialize the file list widget."""
        super().__init__(parent)
        self._files: List[Path] = []
        self._setup_ui()

    def _setup_ui(self):
        """Set up the widget layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header with count
        header_layout = QHBoxLayout()
        self._count_label = QLabel("Files: 0")
        self._count_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(self._count_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # File list
        self._list_widget = QListWidget()
        self._list_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self._list_widget.setAlternatingRowColors(True)
        layout.addWidget(self._list_widget)

        # Buttons
        button_layout = QHBoxLayout()

        self._remove_btn = QPushButton("Remove Selected")
        self._remove_btn.clicked.connect(self._remove_selected)
        self._remove_btn.setEnabled(False)
        button_layout.addWidget(self._remove_btn)

        self._clear_btn = QPushButton("Clear All")
        self._clear_btn.clicked.connect(self.clear)
        self._clear_btn.setEnabled(False)
        button_layout.addWidget(self._clear_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Connect selection change to enable/disable remove button
        self._list_widget.itemSelectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        """Enable/disable remove button based on selection."""
        self._remove_btn.setEnabled(len(self._list_widget.selectedItems()) > 0)

    def add_files(self, files: List[Path]):
        """Add files to the list, avoiding duplicates."""
        existing = set(self._files)
        for file_path in files:
            if file_path not in existing:
                self._files.append(file_path)
                item = QListWidgetItem(file_path.name)
                item.setToolTip(str(file_path))
                self._list_widget.addItem(item)

        self._update_count()
        self.files_changed.emit()

    def _remove_selected(self):
        """Remove selected files from the list."""
        selected_rows = sorted(
            [self._list_widget.row(item) for item in self._list_widget.selectedItems()],
            reverse=True,
        )
        for row in selected_rows:
            self._list_widget.takeItem(row)
            del self._files[row]

        self._update_count()
        self.files_changed.emit()

    def clear(self):
        """Remove all files from the list."""
        self._list_widget.clear()
        self._files.clear()
        self._update_count()
        self.files_changed.emit()

    def _update_count(self):
        """Update the file count label."""
        count = len(self._files)
        self._count_label.setText(f"Files: {count}")
        self._clear_btn.setEnabled(count > 0)

    def get_files(self) -> List[Path]:
        """Get the list of files."""
        return self._files.copy()

    def file_count(self) -> int:
        """Get the number of files in the list."""
        return len(self._files)

    def update_file_status(self, filename: str, status: str):
        """Update the display text for a file to show its status."""
        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            # Check if this is the right file (by original name in tooltip)
            if Path(item.toolTip()).name == filename:
                item.setText(f"{filename} - {status}")
                break
