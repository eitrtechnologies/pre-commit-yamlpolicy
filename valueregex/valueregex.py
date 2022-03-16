import argparse
import re
from typing import List, Optional, Sequence

import jmespath
import ruamel.yaml

yaml = ruamel.yaml.YAML(typ="safe")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(add_help=False)
    required: argparse.ArgumentGroup = parser.add_argument_group("required arguments")
    optional: argparse.ArgumentGroup = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="show this help message and exit",
    )
    optional.add_argument(
        "-m",
        "--multi",
        "--allow-multiple-documents",
        action="store_true",
    )
    required.add_argument(
        "-r",
        "--regex",
        required=True,
    )
    required.add_argument(
        "-j",
        "--jmespath",
        required=True,
    )
    required.add_argument("filenames", nargs="*", help="Filenames to check.")
    args: argparse.Namespace = parser.parse_args(argv)

    regex: re.Pattern = re.compile(args.regex)
    search: str = args.jmespath

    retval: int = 0
    for filename in args.filenames:
        try:
            with open(filename, encoding="UTF-8") as f:
                if args.multi:
                    docs = yaml.load_all(f)
                else:
                    docs = [yaml.load(f)]
                for doc in docs:
                    for val in jmespath.search(search, doc) or []:
                        match: re.Match = regex.search(val)
                        if match:
                            print(
                                f'{filename}: Restricted value found for JMESPath "{search}" =  {match.group(0).rstrip()}'
                            )
                            retval = 1
        except ruamel.yaml.YAMLError as exc:
            print(exc)
            retval = 1
        except jmespath.exceptions.ParseError as exc:
            print(exc)
            retval = 1
        except TypeError:
            print(
                "JMESPath expression returned non-string values. Ensure your expression returns a flat list of strings."
            )
            retval = 1
    return retval


if __name__ == "__main__":
    exit(main())
