"""The competition-specific part: swap model code without rewriting lifecycle."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from lightning.pytorch.loggers import Logger

from kaggle_starter.core.schemas import Candidate
from kaggle_starter.loggers import CustomLogger


@dataclass(frozen=True)
class RunContext:
    output_dir: Path
    tracker: Logger
    logger: CustomLogger
    # Names the validation subset; scores of different protocols are never compared.
    protocol: str


class KaggleModel(ABC):
    @abstractmethod
    def fit(self, train: pd.DataFrame, valid: pd.DataFrame, context: RunContext) -> None:
        """Train using target_column, store reusable artifacts inside context.output_dir."""

    @abstractmethod
    def predict(self, frame: pd.DataFrame, context: RunContext) -> list[Candidate]:
        """Return one numeric prediction or class per input row in the same order."""
