import argparse
from typing import List, Optional, Sequence

import ruamel.yaml

yaml = ruamel.yaml.YAML(typ="safe")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--multi",
        "--allow-multiple-documents",
        action="store_true",
    )
    parser.add_argument(
        "-k",
        "--kinds",
        "--banned-kinds",
        default="Secret",
    )
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    args: argparse.Namespace = parser.parse_args(argv)

    kinds: List[str] = [k.lower() for k in args.kinds.split(",")]

    retval: int = 0
    for filename in args.filenames:
        try:
            with open(filename, encoding="UTF-8") as f:
                if args.multi:
                    docs = yaml.load_all(f)
                else:
                    docs = [yaml.load(f)]
                for doc in docs:
                    if isinstance(doc, dict) and doc.get("kind", "").lower() in kinds:
                        print(f"Found {doc['kind']} in {filename}")
                        retval = 1
        except ruamel.yaml.YAMLError as exc:
            print(exc)
            retval = 1
    return retval


if __name__ == "__main__":
    exit(main())
