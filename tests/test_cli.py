import sys
import pytest
from tinypixels import cli

def test_cli_parser():
    test_args = ["program", "test_folder", "-o", "output", "-f", "webp", "-q", "85"]
    with pytest.MonkeyPatch.context() as m:
        m.setattr(sys, "argv", test_args)
        args = cli.parse_args()   # Now works after adding parse_args to cli.py
    assert args.folder == "test_folder"
    assert args.output == "output"
    assert args.format == "webp"
    assert args.quality == 85
