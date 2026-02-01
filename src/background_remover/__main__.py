"""Entry point for running the app with `python -m background_remover`."""

import sys

from background_remover.app import run_app


def main():
    """Main entry point."""
    sys.exit(run_app())


if __name__ == "__main__":
    main()
