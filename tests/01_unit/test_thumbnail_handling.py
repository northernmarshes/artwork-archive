import pytest
from src.archive import Archive
from tests.fixtures.artworks.sample_data import (
    create_test_image,
    single_valid_artwork,
)
from PySide6.QtCore import Qt
from PIL import Image


@pytest.mark.xfail(reason="Feature not implemented")
def test_thumbnail_valid_image(archive_fixture, tmp_path, create_test_image):
    """Function tests if a thumbnail loads with new picture"""

    test_archive = archive_fixture
    test_image = create_test_image

    # Collecting sample data
    artwork = single_valid_artwork[0]

    # Inserting data to QLineEdit
    test_archive.author_line_edit.setText(artwork[0])
    test_archive.title_line_edit.setText(artwork[1])
    test_archive.size_line_edit.setText(artwork[2])
    test_archive.medium_line_edit.setText(artwork[3])
    test_archive.year_line_edit.setText(artwork[4])
    test_archive.filename_edit.setText(str(test_image))

    # Calling the function
    test_archive.addArtwork()

    # Incpecting added image
    thumb_col = test_archive.headers.index("thumbnail")
    item = test_archive.model.item(0, thumb_col)
    pixmap = item.data(Qt.ItemDataRole.DecorationRole)

    # Asserting the thumbnail is being loaded and displayed
    assert pixmap is not None
    assert not pixmap.isNull()
    assert pixmap.height() == 100


def test_thumbnail_nonexistent(archive_fixture):
    """Function tests if thumbnail is not loaded when the file doesn't exist"""

    test_archive = archive_fixture

    # Collecting sample data
    artwork = single_valid_artwork[0]

    # Inserting data to QLineEdit
    test_archive.author_line_edit.setText(artwork[0])
    test_archive.title_line_edit.setText(artwork[1])
    test_archive.size_line_edit.setText(artwork[2])
    test_archive.medium_line_edit.setText(artwork[3])
    test_archive.year_line_edit.setText(artwork[4])
    test_archive.filename_edit.setText("nonexistent.jpg")

    # Calling the function
    test_archive.addArtwork()

    # Incpecting added image
    thumb_col = test_archive.headers.index("thumbnail")
    item = test_archive.model.item(0, thumb_col)
    pixmap = item.data(Qt.ItemDataRole.DecorationRole)

    # Asserting the thumbnail is not being loaded
    assert pixmap is None or pixmap.isNull()


def test_thumbnail_wrongType(archive_fixture, tmp_path):
    """Function tests if thumbnail is not loaded when file is not an image"""

    test_archive = archive_fixture
    txt_path = tmp_path / "test_text.txt"
    txt_path.touch()

    # Collecting sample data
    artwork = single_valid_artwork[0]

    # Inserting data to QLineEdit
    test_archive.author_line_edit.setText(artwork[0])
    test_archive.title_line_edit.setText(artwork[1])
    test_archive.size_line_edit.setText(artwork[2])
    test_archive.medium_line_edit.setText(artwork[3])
    test_archive.year_line_edit.setText(artwork[4])
    test_archive.filename_edit.setText(str(txt_path))

    # Calling the function
    test_archive.addArtwork()

    # Incpecting added image
    thumb_col = test_archive.headers.index("thumbnail")
    item = test_archive.model.item(0, thumb_col)
    pixmap = item.data(Qt.ItemDataRole.DecorationRole)

    # Asserting the thumbnail is not being loaded
    assert pixmap is None or pixmap.isNull()
