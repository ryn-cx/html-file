"""Library for working with HTML files."""
from __future__ import annotations

from typing import TYPE_CHECKING

from paved_path import CobblestoneCache, PavedPath
from strict_soup import StrictSoup

if TYPE_CHECKING:
    from paved_path import PathableType


# This is set up as a seperate class to make it easier to clear the cache.
class HTMLCache(CobblestoneCache):
    """Cache for HTMLFile."""

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
            write_through: If True the cache will be updated to match what is written to the file. If False the cache
            will be cleared. Either way the cache is not allowed to be out of sync with the file, either it matches the
            file or it is None.
        """
        # Strings and bytes are not serialized because no changescan be made on them.
        if isinstance(content, (str, bytes)):
            super().write(content, write_through=write_through)
        # All other objects are serialized using bs4
        else:
            super().write(str(content), write_through=write_through)
            if write_through:
                self.cache.parsed = content

    def parsed(self) -> StrictSoup:
        """Read the file bytes and parse the file using BeautifulSoup.

        Returns
        -------
            An uncached StrictSoup object.
        """
        # I don't know of any reason why you would want to use read_text instead of read_bytes for BeautifulSoup. Unless
        # a specific need arises this function will always use read_bytes.
        return StrictSoup(self.read_bytes(), "lxml")

    def parsed_cached(self, *, reload: bool = False) -> StrictSoup:
        """Read the file bytes, parse the file using BeautifulSoup, and cache the result.

        Args:
        ----
            reload: If true read the bytes from the file, parse it using StrictSoup and cache the result even if a
            StrictSoup object is already cached. If False use the cached StrictSoup object if it exists otherwise read
            the bytes from the file, parse it using StrictSoup and cache the result.

        Returns:
        -------
            A cached StrictSoup object.
        """
        if not self.cache.parsed or reload:
            self.cache.parsed = self.parsed()

        return self.cache.parsed
