import pytest
import sqlite3
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    single_valid_artwork,
)


def test_datapersistance(tmp_path, qtbot):
    """Function tests data persistance when closing the application"""

    # -----------SESSION-01----------------
    # -------------ADDING------------------

    # Setting up an instance with three sample rows
    test_db = tmp_path / "test.db"
    test_archive_01 = Archive(datapath=test_db)
    qtbot.addWidget(test_archive_01)

    # Connecting to databese
    con = sqlite3.connect(test_archive_01.datapath)
    cur = con.cursor()

    # Counting rows in the database
    rows_01_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Counting rows in the model
    rows_01 = test_archive_01.model.rowCount()

    # Collecting data
    author, title, size, medium, year, thumbnail = single_valid_artwork[0]

    # Inputing data to line edits
    test_archive_01.author_line_edit.setText(author)
    test_archive_01.title_line_edit.setText(title)
    test_archive_01.size_line_edit.setText(size)
    test_archive_01.medium_line_edit.setText(medium)
    test_archive_01.year_line_edit.setText(year)

    # Calling the add function
    test_archive_01.addArtwork()

    # Counting rows in the model
    rows_02 = test_archive_01.model.rowCount()

    # Asserting new row was added to the model
    assert rows_02 == rows_01 + 1

    # Calling the save function
    test_archive_01.saveArchive()

    # Counting rows in the database
    rows_02_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Asserting rows in database increased
    assert rows_02_db == rows_01_db + 1

    # Simulate turning off the application
    del test_archive_01

    # Asserting first instance is down
    assert "test_archive_01" not in locals()

    # -----------SESSION-02----------------

    test_archive_02 = Archive(datapath=test_db)

    # Counting rows in the model
    rows_03 = test_archive_02.model.rowCount()

    # Counting rows in the database
    rows_03_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Checking if data stayed
    assert rows_03 == rows_02
    assert rows_03_db == rows_02_db

    # -----------DELETING----------------

    test_archive_02.deleteArtwork(0)

    # Counting rows in the model
    rows_04 = test_archive_02.model.rowCount()

    # Asserting new row was added to the model
    assert rows_04 == rows_03 - 1

    # Calling the save function
    test_archive_02.saveArchive()

    # Counting rows in the database
    rows_04_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Asserting rows in database deceased
    assert rows_04_db == rows_03_db - 1

    # Simulate turning off the application
    del test_archive_02

    # Asserting first instance is down
    assert "test_archive_02" not in locals()

    # -----------SESSION-03----------------

    test_archive_03 = Archive(datapath=test_db)

    # Counting rows in the model
    rows_05 = test_archive_03.model.rowCount()

    # Counting rows in the database
    rows_05_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Checking if data stayed
    assert rows_05 == rows_04
    assert rows_05_db == rows_04_db

    # ---------CLOSING-CONNECTION----------

    con.close()

    # Simulate turning off the application
    del test_archive_03

    # Asserting first instance is down
    assert "test_archive_03" not in locals()
