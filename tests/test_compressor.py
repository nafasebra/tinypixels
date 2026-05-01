import pytest
from pathlib import Path
from PIL import Image
import shutil

from tinypixels.compressor import format_size, compress_image, compress_folder


class TestFormatSize:
    def test_bytes(self):
        assert format_size(500) == "500.0 B"

    def test_kilobytes(self):
        assert format_size(2048) == "2.0 KB"

    def test_megabytes(self):
        assert format_size(5 * 1024 * 1024) == "5.0 MB"

    def test_gigabytes(self):
        assert format_size(3 * 1024 * 1024 * 1024) == "3.0 GB"


class TestCompressImage:
    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path

    @pytest.fixture
    def sample_rgb_image(self, temp_dir):
        img_path = temp_dir / "rgb.jpg"
        img = Image.new("RGB", (100, 100), color="red")
        img.save(img_path, "JPEG")
        return img_path

    @pytest.fixture
    def sample_rgba_image(self, temp_dir):
        img_path = temp_dir / "rgba.png"
        img = Image.new("RGBA", (100, 100), color=(0, 255, 0, 128))
        img.save(img_path, "PNG")
        return img_path

    def test_compress_jpeg(self, temp_dir, sample_rgb_image):
        out_dir = temp_dir / "output"
        out_dir.mkdir()

        output_file, orig_size, comp_size = compress_image(
            sample_rgb_image,
            out_dir,
            force_format=None,
            jpeg_quality=85
        )

        assert output_file.exists()
        assert output_file.suffix == ".jpg"
        assert comp_size > 0

    def test_compress_png(self, temp_dir, sample_rgba_image):
        out_dir = temp_dir / "output"
        out_dir.mkdir()

        output_file, orig_size, comp_size = compress_image(
            sample_rgba_image,
            out_dir,
            force_format=None,
            jpeg_quality=95
        )

        assert output_file.exists()
        assert output_file.suffix == ".png"

        with Image.open(output_file) as img:
            assert img.mode == "RGBA"

    def test_force_jpeg_conversion(self, temp_dir, sample_rgba_image):
        out_dir = temp_dir / "output"
        out_dir.mkdir()

        output_file, orig_size, comp_size = compress_image(
            sample_rgba_image,
            out_dir,
            force_format="jpeg",
            jpeg_quality=85
        )

        assert output_file.exists()
        assert output_file.suffix == ".jpg"

        with Image.open(output_file) as img:
            assert img.mode == "RGB"

    def test_force_webp_conversion(self, temp_dir, sample_rgb_image):
        out_dir = temp_dir / "output"
        out_dir.mkdir()

        output_file, orig_size, comp_size = compress_image(
            sample_rgb_image,
            out_dir,
            force_format="webp",
            jpeg_quality=95
        )

        assert output_file.exists()
        assert output_file.suffix == ".webp"

    def test_force_png_conversion(self, temp_dir, sample_rgb_image):
        out_dir = temp_dir / "output"
        out_dir.mkdir()

        output_file, orig_size, comp_size = compress_image(
            sample_rgb_image,
            out_dir,
            force_format="png",
            jpeg_quality=95
        )

        assert output_file.exists()
        assert output_file.suffix == ".png"


class TestCompressFolder:
    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path

    @pytest.fixture
    def sample_rgb_image(self, temp_dir):
        img_path = temp_dir / "rgb.jpg"
        img = Image.new("RGB", (100, 100), color="blue")
        img.save(img_path, "JPEG")
        return img_path

    def test_empty_folder(self, temp_dir, capsys):
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()

        compress_folder(str(empty_dir))

        captured = capsys.readouterr()
        assert "No images found" in captured.out

    def test_folder_with_images(self, temp_dir, sample_rgb_image, capsys):
        # Execute the function on the directory containing the test file
        compress_folder(str(temp_dir))

        # Verify that the default 'web_optimized' output folder is created
        out_dir = temp_dir / "web_optimized"
        assert out_dir.exists(), "Default 'web_optimized' folder was not created."

        # Check if the optimized file is successfully placed in the output directory
        optimized_image = out_dir / sample_rgb_image.name
        assert optimized_image.exists(), "Optimized image was not found in the output folder."

        # Ensure that the successful output is printed to the terminal
        # (You can adapt this based on the exact string printed in compressor.py)
        captured = capsys.readouterr()
        assert str(sample_rgb_image.name) in captured.out

    def test_folder_with_custom_output(self, temp_dir, sample_rgb_image):
        # Test behavior when the user specifies a custom output directory
        custom_out_dir = temp_dir / "my_custom_build"
        
        compress_folder(str(temp_dir), output_folder=str(custom_out_dir))
        
        assert custom_out_dir.exists(), "Custom output directory was not created."
        
        optimized_image = custom_out_dir / sample_rgb_image.name
        assert optimized_image.exists(), "File was not saved in the custom output directory."
