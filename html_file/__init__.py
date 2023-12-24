"""Library for working with HTML files."""
from __future__ import annotations

from typing import TYPE_CHECKING

from paved_path import PavedPath
from strict_soup import StrictSoup

if TYPE_CHECKING:
    from paved_path import PathableType


class HTMLFile(PavedPath):
    """Library for working with HTML files."""

    def __init__(self, *_args: PathableType) -> None:
        """Initialize the HTMLFile class."""
        self.parsed_cached_value = None
        super().__init__()

    def parsed(self) -> StrictSoup:
        """Parse the file bytes using BeautifulSoup."""
        return StrictSoup(self.read_bytes(), "lxml")

    def parsed_cached(self, *, reload: bool = False) -> StrictSoup:
        """Parse the file bytes using BeautifulSoup and cache the result."""
        # I don't know of any reason why you would want to use read_text instead of read_bytes for BeautifulSoup. Unless
        # a specific need arises this function will always just use read_bytes
        if not self.parsed_cached_value or reload:
            self.parsed_cached_value = StrictSoup(self.read_bytes_cached(reload=reload), "lxml")

        return self.parsed_cached_value
