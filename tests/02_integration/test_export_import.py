import pytest
import sqlite3
from src.archive import Archive
from tests.fixtures.helpers.db_utils import populated_database


@pytest.mark.xfail(reason="Feature not implemented")
def test_export_database(archive_fixture, tmp_path):
    """Tests exporting database for backup and migration"""

    # Creating an instance of archive with 3 sample rows
    test_archive = archive_fixture

    # Creating path for exporting test database
    export_path = tmp_path / "backup.db"

    # Calling export function
    test_archive.exportDatabase(export_path)

    # Checking if file is being created
    assert export_path.exists()

    # Opening file
    with sqlite3.connect(export_path) as con:
        count = con.execute("SELECT COUNT(*) FROM ARTWORKS").fetchone()[0]
        assert count == 3


@pytest.mark.xfail(reason="Feature not implemented")
def test_import_database(archive_fixture, populated_database):
    """Tests importing database for backup and migration"""

    # Creating an instance of archive with 3 sample rows
    test_archive = archive_fixture

    test_db_path = populated_database

    # Calling import function
    test_archive.importDatabase(test_db_path)

    rowcount = test_archive.model.rowCount()

    assert rowcount == 100
