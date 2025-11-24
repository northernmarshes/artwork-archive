import pytest
from src.archive import Archive


@pytest.fixture
def archive_fixture(tmp_path, qtbot):
    "The fixture prepers an instance of Archive with isolated, temporary database"

    # Creating path for test database
    test_db = tmp_path / "test.db"

    # Creating an instance of Archive with test_db as database
    archive = Archive(datapath=test_db)

    # Adding a widget to qtbot - for GUI test_db
    qtbot.addWidget(archive)

    # Returning widget for test_db
    return archive
