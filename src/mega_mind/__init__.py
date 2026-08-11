"""Mega-Mind Orchestrator package.

The canonical version lives in pyproject.toml. When installed, __version__ is
read from package metadata; the fallback constant keeps the source checkout
self-consistent and is asserted to equal pyproject.toml by the validator.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mmo")
except PackageNotFoundError:  # source checkout / not yet installed
    __version__ = "1.0.1"
