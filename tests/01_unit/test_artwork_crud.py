import pytest
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    single_valid_artwork,
    three_valid_artworks,
    single_invalid_year,
)

# ----------------------------------------
# ----- TESTING-THE-HAPPY-PATH------------
# ----------------------------------------


# --- CREATE ---
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


# def test_update_artwork(archive_fixture):
#     pass


# --- DELETE ---
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
