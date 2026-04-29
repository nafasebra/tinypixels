import pytest
from pathlib import Path
from PIL import Image
import shutil
import tempfile
from compressor import (
    format_size,
    compress_image,
    compress_folder,
    SUPPORTED_FORMATS,
)


# ----------------------------------
# format_size tests
# ----------------------------------

class TestFormatSize:
    def test_bytes(self):
        assert format_size(500) == "500.0 B"

    def test_kb(self):
        assert format_size(1024) == "1.0 KB"

    def test_mb(self):
        assert format_size(1024 * 1024) == "1.0 MB"

    def test_gb(self):
        assert format_size(1024 * 1024 * 1024) == "1.0 GB"

    def test_tb(self):
        assert format_size(1024**4) == "1.0 TB"

    def test_fraction(self):
        assert format_size(1536) == "1.5 KB"


# ----------------------------------
# Fixtures
# ----------------------------------

@pytest.fixture
def temp_dir():
    path = Path(tempfile.mkdtemp())
    yield path
    shutil.rmtree(path)


@pytest.fixture
def sample_rgb_image(temp_dir):
    img_path = temp_dir / "rgb.jpg"
    img = Image.new("RGB", (100, 100), "red")
    img.save(img_path, "JPEG")
    return img_path


@pytest.fixture
def sample_rgba_image(temp_dir):
    img_path = temp_dir / "rgba.png"
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
    img.save(img_path, "PNG")
    return img_path


@pytest.fixture
def sample_gif_image(temp_dir):
    img_path = temp_dir / "test.gif"
    img = Image.new("RGB", (50, 50), "blue")
    img.save(img_path, "GIF")
    return img_path


# ----------------------------------
# compress_image tests
# ----------------------------------

class TestCompressImage:
    def test_jpeg_default(self, sample_rgb_image, temp_dir):
        out = temp_dir / "out"
        out.mkdir()

        output_file, orig, comp = compress_image(sample_rgb_image, out)

        assert output_file.exists()
        assert output_file.suffix == ".jpg"
        assert orig > 0
        assert comp > 0

    def test_png_default(self, sample_rgba_image, temp_dir):
        out = temp_dir / "out"
        out.mkdir()

        output_file, orig, comp = compress_image(sample_rgba_image, out)

        assert output_file.exists()
        assert output_file.suffix == ".png"

    def test_force_webp(self, sample_rgb_image, temp_dir):
        out = temp_dir / "out"
        out.mkdir()

        output_file, _, _ = compress_image(
            sample_rgb_image, out, force_format="webp"
        )

        assert output_file.exists()
        assert output_file.suffix == ".webp"

    def test_force_jpeg_conversion(self, sample_rgba_image, temp_dir):
        out = temp_dir / "out"
        out.mkdir()

        output_file, _, _ = compress_image(
            sample_rgba_image, out, force_format="jpeg"
        )

        assert output_file.exists()
        assert output_file.suffix == ".jpg"

        with Image.open(output_file) as img:
            assert img.mode == "RGB"

    def test_force_png(self, sample_rgba_image, temp_dir):
        out = temp_dir / "out"
        out.mkdir()

        output_file, _, _ = compress_image(
            sample_rgba_image, out, force_format="png"
        )

        assert output_file.exists()
        assert output_file.suffix == ".png"

    def test_unsupported_forced_format(self, sample_rgb_image, temp_dir):
        out = temp_dir / "out"
        out.mkdir()

        with pytest.raises(ValueError):
            compress_image(sample_rgb_image, out, force_format="xyz")


# ----------------------------------
# compress_folder tests
# ----------------------------------

class TestCompressFolder:
    def test_folder_not_found(self, capsys):
        compress_folder("non_existing_folder")
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_empty_folder(self, temp_dir, capsys):
        compress_folder(str(temp_dir))
        captured = capsys.readouterr()
        assert "no images" in captured.out.lower()

    def test_folder_with_images(self, temp_dir, sample_rgb_image, sample_png=None):
        img_dir = temp_dir / "images"
        img_dir.mkdir()
        shutil.copy2(sample_rgb_image, img_dir / sample_rgb_image.name)

        out_dir = temp_dir / "optimized"

        compress_folder(str(img_dir), output_folder=str(out_dir))

        assert out_dir.exists()
        assert any(
            f.suffix.lower() in SUPPORTED_FORMATS
            for f in out_dir.iterdir()
        )

    def test_force_format_folder(self, temp_dir, sample_rgb_image):
        img_dir = temp_dir / "images"
        img_dir.mkdir()

        shutil.copy2(sample_rgb_image, img_dir / sample_rgb_image.name)

        out_dir = temp_dir / "opt"

        compress_folder(str(img_dir), output_folder=str(out_dir), force_format="webp")

        assert any(f.suffix == ".webp" for f in out_dir.iterdir())


# ----------------------------------
# CLI tests (optional)
# ----------------------------------
def test_cli_basic(monkeypatch, temp_dir, sample_rgb_image, capsys):
    img_dir = temp_dir / "cliimg"
    img_dir.mkdir()
    shutil.copy2(sample_rgb_image, img_dir / sample_rgb_image.name)

    from cli import main

    monkeypatch.setattr(
        "sys.argv",
        ["cli.py", str(img_dir), "-o", str(temp_dir / "out")]
    )

    main()

    captured = capsys.readouterr()
    assert "images found" in captured.out.lower()
