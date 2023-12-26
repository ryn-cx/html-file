"""Test the HTMLFile class."""

from typing import Generator

import pytest
from strict_soup import StrictSoup

from html_file import HTMLFile


class TestHTMLFile:
    """Test the HTMLFile class."""

    @pytest.fixture()
    def temporary_file(self) -> Generator[HTMLFile, None, None]:
        """Get a file path for testing and delete the test_data folder if it exists after the test."""
        temporary_file = HTMLFile("test_data/file.html")
        yield temporary_file
        if temporary_file.parent == HTMLFile("test_data"):
            temporary_file.parent.delete()

    def test_write(self, temporary_file: HTMLFile) -> None:
        """Test the write method."""
        soup = StrictSoup("<title>Example</title>")
        # Test empty cache without write_through
        temporary_file.write(soup, write_through=False)
        assert temporary_file.cache.parsed is None

        # Test empty cache with write_through
        temporary_file.write(soup)
        assert temporary_file.cache.parsed == soup

        # Test non-empty cache without write_through
        temporary_file.write(soup, write_through=False)
        assert temporary_file.cache.parsed is None

        # Test non-empty cache with write_through
        temporary_file.write(soup)
        assert temporary_file.cache.parsed == soup

    def test_parse(self, temporary_file: HTMLFile) -> None:
        """Test the parse method."""
        soup = StrictSoup("<title>Example</title>")
        temporary_file.write(soup)
        assert temporary_file.parsed() == soup
        assert temporary_file.cache.parsed == soup
