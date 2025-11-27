import pytest
import sqlite3
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    single_valid_artwork,
    three_valid_artworks,
)


def test_crud_with_database(archive_fixture):
    """Function tests integration of adding, reading, deleting and saving"""

    # -------------ADDING------------------

    # Setting up an instance with three sample rows
    test_archive = archive_fixture

    # Connecting to databese
    con = sqlite3.connect(test_archive.datapath)
    cur = con.cursor()

    # Counting rows in the database
    rows_01_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Counting rows in the model
    rows_01 = test_archive.model.rowCount()

    # Collecting data
    author, title, size, medium, year, thumbnail = single_valid_artwork[0]

    # Inputing data to line edits
    test_archive.author_line_edit.setText(author)
    test_archive.title_line_edit.setText(title)
    test_archive.size_line_edit.setText(size)
    test_archive.medium_line_edit.setText(medium)
    test_archive.year_line_edit.setText(year)

    # Calling the add function
    test_archive.addArtwork()

    # Counting rows in the model
    rows_02 = test_archive.model.rowCount()

    # Asserting new row was added to the model
    assert rows_02 == rows_01 + 1

    # Calling the save function
    test_archive.saveArchive()

    # Counting rows in the database
    rows_02_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Asserting rows in database increased
    assert rows_02_db == rows_01_db + 1

    # ------------READING-----------------

    # Collecting data suppoused to be in the model
    sampleNames = []
    for item in three_valid_artworks:
        sampleNames.append(item[0])
    for item in single_valid_artwork:
        sampleNames.append(item[0])

    # Reading from the model
    readNames = []
    for i in range(test_archive.proxy_model.rowCount()):
        readNames.append(test_archive.model.item(i).text())

    # Asserting uniformity
    assert set(sampleNames) == set(readNames)

    # -----------FILTERING----------------

    # Counting rows in proxy model before filtering
    rows_before_proxy = test_archive.proxy_model.rowCount()

    # Filtering
    test_archive.searchbar.setText(author)

    # Counting rows in proxy model after filtering
    rows_after_proxy = test_archive.proxy_model.rowCount()

    # Asserting row count after filtering
    assert rows_after_proxy != rows_before_proxy
    assert rows_after_proxy == 1

    # Clearing the searchbar
    test_archive.searchbar.clear()

    # -----------DELETING----------------

    test_archive.deleteArtwork(0)

    # Counting rows in the model
    rows_03 = test_archive.model.rowCount()

    # Asserting new row was added to the model
    assert rows_03 == rows_02 - 1

    # Calling the save function
    test_archive.saveArchive()

    # Counting rows in the database
    rows_03_db = cur.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]

    # Asserting rows in database increased
    assert rows_03_db == rows_02_db - 1
