"""Image processing wrapper for rembg."""

from pathlib import Path

from PIL import Image
from rembg import new_session, remove


class ImageProcessor:
    """Handles background removal using rembg."""

    SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tiff"}

    def __init__(self):
        """Initialize the processor with a reusable rembg session."""
        self._session = None

    @property
    def session(self):
        """Lazy-load the rembg session for batch efficiency."""
        if self._session is None:
            self._session = new_session("u2net")
        return self._session

    @classmethod
    def is_supported_format(cls, path: Path) -> bool:
        """Check if a file has a supported image format."""
        return path.suffix.lower() in cls.SUPPORTED_FORMATS

    def process_image(self, input_path: Path, output_path: Path) -> None:
        """
        Remove background from an image and save as PNG with transparency.

        Args:
            input_path: Path to the input image file.
            output_path: Path where the output PNG will be saved.

        Raises:
            FileNotFoundError: If input file doesn't exist.
            ValueError: If input format is not supported.
            Exception: If processing fails.
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if not self.is_supported_format(input_path):
            raise ValueError(f"Unsupported format: {input_path.suffix}")

        # Ensure output has .png extension
        output_path = output_path.with_suffix(".png")

        # Load input image
        with Image.open(input_path) as img:
            # Convert to RGBA if needed
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            # Remove background using rembg
            result = remove(img, session=self.session)

            # Save with transparency
            result.save(output_path, "PNG")

    def generate_output_path(self, input_path: Path, output_folder: Path) -> Path:
        """
        Generate output path for a processed image.

        Args:
            input_path: Original input file path.
            output_folder: Folder where output should be saved.

        Returns:
            Path for the output file (always .png).
        """
        stem = input_path.stem
        output_path = output_folder / f"{stem}.png"

        # Handle filename conflicts
        counter = 1
        while output_path.exists():
            output_path = output_folder / f"{stem}_{counter}.png"
            counter += 1

        return output_path
