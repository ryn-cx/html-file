"""Library for working with HTML files."""
from __future__ import annotations

from typing import TYPE_CHECKING

from paved_path import CobblestoneCache, PavedPath
from strict_soup import StrictSoup

if TYPE_CHECKING:
    from paved_path import PathableType


class HTMLCache(CobblestoneCache):
    """Cache for JSONFile.

    This is set up as a seperate class to make it easier to clear the cache.
    """

    def __init__(self) -> None:
        """Initialize the cache with None values."""
        self.parsed: StrictSoup | None = None
        super().__init__()


class HTMLFile(PavedPath):
    """Library for working with HTML files."""

    def __init__(self, *_args: PathableType) -> None:
        """Initialize the HTMLFile class.

        Args:
        ----
            _args: The path fragments to join together.
        """
        self.cache = HTMLCache()

    def write(self, content: StrictSoup | str | bytes, *, write_through: bool = True) -> None:
        """Write the data to the file.

        Args:
        ----
            content: The object to be written to the file.
            write_through: Whether to write through the cache.
        """
        # Strings and bytes are not serialized because no changescan be made on them.
        if isinstance(content, (str, bytes)):
            super().write(content, write_through=write_through)
            if write_through:
                self.cache.parsed = None
        # All other objects are serialized using json
        else:
            super().write(str(content), write_through=write_through)
            if write_through:
                self.cache.parsed = content

    def parsed(self) -> StrictSoup:
        """Parse the file bytes using BeautifulSoup.

        Returns
        -------
            An uncached StrictSoup object.
        """
        return StrictSoup(self.read_bytes(), "lxml")

    def parsed_cached(self, *, reload: bool = False) -> StrictSoup:
        """Parse the file bytes using StrictSoup and cache the result.

        Args:
        ----
            reload: Whether to reload the file bytes and reparse the file.

        Returns:
        -------
            A cached parsed StrictSoup object.
        """
        # I don't know of any reason why you would want to use read_text instead of read_bytes for BeautifulSoup. Unless
        # a specific need arises this function will always just use read_bytes
        if not self.cache.parsed or reload:
            self.cache.parsed = StrictSoup(self.read_bytes_cached(reload=reload), "lxml")

        return self.cache.parsed
