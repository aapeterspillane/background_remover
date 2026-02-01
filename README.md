# Background Remover

A cross-platform desktop application for removing image backgrounds using AI.

## Features

- **Drag-and-drop** images directly into the app
- **Batch processing** - process multiple images at once
- **AI-powered** background removal using U2-Net
- **Preserves quality** - outputs PNG with transparency at original resolution
- **Cross-platform** - works on macOS and Windows

## Supported Formats

Input: PNG, JPG, JPEG, WebP, BMP, GIF, TIFF

Output: PNG with transparency

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/background_remover.git
   cd background_remover
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Run the app:
   ```bash
   python -m background_remover
   ```

### Development Setup

Install with dev dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Run tests excluding slow integration tests:
```bash
pytest -m "not slow"
```

## Usage

1. **Add images** - Drag and drop images onto the drop zone, or click "Add Files" to browse
2. **Select output folder** - Click "Select..." to choose where processed images will be saved
3. **Process** - Click "Remove Backgrounds" to start processing
4. **Monitor progress** - Watch the progress dialog for status updates

## Building Standalone App

### macOS

```bash
python scripts/build_macos.py
```

This creates `dist/Background Remover.app`. To create a DMG:

```bash
./scripts/create_dmg.sh
```

### Windows

```bash
python scripts/build_windows.py
```

This creates `dist/BackgroundRemover/BackgroundRemover.exe`.

## Technology Stack

- **GUI**: PySide6 (Qt6)
- **AI Model**: rembg with U2-Net
- **Image Processing**: Pillow
- **Packaging**: PyInstaller

## License

MIT License - see LICENSE file for details.
