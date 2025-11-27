import pytest
from src.archive import Archive
from tests.fixtures.artworks.hundred_valid_artworks import (
    hundred_valid_artworks_data,
)
from tests.fixtures.artworks.sample_data import three_special_chars_artworks_data
from PySide6.QtCore import Qt


def test_sorting(archive_with_custom_data):
    """Function tests if sorting works properly"""

    # Creating an instance of archive with special characters
    test_archive = archive_with_custom_data(hundred_valid_artworks_data)

    # Prints current sorting column
    print(f"Currently sorting by column #{test_archive.proxy_model.sortColumn()}")

    # Collecting data from proxy model
    namesUnsorted = []
    for i in range(test_archive.proxy_model.rowCount()):
        namesUnsorted.append(test_archive.proxy_model.index(i, 0).data())

    firstName = namesUnsorted[0]

    # Calling sorting inverted sorting method
    test_archive.proxy_model.sort(0, Qt.SortOrder.DescendingOrder)

    # Collecting data from proxy after sorting
    namesSorted = []
    for i in range(test_archive.proxy_model.rowCount()):
        namesSorted.append(test_archive.proxy_model.index(i, 0).data())

    lastName = namesSorted[99]

    # Asserting first and last names before and after sorting are the same
    assert firstName == lastName


def test_sorting_unicode(archive_with_custom_data):
    """Function tests if sorting works properly"""

    # Creating an instance of archive with special characters
    test_archive = archive_with_custom_data(three_special_chars_artworks_data)

    # Prints current sorting column
    print(f"Currently sorting by column #{test_archive.proxy_model.sortColumn()}")

    # Collecting data from proxy model
    namesUnsorted = []
    for i in range(test_archive.proxy_model.rowCount()):
        namesUnsorted.append(test_archive.proxy_model.index(i, 0).data())

    firstName = namesUnsorted[0]

    # Calling sorting inverted sorting method
    test_archive.proxy_model.sort(0, Qt.SortOrder.DescendingOrder)

    # Collecting data from proxy after sorting
    namesSorted = []
    for i in range(test_archive.proxy_model.rowCount()):
        namesSorted.append(test_archive.proxy_model.index(i, 0).data())

    lastName = namesSorted[2]

    # Asserting first and last names before and after sorting are the same
    assert firstName == lastName
