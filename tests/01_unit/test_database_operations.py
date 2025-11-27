import pytest
import sqlite3
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    single_valid_artwork,
)


def test_adding_to_database(archive_fixture):
    """Function tests if data is properly saved to database"""

    test_archive = archive_fixture

    rows_before = test_archive.model.rowCount()
    # Collecting sample data
    new_artwork = single_valid_artwork[0]
    author, title, size, medium, year, filename = new_artwork

    # Inserting data to QLineEdit
    test_archive.author_line_edit.setText(author)
    test_archive.title_line_edit.setText(title)
    test_archive.size_line_edit.setText(size)
    test_archive.medium_line_edit.setText(medium)
    test_archive.year_line_edit.setText(year)

    # Calling the function
    test_archive.addArtwork()

    # Counting rows before adding
    rows_after = test_archive.model.rowCount()

    assert rows_after == rows_before + 1

    # Connecting to database and reading added row
    con = sqlite3.connect(test_archive.datapath)
    cur = con.cursor()
    cur.execute("SELECT * FROM ARTWORKS ORDER BY ROWID DESC LIMIT 1")
    lastRow = cur.fetchone()
    con.close()

    # Asserting last row is the added row
    assert lastRow[0] == author


def test_deleting_from_database(archive_fixture):
    """Function tests if data is properly deleted from database"""

    # Creating an instance of Archive with three sample rows
    test_archive = archive_fixture

    # Connecting to the database
    con = sqlite3.connect(test_archive.datapath)
    cur = con.cursor()

    # Counting rows before deleting
    rows_before = test_archive.model.rowCount()

    # Deleting one row
    test_archive.deleteArtwork(0)

    # Counting rows after deleting
    rows_after = test_archive.model.rowCount()

    # Asserting row is deleted
    assert rows_after == rows_before - 1

    # Counting rows in the database
    rows_before_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Saving changes to the database
    test_archive.saveArchive()

    # Counting rows in database after deleting
    rows_after_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Asserting a row is deleted from the database
    assert rows_after_db == rows_before_db - 1
