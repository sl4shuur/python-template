from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import wandb
from lightning.pytorch.loggers import WandbLogger
from lightning.pytorch.utilities import rank_zero_only

from kaggle_starter.config import TrackingConfig


def _open(config: TrackingConfig, run_id: str, name: str, save_dir: Path) -> WandbLogger:
    tracker = WandbLogger(
        project=config.project,
        entity=config.entity,
        name=name,
        id=run_id,
        resume="allow",
        save_dir=save_dir,
        # Offline runs are synced later with `wandb sync`, which Kaggle notebooks need.
        offline=config.offline,
    )
    _ = tracker.experiment
    return tracker


@contextmanager
def wandb_run(
    config: TrackingConfig, *, run_id: str, name: str, save_dir: Path
) -> Iterator[WandbLogger]:
    """Open the W&B run for `run_experiment`. The run is closed on exit, even after an error.

    `run_id` restores the saved identity; `name` is a human-readable experiment label.
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    if wandb.run is not None:
        # A cell interrupted earlier can leave its run open, and one id cannot be opened twice.
        wandb.run.finish()
    if rank_zero_only.rank == 0 and config.api_key is not None and not config.offline:
        wandb.login(key=config.api_key.get_secret_value())
    tracker = _open(config, run_id, name, save_dir)
    exit_code = 0
    try:
        yield tracker
    except BaseException:
        exit_code = 1
        raise
    finally:
        # `tracker.experiment` would start a run when `init` failed and hide the real error.
        if wandb.run is not None:
            wandb.run.finish(exit_code=exit_code)
