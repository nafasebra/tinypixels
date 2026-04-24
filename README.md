# TinyPixels

A fast and lightweight **command‑line tool for compressing and optimizing images in bulk**.

TinyPixels scans a folder, compresses supported image formats, and saves optimized versions while preserving visual quality.  
It can also **convert images to a specific format** such as WebP, JPEG, or PNG.

Designed to be simple, fast, and useful for developers preparing images for the web.

---

## Features

- Fast **batch image compression**
- Supports many common image formats
- Optional **format conversion** (WebP / JPEG / PNG)
- Adjustable **JPEG quality**
- Optimized compression settings for each format
- Animated **GIF support**
- Automatic fallback to **lossless WebP** for unsupported formats
- Skips files when the compressed version becomes larger
- Generates a **compression summary report**
- Clean and simple **CLI interface**

---

## Supported Formats

TinyPixels supports most commonly used image formats:

```
jpg   jpeg   png   webp
bmp   tiff   tif
gif   ico
heic  heif   avif
```

Some formats may be converted internally before compression.

---

## Installation

### Requirements

- Python **3.9+**
- `pip`

Check your Python version:

```
python --version
```

---

### Install with pipx (Recommended)

`pipx` installs CLI tools in isolated environments and makes them available globally.

Install pipx:

```
pip install pipx
pipx ensurepath
```

Then install TinyPixels directly from GitHub:

```
pipx install git+https://github.com/nafasebra/tinypixels.git
```

After installation, the `tinypixels` command will be available globally.

---

### Install from Source

Clone the repository:

```
git clone https://github.com/nafasebra/tinypixels
cd tinypixels
```

Install the package:

```
pip install .
```

For development (editable install):

```
pip install -e .
```

If you prefer pipx for development:

```
pipx install .
```

---

## Quick Start

Compress all images inside a folder:

```
tinypixels ./images
```

TinyPixels will create an output folder automatically and save optimized images there.

---

## CLI Usage

```
tinypixels <input_path> [options]
```

Example:

```
tinypixels images -o output -f webp -q 85
```

---

## Options

### Output directory

Specify where optimized images should be saved.

```
tinypixels images --output optimized
```

Short version:

```
tinypixels images -o optimized
```

---

### Force output format

Convert all images to a specific format.

Supported formats:

```
webp
jpeg / jpg
png
```

Example:

```
tinypixels images -f webp
```

---

### JPEG quality

Control JPEG compression quality.

Default:

```
95
```

Example:

```
tinypixels images -q 85
```

---

## Output Behavior

By default, optimized images are stored in:

```
web_optimized/
```

This folder is created inside the input directory.

Example structure:

```
images/
│
├─ photo1.jpg
├─ photo2.png
│
└─ web_optimized/
   ├─ photo1.jpg
   └─ photo2.png
```

Original images are **never overwritten**.

---

## How TinyPixels Works

For every image in the input folder:

1. The image is loaded.
2. The format is detected.
3. Format‑specific compression settings are applied.
4. The optimized image is saved to the output folder.

If the optimized image becomes **larger than the original**, the original file is kept instead.

---

## Compression Settings

#### PNG
- `compress_level=9`
- Maximum optimization
- Transparency preserved

#### JPEG
- Adjustable quality
- `subsampling=0` for better color accuracy
- Progressive encoding

#### WebP
- High compression method
- Lossless when appropriate

#### GIF
- Animation frames preserved
- Rebuilt optimized GIF

#### Other formats (HEIC, TIFF, BMP...)

Converted to **lossless WebP** before saving.

---

## Example Output

```
8 images found.

File                               Format      Before       After    Saved
----------------------------------------------------------------------------
photo1.png                         .png        3.5 MB      2.1 MB    40.3%
photo2.jpg                         .jpg        1.2 MB      1.0 MB    16.7%
graphic.webp                       .webp       800 KB      620 KB    22.5%
----------------------------------------------------------------------------
Total                              —           12.4 MB     7.8 MB    37.1%

Output folder: ./images/web_optimized
```

---

## Platform Support

TinyPixels works on:

- Windows
- macOS
- Linux

---

## Contributing

Contributions are welcome.

Typical workflow:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

Examples of contributions:

- Bug fixes
- Performance improvements
- Documentation updates
- New features

Please use conventional commit messages:

```
feat:
fix:
docs:
refactor:
chore:
```

---

## License

This project is licensed under the **MIT License**.

---
