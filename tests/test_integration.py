# tests/test_integration.py
from PIL import Image
from tinypixels.compressor import compress_folder

def test_compress_folder_end_to_end(tmp_path):
    # Create test image
    img = Image.new('RGB', (100, 100), color='blue')
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    img.save(input_dir / "test.jpg")
    
    output_dir = tmp_path / "output"
    compress_folder(input_dir, output_dir)
    
    # Verify output exists
    assert (output_dir / "test.jpg").exists()
