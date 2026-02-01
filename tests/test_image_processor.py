"""Tests for the ImageProcessor class."""

import pytest
from pathlib import Path
from PIL import Image

from background_remover.image_processor import ImageProcessor


class TestImageProcessor:
    """Tests for ImageProcessor."""

    def test_supported_formats(self):
        """Test that common image formats are supported."""
        processor = ImageProcessor()

        assert processor.is_supported_format(Path("image.png"))
        assert processor.is_supported_format(Path("image.PNG"))
        assert processor.is_supported_format(Path("image.jpg"))
        assert processor.is_supported_format(Path("image.jpeg"))
        assert processor.is_supported_format(Path("image.webp"))
        assert processor.is_supported_format(Path("image.bmp"))
        assert processor.is_supported_format(Path("image.gif"))
        assert processor.is_supported_format(Path("image.tiff"))

    def test_unsupported_formats(self):
        """Test that non-image formats are rejected."""
        processor = ImageProcessor()

        assert not processor.is_supported_format(Path("file.txt"))
        assert not processor.is_supported_format(Path("file.pdf"))
        assert not processor.is_supported_format(Path("file.svg"))
        assert not processor.is_supported_format(Path("file.psd"))

    def test_generate_output_path(self, temp_output_dir):
        """Test output path generation."""
        processor = ImageProcessor()

        input_path = Path("/some/folder/photo.jpg")
        output_path = processor.generate_output_path(input_path, temp_output_dir)

        assert output_path.parent == temp_output_dir
        assert output_path.name == "photo.png"
        assert output_path.suffix == ".png"

    def test_generate_output_path_conflict(self, temp_output_dir):
        """Test output path handles filename conflicts."""
        processor = ImageProcessor()

        # Create existing file
        existing = temp_output_dir / "photo.png"
        existing.touch()

        input_path = Path("/some/folder/photo.jpg")
        output_path = processor.generate_output_path(input_path, temp_output_dir)

        assert output_path.name == "photo_1.png"

    def test_process_nonexistent_file(self, temp_output_dir):
        """Test that processing nonexistent file raises error."""
        processor = ImageProcessor()

        with pytest.raises(FileNotFoundError):
            processor.process_image(
                Path("/nonexistent/image.png"),
                temp_output_dir / "output.png"
            )

    def test_process_unsupported_format(self, temp_output_dir, tmp_path):
        """Test that processing unsupported format raises error."""
        processor = ImageProcessor()

        # Create a fake text file with image extension
        fake_file = tmp_path / "file.txt"
        fake_file.write_text("not an image")

        with pytest.raises(ValueError, match="Unsupported format"):
            processor.process_image(fake_file, temp_output_dir / "output.png")


class TestImageProcessorIntegration:
    """Integration tests that actually process images."""

    @pytest.fixture
    def sample_image(self, tmp_path) -> Path:
        """Create a simple test image."""
        img = Image.new("RGB", (100, 100), color="red")
        path = tmp_path / "test_image.png"
        img.save(path)
        return path

    @pytest.mark.slow
    def test_process_image_creates_output(self, sample_image, temp_output_dir):
        """Test that processing creates an output file."""
        processor = ImageProcessor()
        output_path = temp_output_dir / "result.png"

        processor.process_image(sample_image, output_path)

        assert output_path.exists()

    @pytest.mark.slow
    def test_process_image_has_transparency(self, sample_image, temp_output_dir):
        """Test that output image has RGBA mode."""
        processor = ImageProcessor()
        output_path = temp_output_dir / "result.png"

        processor.process_image(sample_image, output_path)

        with Image.open(output_path) as img:
            assert img.mode == "RGBA"

    @pytest.mark.slow
    def test_process_image_preserves_dimensions(self, sample_image, temp_output_dir):
        """Test that output has same dimensions as input."""
        processor = ImageProcessor()
        output_path = temp_output_dir / "result.png"

        processor.process_image(sample_image, output_path)

        with Image.open(sample_image) as original:
            with Image.open(output_path) as result:
                assert result.size == original.size
