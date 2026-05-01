import argparse

try:
    from .compressor import compress_folder
except ImportError:
    from compressor import compress_folder


def get_parser():
    """Create and return the argument parser."""
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
    return parser


def parse_args(args=None):
    """Parse command line arguments. Useful for testing."""
    parser = get_parser()
    return parser.parse_args(args)


def main():
    args = parse_args()
    compress_folder(
        args.folder,
        output_folder=args.output,
        force_format=args.format,
        jpeg_quality=args.quality,
    )


if __name__ == "__main__":
    main()
