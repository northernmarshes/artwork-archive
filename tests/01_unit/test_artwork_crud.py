import pytest
from src.archive import Archive


def test_add_artwork(archive_fixture):
    # Inserting data to QLineEdit
    archive = archive_fixture
    archive.author_line_edit.setText("test")
    archive.title_line_edit.setText("test")
    archive.size_line_edit.setText("test")
    archive.medium_line_edit.setText("test")
    archive.year_line_edit.setText("test")

    # Counting rows before addition
    rows_before = archive.model.rowCount()

    # Calling the function
    archive.addArtwork()

    # Counting rows after addition
    rows_after = archive.model.rowCount()

    # Asserting row count
    assert rows_after == rows_before + 1
