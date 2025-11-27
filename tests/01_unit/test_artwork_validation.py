import pytest
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    single_invalid_year,
    three_special_chars_artworks_data,
)

# ----------------------------------------
# ------- TESTING-THE-EDGE-CASES----------
# ----------------------------------------


def test_add_artwork_with_unicode_data(archive_fixture):
    """Function tests adding a new artwork with unicode data"""

    # Creating test instance of Archive with three sample artworks
    test_archive = archive_fixture

    # Counting rows before the addition
    rows_before = test_archive.model.rowCount()

    japaneseArtwork = three_special_chars_artworks_data[0]

    test_archive.author_line_edit.setText(japaneseArtwork[0])
    test_archive.title_line_edit.setText(japaneseArtwork[1])
    test_archive.size_line_edit.setText(japaneseArtwork[2])
    test_archive.medium_line_edit.setText(japaneseArtwork[3])
    test_archive.year_line_edit.setText(japaneseArtwork[4])

    test_archive.addArtwork()

    # Counting rows after the adddintion
    rows_after = test_archive.model.rowCount()

    japaneseArtist = japaneseArtwork[0]
    last_row = rows_after - 1
    addedArtist = test_archive.model.item(last_row).text()
    print(f"Added artwork by {addedArtist}")

    assert addedArtist == japaneseArtist


def test_add_artwork_with_empty_fields(archive_fixture):
    """Function tests adding a new artwork with empty fields"""

    test_archive = archive_fixture

    # Collecting sample data
    print("Adding empty fields")
    rows_before = test_archive.model.rowCount()

    # Inserting data to QLineEdit
    test_archive.author_line_edit.setText("")
    test_archive.title_line_edit.setText("")
    test_archive.size_line_edit.setText("")
    test_archive.medium_line_edit.setText("")
    test_archive.year_line_edit.setText("")

    # Error assertion
    with pytest.raises(ValueError, match="All fields must be filled"):
        test_archive.addArtwork()

    # Counting rows after addition
    rows_after = test_archive.model.rowCount()

    assert rows_after == rows_before


def test_add_artwork_with_invalid_data(archive_fixture):
    """Tests if adding string to year is blocked"""

    test_archive = archive_fixture

    # Collecting sample data
    invalidyear = single_invalid_year[0]
    author_invy, title_invy, size_invy, medium_invy, year_invy, filename_invy = (
        invalidyear
    )

    print(f"Adding '{year_invy}' as a year")

    rows_before = test_archive.model.rowCount()

    # Inserting data to QLineEdit
    test_archive.author_line_edit.setText(author_invy)
    test_archive.title_line_edit.setText(title_invy)
    test_archive.size_line_edit.setText(size_invy)
    test_archive.medium_line_edit.setText(medium_invy)
    test_archive.year_line_edit.setText(year_invy)

    # Error assertion
    with pytest.raises(ValueError, match="Invalid year value"):
        test_archive.addArtwork()

    # Counting rows after addition
    rows_after = test_archive.model.rowCount()

    # Checking for added year
    last_row_index = rows_after - 1
    year = test_archive.model.item(last_row_index, 4)

    # Printing year if the invalid type data passed or an error message
    if rows_after != rows_before:
        print(f"Added year: {year.text()}")

    assert rows_after == rows_before


def test_delete_artwork_no_selection(archive_fixture):
    """Functions tests if deleting with no selection doesn't create malfunction"""

    # Create an instance with 3 sample artworks
    test_archive = archive_fixture

    # Counting rows before deletion
    rows_before = test_archive.model.rowCount()

    # Error assertion
    with pytest.raises(IndexError, match="list index out of range"):
        test_archive.deleteArtwork()

    # Counting rows after addition
    rows_after = test_archive.model.rowCount()

    assert rows_after == rows_before


def test_delete_multiple_artworks(archive_fixture):
    """Function tests adding a new artwork"""

    # Create an instance with 3 sample artworks
    test_archive = archive_fixture

    # Counting rows before addition
    rows_before = test_archive.model.rowCount()

    # Deleting three artworks

    test_archive.deleteArtwork(0)
    test_archive.deleteArtwork(0)
    test_archive.deleteArtwork(0)

    # Counting rows after addition
    rows_after = test_archive.model.rowCount()

    # Asserting row count
    assert rows_before - rows_after == 3
