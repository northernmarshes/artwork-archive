import pytest
from PIL import Image

single_valid_artwork = [
    (
        "Emily Turner",
        "Silent Horizon",
        "90x90cm",
        "Acrylic on Canvas",
        "2025",
        "sample5.jpg",
    )
]

single_empty_artwork_data = [
    (
        "",
        "",
        "",
        "",
        "",
        "",
    )
]

three_valid_artworks = [
    ("Jane Smith", "Abstract 1", "100x100cm", "Acrylic", "2024", "sample1.jpg"),
    ("John Doe", "Landscape", "80x60cm", "Oil", "2023", "sample2.jpg"),
    ("Alice Brown", "Portrait", "50x70cm", "Watercolor", "2024", "sample3.jpg"),
]

single_invalid_year = [
    (
        "Rose Black",
        "Cold Sunday",
        "20x40cm",
        "Acrylic on Canvas",
        "Two Thousand",
        "sample25.jpg",
    )
]

three_special_chars_artworks_data = [
    (
        "山田太郎",
        "春の風景",
        "100×100cm",
        "アクリル絵具",
        "2024",
        "path.jpg",
    ),
    ("أحمد العلي", "مشهد الغروب", "٨٠×٦٠ سم", "زيت", "2024", "path.jpg"),
    (
        "Mårten Ødegård",
        "Unicode Dreams",
        "50×70㎝",
        "𝕬𝖗𝖙 𝕸𝖎𝖝",
        "2024",
        "path.jpg",
    ),
]


@pytest.fixture
def three_special_chars_artworks():
    return three_special_chars_artworks_data


@pytest.fixture
def single_empty_artwork():
    return single_empty_artwork_data


@pytest.fixture
def create_test_image(tmp_path, name="test_img.jpg"):
    test_img = Image.new("RGB", (100, 300), color="blue")
    img_path = tmp_path / name
    test_img.save(img_path)
    return img_path
