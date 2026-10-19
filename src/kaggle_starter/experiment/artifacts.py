"""Artifact-saving stubs; implement for your competition.

Keep file formats and tracker logging here. For distributed training, write shared
files only on rank zero.
"""

from pathlib import Path

from kaggle_starter.config import Config


def save_inputs(output_dir: Path, *, config: Config) -> None:
    """Save config.safe_dump(), split IDs and any preprocessing needed to reproduce the run."""
    pass


def save_report(output_dir: Path, *, metrics: dict[str, float]) -> None:
    """Save scores and competition-specific predictions; optionally log them to a tracker."""
    pass
