"""Background Remover - A desktop app to remove image backgrounds using AI."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("background_remover")
except PackageNotFoundError:
    # Package is not installed (e.g., running from source without pip install)
    __version__ = "0.0.0.dev"
