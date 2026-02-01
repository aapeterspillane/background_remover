"""Worker thread for async image processing."""

from pathlib import Path
from threading import Lock
from typing import List, Optional

from PySide6.QtCore import QThread, Signal

from background_remover.image_processor import ImageProcessor


class ProcessingWorker(QThread):
    """QThread for non-blocking batch image processing."""

    # Signals
    progress_updated = Signal(int, int)  # current, total
    file_started = Signal(str)  # filename
    file_completed = Signal(str, bool, str)  # filename, success, message
    all_completed = Signal(int, int)  # successful, failed

    def __init__(
        self,
        files: List[Path],
        output_folder: Path,
        processor: Optional[ImageProcessor] = None,
        parent=None,
    ):
        """
        Initialize the worker.

        Args:
            files: List of input file paths to process.
            output_folder: Folder where outputs will be saved.
            processor: Optional pre-loaded ImageProcessor instance.
            parent: Parent QObject.
        """
        super().__init__(parent)
        self._files = files
        self._output_folder = output_folder
        self._cancelled = False
        self._cancel_lock = Lock()
        self._processor = processor if processor else ImageProcessor()

    def cancel(self):
        """Request cancellation of the processing."""
        with self._cancel_lock:
            self._cancelled = True

    def is_cancelled(self) -> bool:
        """Check if cancellation was requested."""
        with self._cancel_lock:
            return self._cancelled

    def run(self):
        """Process all files in the queue."""
        total = len(self._files)
        successful = 0
        failed = 0

        for i, input_path in enumerate(self._files):
            if self.is_cancelled():
                break

            filename = input_path.name
            self.file_started.emit(filename)

            try:
                output_path = self._processor.generate_output_path(
                    input_path, self._output_folder
                )
                self._processor.process_image(input_path, output_path)
                self.file_completed.emit(filename, True, str(output_path))
                successful += 1
            except Exception as e:
                self.file_completed.emit(filename, False, str(e))
                failed += 1

            self.progress_updated.emit(i + 1, total)

        self.all_completed.emit(successful, failed)
