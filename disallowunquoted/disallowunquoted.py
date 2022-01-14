import argparse
import re
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--values",
        default="y,n,yes,no,on,off",
    )
    parser.add_argument("--case-sensitive", dest="case_sensitive", action="store_true")
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    args: argparse.Namespace = parser.parse_args(argv)

    values: str = "|".join([val.lower() for val in args.values.split(",")])

    flags: int = re.IGNORECASE
    if args.case_sensitive:
        flags = 0
        print("here")

    regex: re.Pattern = re.compile(
        r""":\s+(?:(?:"""
        + values
        + r""")(?:['"]|\s|$)|(?:['"](?:"""
        + values
        + r""")(?:[^\w'"]|$)))""",
        flags,
    )

    retval: int = 0
    for filename in args.filenames:
        try:
            with open(filename, encoding="UTF-8") as f:
                idx: int = 0
                for line in f:
                    idx += 1
                    match: re.Match = regex.search(line)
                    if match:
                        print(
                            f"{filename}: Restricted value found on line {idx} at column {match.span(0)[0]} {match.group(0).rstrip()}"
                        )
                        retval = 1
        except OSError as exc:
            print(exc)
            retval = 1
    return retval


if __name__ == "__main__":
    exit(main())
