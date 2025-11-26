import pytest
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    single_valid_artwork,
    three_valid_artworks,
    three_special_chars_artworks,
    three_special_chars_artworks_data,
    single_invalid_year,
)

# ----------------------------------------
# ------- TESTING-THE-FILTERING-----------
# ----------------------------------------


def test_search_by_author(archive_fixture):
    """Function tests the happy path search by author"""
    archive = archive_fixture

    rows_before = archive.proxy_model.rowCount()

    # Extracting a name to filter
    author_02 = three_valid_artworks[1][0]

    # Filtering
    archive.searchbar.setText(author_02)

    rows_after = archive.proxy_model.rowCount()

    assert rows_after != rows_before
    assert rows_after == 1

    print(
        f"Before the search there were {rows_before} lines and after the search the number was {rows_after}"
    )


def test_search_by_title(archive_fixture):
    """Function tests the happy path search by title"""
    archive = archive_fixture

    rows_before = archive.proxy_model.rowCount()

    # Extracting a name to filter
    title_02 = three_valid_artworks[1][1]

    # Filtering
    archive.searchbar.setText(title_02)

    rows_after = archive.proxy_model.rowCount()

    assert rows_after != rows_before
    assert rows_after == 1

    print(
        f"Before the search there were {rows_before} lines and after the search the number was {rows_after}"
    )


def test_search_case_insensitive(archive_fixture):
    """Function tests the case insensitive search"""
    archive = archive_fixture

    rows_before = archive.proxy_model.rowCount()

    # Extracting a name to filter
    title_02 = three_valid_artworks[1][1]
    title_upper = title_02.upper()
    title_lower = title_02.lower()

    # Filtering 1
    archive.searchbar.setText(title_upper)
    rows_after_caps = archive.proxy_model.rowCount()

    # Filtering 2
    archive.searchbar.setText(title_lower)
    rows_after_low = archive.proxy_model.rowCount()

    assert rows_after_caps and rows_after_low != rows_before
    assert rows_after_caps and rows_after_low == 1

    print(
        f"Before the search there were {rows_before} lines \nAfter the search with caps the number was {rows_after_caps} \nAfter the search with lows the number was {rows_after_low}"
    )


def test_search_with_special_characters(
    monkeypatch, three_special_chars_artworks, archive_fixture
):
    """Function tests searching with special characters"""
    monkeypatch.setattr(
        "src.archive.three_valid_artworks", three_special_chars_artworks
    )

    archive = archive_fixture
    rows_before = archive.proxy_model.rowCount()
    archive.searchbar.setText(three_special_chars_artworks_data[2][0])
    rows_after = archive.proxy_model.rowCount()

    assert rows_after != rows_before
    assert rows_after == 0
    print(
        f"Before the search there were {rows_before} lines \nAfter the search with the number was {rows_after}"
    )


def test_search_with_partial_match():
    """Function tests searching with partial match"""
    pass
