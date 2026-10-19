import pandas as pd

from kaggle_starter.experiment.contract import KaggleModel, RunContext
from kaggle_starter.core.schemas import Candidate


class DummyBaseline(KaggleModel):

    def fit(self, train: pd.DataFrame, valid: pd.DataFrame, context: RunContext) -> None:
        pass

    def predict(self, frame: pd.DataFrame, context: RunContext) -> list[Candidate]:
        return [Candidate(score=1.0)]
