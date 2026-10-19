"""Shared data domain models"""

import numpy as np
from pydantic import BaseModel, ConfigDict, field_validator


class Candidate(BaseModel):
    model_config = ConfigDict(frozen=True)

    # Higher ranks first. Only compared between candidates of one molecule.
    score: float

    @field_validator("score")
    @classmethod
    def _not_nan(cls, score: float) -> float:
        if np.isnan(score):
            raise ValueError("score must not be NaN.")
        return score
