"""Run on Kaggle to record the image's Python and installed packages."""

import datetime
import platform
import subprocess
import sys
from pathlib import Path


def main() -> None:
    packages = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, check=True
    ).stdout
    header = (
        f"# Kaggle default image, Python {platform.python_version()}, taken {datetime.date.today()}"
    )
    Path("/kaggle/working/image-freeze.txt").write_text(header + "\n" + packages, encoding="utf-8")


if __name__ == "__main__":
    main()
