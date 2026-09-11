"""Load project config from config/config.yaml."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.yaml"


@lru_cache
def load_config(path: Path = _CONFIG_PATH) -> dict[str, Any]:
    """Return the parsed config dict (cached)."""
    with path.open() as f:
        return yaml.safe_load(f)
