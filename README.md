# TinyPixels - A lightweight tool for compressing and optimizing

A fast and simple **command‑line tool for compressing and optimizing images**.  
It scans a folder, compresses supported image formats, and saves optimized versions while preserving visual quality.

The tool can optionally **convert all images to a specific format** (WebP, JPEG, PNG) and generate a detailed compression report.

---

## Features

- Batch image compression
- Supports many common image formats
- Optional **format conversion**
- Adjustable **JPEG quality**
- Optimized settings for each format
- Animated GIF support
- Automatic fallback to **lossless WebP** for unsupported formats
- Skips optimized files if they become larger than the original
- Clean **CLI interface**
- Can be installed globally and used as a command

---

## Supported Formats

```
jpg  jpeg  png  webp
bmp  tiff  tif
gif  ico
heic  heif  avif
```

---

## Installation

### Install from source

Clone the repository:

```
git clone https://github.com/nafasebra/tinypixels
cd tinypixels
```

### Install the package:

```
pip install .
```

For development mode:

```
pip install -e .
```

After installation the global command becomes available:

```
tinypixels
```

---

## Usage

### Basic usage:

```
tinypixels <folder>
```

Example:

```
tinypixels ./images
```

By default optimized images are stored in:

```
web_optimized/
```

inside the input folder.

---

## CLI Options

### Output directory

Specify where optimized images should be saved.

```
tinypixels images --output optimized
```

or

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

Control compression quality for JPEG output.

Default value:

```
95
```

Example:

```
tinypixels images -q 85
```

---

### Combine options

You can combine all options together.

Example:

```
tinypixels images -o output -f jpeg -q 80
```

---

## How It Works

For each image in the folder the tool:

1. Loads the image
2. Detects its format
3. Applies optimized compression settings
4. Saves the result in the output directory

### PNG
- `compress_level=9`
- Full optimization
- Transparency preserved

### JPEG
- Adjustable quality
- `subsampling=0` for better color accuracy
- Progressive encoding enabled

### WebP
- High compression method
- Lossless by default

### GIF
- Preserves animation frames
- Rebuilds optimized GIFs

### Other formats (HEIC, TIFF, BMP…)

Converted to **lossless WebP**.

If the optimized file becomes **larger than the original**, the tool automatically keeps the original instead.

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

## Notes

- Original images are **never overwritten**
- Output files are stored in a separate folder
- Animated GIFs are supported
- Works on **Windows, macOS, and Linux**

---

## Licence

This project uses MIT licence.


## How to Contribute

- **Fork** the repository
- **Create** a new branch for your feature or fix
- **Commit** your changes. Please use standard of commit messaging (such as feat, fix, chore, etc.)
- **Open** a Pull Request

Contributions of any kind are welcome:

- Bug fixes
- Performance improvements
- Documentation updates
- New features
- Code cleanup


---




