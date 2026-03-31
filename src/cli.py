import argparse

try:
    # when installed as package
    from .compressor import compress_folder
except ImportError:
    # when running the file directly
    from compressor import compress_folder


def main():
    parser = argparse.ArgumentParser(
        description="Tinypixels — A lightweight tool to optimize images"
    )

    parser.add_argument("folder", help="Folder containing images")
    parser.add_argument(
        "-o", "--output",
        help="Output directory for optimized images"
    )

    parser.add_argument(
        "-f", "--format",
        choices=["webp", "jpeg", "jpg", "png"],
        help="Force output format"
    )

    parser.add_argument(
        "-q", "--quality",
        default=95,
        type=int,
        help="JPEG quality (default: 95)"
    )

    args = parser.parse_args()

    compress_folder(
        args.folder,
        output=args.output,
        force_format=args.format,
        quality=args.quality,
    )


# allow running directly
if __name__ == "__main__":
    main()
