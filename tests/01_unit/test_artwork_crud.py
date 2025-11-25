import pytest
from src.archive import Archive
from src.database.sample_data import single_artwork


def test_add_artwork(archive_fixture):
    """Function tests adding a new artwork"""
    # Collecting sample data
    artwork = single_artwork[0]
    author, title, size, medium, year, filename = artwork
    archive = archive_fixture

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


def test_delete_artwork(archive_fixture):
    """Function tests deleting an artwork"""
    # Adding an artwork

    # Collecting sample data
    artwork = single_artwork[0]
    author, title, size, medium, year, filename = artwork
    archive = archive_fixture

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
