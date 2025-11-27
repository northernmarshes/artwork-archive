import pytest
from src.archive import Archive


@pytest.fixture
def archive_fixture(tmp_path, qtbot):
    "Fixture prepers an instance of Archive with isolated, temporary database"

    # Creating path for test database
    test_db = tmp_path / "test.db"

    # Creating an instance of Archive with test_db as database
    archive = Archive(datapath=test_db)

    # Adding a widget to qtbot - for GUI test_db
    qtbot.addWidget(archive)

    # Returning widget for test_db
    return archive


@pytest.fixture
def archive_with_custom_data(tmp_path, qtbot, monkeypatch):
    """Fixture that provides an instance of Archive with custom data"""

    # Patching initial data with monkeypatch
    def _create_archive(test_data):
        monkeypatch.setattr("src.archive.three_valid_artworks", test_data)

        # Setting up clean database
        test_db = tmp_path / "test.db"
        if test_db.exists():
            test_db.unlink()

        # Creating an instance with patched data
        archive = Archive(datapath=test_db)
        qtbot.addWidget(archive)
        return archive

    return _create_archive
