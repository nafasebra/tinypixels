import os
import sys
import argparse
from pathlib import Path
from PIL import Image

SUPPORTED_FORMATS = {
    '.jpg', '.jpeg', '.png', '.webp',
    '.bmp', '.tiff', '.tif', '.gif',
    '.ico', '.heic', '.heif', '.avif'
}

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def compress_image(img_file: Path, output_path: Path, force_format=None, jpeg_quality=95):
    original_size = img_file.stat().st_size
    suffix = img_file.suffix.lower()

    with Image.open(img_file) as img:
        img.load()
        has_alpha = img.mode in ("RGBA", "LA", "PA") or (
            img.mode == "P" and "transparency" in img.info
        )

        # اگر فرمت اجباری تعیین شده باشد
        if force_format:
            fmt = force_format.lower()

            if fmt == "jpeg" or fmt == "jpg":
                if img.mode != "RGB":
                    img = img.convert("RGB")

                output_file = output_path / (img_file.stem + ".jpg")
                img.save(
                    output_file,
                    format="JPEG",
                    quality=jpeg_quality,
                    optimize=True,
                    subsampling=0,
                    progressive=True,
                )

            elif fmt == "png":
                if img.mode == "P":
                    img = img.convert("RGBA" if has_alpha else "RGB")

                output_file = output_path / (img_file.stem + ".png")
                img.save(
                    output_file,
                    format="PNG",
                    optimize=True,
                    compress_level=9,
                )

            elif fmt == "webp":
                output_file = output_path / (img_file.stem + ".webp")
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA" if has_alpha else "RGB")

                img.save(
                    output_file,
                    format="WEBP",
                    lossless=True,
                    quality=100,
                    method=6,
                )

            else:
                raise ValueError(f"Unsupported forced format: {force_format}")

        else:

            # ── PNG ─────────────────────────
            if suffix == '.png':
                if img.mode == "P":
                    img = img.convert("RGBA" if has_alpha else "RGB")

                output_file = output_path / img_file.name
                img.save(
                    output_file,
                    format="PNG",
                    optimize=True,
                    compress_level=9,
                )

            # ── JPEG ────────────────────────
            elif suffix in ('.jpg', '.jpeg'):
                if img.mode != "RGB":
                    img = img.convert("RGB")

                output_file = output_path / img_file.name
                img.save(
                    output_file,
                    format="JPEG",
                    quality=jpeg_quality,
                    optimize=True,
                    subsampling=0,
                    progressive=True,
                )

            # ── WebP ────────────────────────
            elif suffix == '.webp':
                output_file = output_path / img_file.name
                img.save(
                    output_file,
                    format="WEBP",
                    lossless=True,
                    quality=100,
                    method=6,
                )

            # ── GIF ─────────────────────────
            elif suffix == '.gif':
                output_file = output_path / img_file.name
                frames = []
                try:
                    while True:
                        frames.append(img.copy())
                        img.seek(img.tell() + 1)
                except EOFError:
                    pass

                if len(frames) > 1:
                    frames[0].save(
                        output_file,
                        format="GIF",
                        save_all=True,
                        append_images=frames[1:],
                        optimize=True,
                        loop=img.info.get("loop", 0),
                    )
                else:
                    frames[0].save(output_file, format="GIF", optimize=True)

            # ── ICO ─────────────────────────
            elif suffix == '.ico':
                output_file = output_path / img_file.name
                img.save(output_file, format="ICO")

            # ── سایر → WebP ─────────────────
            else:
                output_file = output_path / (img_file.stem + ".webp")
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA" if has_alpha else "RGB")

                img.save(
                    output_file,
                    format="WEBP",
                    lossless=True,
                    quality=100,
                    method=6,
                )

    compressed_size = output_file.stat().st_size

    if compressed_size >= original_size:
        import shutil
        shutil.copy2(img_file, output_file)
        compressed_size = original_size

    return output_file, original_size, compressed_size


def compress_folder(
    input_folder: str,
    output_folder: str | None = None,
    force_format: str | None = None,
    jpeg_quality: int = 95
):
    input_path = Path(input_folder)

    if not input_path.exists():
        print(f"❌ Folder '{input_folder}' not found!")
        return

    output_path = Path(output_folder) if output_folder else input_path / "web_optimized"
    output_path.mkdir(parents=True, exist_ok=True)

    image_files = [
        f for f in input_path.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS
    ]

    if not image_files:
        print("⚠️ No images found!")
        return

    print(f"✅ {len(image_files)} images found.\n")
    print(f"{'File':<35} {'Format':<8} {'Before':>10} {'After':>10} {'Saved':>8}")
    print("─" * 76)

    total_original = total_compressed = 0
    failed = []

    for img_file in image_files:
        try:
            output_file, orig, comp = compress_image(
                img_file,
                output_path,
                force_format,
                jpeg_quality
            )

            total_original += orig
            total_compressed += comp

            saved = (1 - comp / orig) * 100 if orig > 0 else 0

            print(
                f"{img_file.name:<35} "
                f"{img_file.suffix.lower():<8} "
                f"{format_size(orig):>10} "
                f"{format_size(comp):>10} "
                f"{saved:>7.1f}%"
            )

        except Exception as e:
            failed.append((img_file.name, str(e)))
            print(f"❌ {img_file.name:<33} Error: {e}")

    total_saved = (1 - total_compressed / total_original) * 100 if total_original else 0

    print("─" * 76)
    print(
        f"{'Total':<35} {'':8} "
        f"{format_size(total_original):>10} "
        f"{format_size(total_compressed):>10} "
        f"{total_saved:>7.1f}%"
    )

    if failed:
        print(f"\n⚠️ {len(failed)} files failed to process:")
        for name, err in failed:
            print(f"   • {name}: {err}")

    print(f"\n📁 Output folder: {output_path}")

