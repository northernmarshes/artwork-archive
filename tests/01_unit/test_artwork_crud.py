import pytest
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    single_valid_artwork,
    three_valid_artworks,
    single_invalid_year,
)


def test_add_artwork(archive_fixture):
    """Function tests adding a new artwork"""

    archive = archive_fixture

    # Collecting sample data
    artwork = single_valid_artwork[0]
    print(f"Adding {artwork}")
    author, title, size, medium, year, filename = artwork
    # Inserting data to QLineEdit
    archive.author_line_edit.setText(author)
    archive.title_line_edit.setText(title)
    archive.size_line_edit.setText(size)
    archive.medium_line_edit.setText(medium)
    archive.year_line_edit.setText(year)

    # Counting rows before addition
    rows_before = archive.model.rowCount()

    # Calling the function
    archive.addArtwork()

    # Counting rows after addition
    rows_after = archive.model.rowCount()

    # Printing data from of the added artwork
    last_row_index = rows_after - 1
    if last_row_index > 0:
        last_row_data = []
        for col in range(archive.model.columnCount()):
            item = archive.model.item(last_row_index, col)
            last_row_data.append(item.text() if item is not None else None)
        print(f"Newly added artwork is {last_row_data}")

    # Asserting row count
    assert rows_after == rows_before + 1


def test_add_artwork_with_empty_fields(archive_fixture):
    """Function tests adding a new artwork with empty fields"""

    archive = archive_fixture

    # Collecting sample data
    print("Adding empty fields")
    rows_before = archive.model.rowCount()
    # Inserting data to QLineEdit
    archive.author_line_edit.setText("")
    archive.title_line_edit.setText("")
    archive.size_line_edit.setText("")
    archive.medium_line_edit.setText("")
    archive.year_line_edit.setText("")

    # Error assertion
    with pytest.raises(ValueError, match="All fields must be filled"):
        archive.addArtwork()

    # Counting rows after addition
    rows_after = archive.model.rowCount()

    assert rows_after == rows_before


def test_add_artwork_with_invalid_data(archive_fixture):
    """Tests if adding string to year is blocked"""

    archive = archive_fixture

    # Collecting sample data
    invalidyear = single_invalid_year[0]
    author_invy, title_invy, size_invy, medium_invy, year_invy, filename_invy = (
        invalidyear
    )

    print(f"Adding '{year_invy}' as a year")

    rows_before = archive.model.rowCount()

    # Inserting data to QLineEdit
    archive.author_line_edit.setText(author_invy)
    archive.title_line_edit.setText(title_invy)
    archive.size_line_edit.setText(size_invy)
    archive.medium_line_edit.setText(medium_invy)
    archive.year_line_edit.setText(year_invy)

    # Error assertion
    with pytest.raises(ValueError, match="Invalid year value"):
        archive.addArtwork()

    # Counting rows after addition
    rows_after = archive.model.rowCount()

    # Checking for added year
    last_row_index = rows_after - 1
    year = archive.model.item(last_row_index, 4)

    # Printing year if the invalid type data passed or an error message
    if rows_after != rows_before:
        print(f"Added year: {year.text()}")

    assert rows_after == rows_before


def test_delete_artwork(archive_fixture):
    """Function tests deleting an artwork"""

    archive = archive_fixture

    # Collecting sample data
    artwork = single_valid_artwork[0]
    author, title, size, medium, year, filename = artwork

    # Inserting data to QLineEdit
    archive.author_line_edit.setText(author)
    archive.title_line_edit.setText(title)
    archive.size_line_edit.setText(size)
    archive.medium_line_edit.setText(medium)
    archive.year_line_edit.setText(year)

    # Counting rows before addition
    rows_before_addition = archive.model.rowCount()

    # Calling the function
    archive.addArtwork()

    # Counting rows after addition
    rows_after_addition = archive.model.rowCount()

    # Calling the function
    archive.deleteArtwork(0)

    # Counting rows after deletion
    rows_after_deletion = archive.model.rowCount()

    assert rows_before_addition == rows_after_deletion
    assert rows_after_addition == rows_before_addition + 1


def test_delete_artwork_no_selection(archive_fixture):
    """Functions tests if deleting with no selection doesn't create malfunction"""

    archive = archive_fixture

    # Collecting sample data
    artwork = single_valid_artwork[0]
    author, title, size, medium, year, filename = artwork

    rows_before = archive.model.rowCount()

    # Inserting data to QLineEdit
    archive.author_line_edit.setText(author)
    archive.title_line_edit.setText(title)
    archive.size_line_edit.setText(size)
    archive.medium_line_edit.setText(medium)
    archive.year_line_edit.setText(year)

    # Error assertion
    with pytest.raises(IndexError, match="list index out of range"):
        archive.deleteArtwork()

    # Counting rows after addition
    rows_after = archive.model.rowCount()

    assert rows_after == rows_before


def test_delete_multiple_artworks(archive_fixture):
    """Function tests adding a new artwork"""

    archive = archive_fixture

    # Counting rows before addition
    rows_before = archive.model.rowCount()

    # Collecting sample data
    # Adding 1st artwork
    artwork_01 = three_valid_artworks[0]
    author_01, title_01, size_01, medium_01, year_01, filename = artwork_01
    # Inserting data to QLineEdit
    archive.author_line_edit.setText(author_01)
    archive.title_line_edit.setText(title_01)
    archive.size_line_edit.setText(size_01)
    archive.medium_line_edit.setText(medium_01)
    archive.year_line_edit.setText(year_01)
    # Calling the function
    archive.addArtwork()

    # Clearing lines
    archive.author_line_edit.clear()
    archive.title_line_edit.clear()
    archive.size_line_edit.clear()
    archive.medium_line_edit.clear()
    archive.year_line_edit.clear()

    # Adding 2st artwork
    artwork_02 = three_valid_artworks[1]
    author_02, title_02, size_02, medium_02, year_02, filename_02 = artwork_02
    # Inserting data to QLineEdit
    archive.author_line_edit.setText(author_02)
    archive.title_line_edit.setText(title_02)
    archive.size_line_edit.setText(size_02)
    archive.medium_line_edit.setText(medium_02)
    archive.year_line_edit.setText(year_02)
    # Calling the function
    archive.addArtwork()

    # Clearing lines
    archive.author_line_edit.clear()
    archive.title_line_edit.clear()
    archive.size_line_edit.clear()
    archive.medium_line_edit.clear()
    archive.year_line_edit.clear()

    # Adding 3st artwork
    artwork_03 = three_valid_artworks[2]
    author_03, title_03, size_03, medium_03, year_03, filename_03 = artwork_03
    # Inserting data to QLineEdit
    archive.author_line_edit.setText(author_03)
    archive.title_line_edit.setText(title_03)
    archive.size_line_edit.setText(size_03)
    archive.medium_line_edit.setText(medium_03)
    archive.year_line_edit.setText(year_03)
    # Calling the function
    archive.addArtwork()

    # Deleting three artworks

    archive.deleteArtwork(0)
    archive.deleteArtwork(0)
    archive.deleteArtwork(0)

    # Counting rows after addition
    rows_after = archive.model.rowCount()

    # Asserting row count
    assert rows_after == rows_before


# def test_update_artwork(archive_fixture):
#     pass
