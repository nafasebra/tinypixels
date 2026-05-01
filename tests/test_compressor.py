# tests/test_compressor.py
import pytest
from PIL import Image
from tinypixels.compressor import compress_image

def test_jpeg_compression_quality(tmp_path):
    """Test that JPEG quality parameter affects file size"""
    # Create a test image
    img = Image.new('RGB', (100, 100), color='red')
    test_file = tmp_path / "test.jpg"
    img.save(test_file, format='JPEG', quality=100)
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    # Compress with low quality (should be smaller)
    compress_image(test_file, output_dir, jpeg_quality=50)
    compressed_file = output_dir / "test.jpg"
    assert compressed_file.exists()
    assert compressed_file.stat().st_size < test_file.stat().st_size
