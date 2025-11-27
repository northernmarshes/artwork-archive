import pytest
from src import archive
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    three_valid_artworks,
    three_special_chars_artworks,
    three_special_chars_artworks_data,
)

# ----------------------------------------
# ------- TESTING-THE-FILTERING-----------
# ----------------------------------------


def test_search_by_author(archive_fixture):
    """Function tests the happy path search by author"""
    test_archive = archive_fixture

    rows_before = test_archive.proxy_model.rowCount()

    # Extracting a name to filter
    author_02 = three_valid_artworks[1][0]

    # Filtering
    test_archive.searchbar.setText(author_02)

    rows_after = test_archive.proxy_model.rowCount()

    assert rows_after != rows_before
    assert rows_after == 1

    print(
        f"Before the search there were {rows_before} lines and after the search the number was {rows_after}"
    )


def test_search_by_title(archive_fixture):
    """Function tests the happy path search by title"""
    test_archive = archive_fixture

    rows_before = test_archive.proxy_model.rowCount()

    # Extracting a name to filter
    title_02 = three_valid_artworks[1][1]

    # Filtering
    test_archive.searchbar.setText(title_02)

    rows_after = test_archive.proxy_model.rowCount()

    assert rows_after != rows_before
    assert rows_after == 1

    print(
        f"Before the search there were {rows_before} lines and after the search the number was {rows_after}"
    )


def test_search_case_insensitive(archive_fixture):
    """Function tests the case insensitive search"""

    test_archive = archive_fixture

    rows_before = test_archive.proxy_model.rowCount()

    # Extracting a name to filter
    title_02 = three_valid_artworks[1][1]
    title_upper = title_02.upper()
    title_lower = title_02.lower()

    # Filtering 1
    test_archive.searchbar.setText(title_upper)
    rows_after_caps = test_archive.proxy_model.rowCount()

    # Filtering 2
    test_archive.searchbar.setText(title_lower)
    rows_after_low = test_archive.proxy_model.rowCount()

    assert rows_after_caps and rows_after_low != rows_before
    assert rows_after_caps and rows_after_low == 1

    print(
        f"Before the search there were {rows_before} lines \nAfter the search with caps the number was {rows_after_caps} \nAfter the search with lows the number was {rows_after_low}"
    )


def test_search_with_special_characters(
    archive_with_custom_data, three_special_chars_artworks
):
    """Function tests searching with special characters"""

    # Creating an instance of archive with special characters
    test_archive = archive_with_custom_data(three_special_chars_artworks)

    print(
        [
            test_archive.model.item(i, 0).text()
            for i in range(test_archive.proxy_model.rowCount())
        ]
    )

    # Counting rows before the search
    rows_before = test_archive.proxy_model.rowCount()

    # Searching
    test_archive.searchbar.setText(three_special_chars_artworks_data[2][0])

    # Counting rows after the search
    rows_after = test_archive.proxy_model.rowCount()

    # Assertions
    assert rows_after != rows_before
    assert rows_after == 1

    print(
        f"Before the search there were {rows_before} lines \nAfter the search with the number was {rows_after}"
    )


def test_search_with_partial_match():
    """Function tests searching with partial match"""
    pass
