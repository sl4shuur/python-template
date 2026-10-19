"""Optional run-state stubs; implement if you need resume support.

Choose the state fields for your competition, e.g. run ID, phase and checkpoint.
Check configuration and split compatibility before resuming an existing run.
"""

from pathlib import Path


def load_state(output_dir: Path) -> dict[str, object]:
    """Read saved progress, or return initial state for a new run."""
    return {}


def save_state(output_dir: Path, state: dict[str, object]) -> None:
    """Write progress atomically; record completion, failure or interruption here."""
    pass

