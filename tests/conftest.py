"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def temp_output_dir(tmp_path) -> Path:
    """Create a temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
