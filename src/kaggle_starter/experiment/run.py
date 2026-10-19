"""Experiment entry-point stub; implement the workflow for your competition.

Keep model architecture, dataset details and metric definitions in their own modules.
"""

from pathlib import Path

from kaggle_starter.config import Config
from kaggle_starter.core.schemas import DataSplit
from kaggle_starter.experiment.contract import KaggleModel
from kaggle_starter.loggers import CustomLogger


def run_experiment(
    model: KaggleModel, split: DataSplit, *, config: Config, name: str, logger: CustomLogger
) -> Path:
    """Train and validate, then return the run's output directory.

    Create the run folder, prepare data and split, initialize the model and tracker,
    save inputs, train, evaluate and save results. Add state/resume handling if needed.
    """
    return Path()
