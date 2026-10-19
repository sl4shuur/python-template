"""Experiment entry-point stub; implement the workflow for your competition.

Keep model architecture, dataset details and metric definitions in their own modules.
"""

from pathlib import Path

from kaggle_starter.config import Config


def run_experiment(config: Config, *, name: str) -> Path:
    """Train and validate, then return the run's output directory.

    Create the run folder, prepare data and split, initialize the model and tracker,
    save inputs, train, evaluate and save results. Add state/resume handling if needed.
    """
    pass
