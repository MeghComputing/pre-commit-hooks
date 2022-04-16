#!/usr/bin/env python3

# Copyright (c) 2022 Megh Computing, Inc.

# All rights reserved. No warranty, explicit or implied, provided.
# Unauthorized use, modification, or distribution is strictly prohibited.

import argparse
import datetime
import os
import re
import sys
import typing

# Constants.
default_extensions = (".c", ".cpp", ".cs", ".css", ".h", ".hpp", ".java", ".js", ".php", ".py")

# Globals.
g_verbose = False


def read_tombstone(file: typing.TextIO, max_lines: int = 9) -> str:
    """Extract and return the tombstone from the file."""
    lines = ""
    for _ in range(max_lines):
        line = file.readline()
        if not line:
            break
        lines += line

    return lines


def read_file(filepath: str) -> list:
    """Useful for unit testing."""
    with open(filepath, "r") as file:
        return file.readlines()


def write_file(filepath: str, lines: list) -> None:
    """Useful for unit testing."""
    with open(filepath, "w") as file:
        file.writelines(lines)


def write_current_year(filepath: str, start_year: int, current_year: int):
    lines = read_file(filepath)

    # The subbing RE has to work for Megh and Apache.
    copyright_regex = R" 20\d\d(-20\d\d)? Megh Computing, Inc."
    copyright_replace = " {0}-{1} Megh Computing, Inc."

    regex = re.compile(copyright_regex)
    for i, line in enumerate(lines):
        match = regex.search(line)
        if match:
            to_write = lines[:]
            to_write[i] = regex.sub(copyright_replace.format(start_year, current_year), line)
            # Write out.
            write_file(filepath, to_write)
            return
    raise AssertionError()


def parse_copyright_megh(lines: str) -> tuple:
    copyright_regex_megh = R"Copyright \(c\) 20\d\d(-20\d\d)? Megh Computing, Inc."
    match = re.search(copyright_regex_megh, lines)
    if not match:
        return None, None

    start_year = int(match.group()[14:18])
    end_year = int(match.group()[-25:-21])

    return start_year, end_year


def parse_copyright_apache(lines: str) -> tuple:
    copyright_regex_apache = R"Copyright 20\d\d(-20\d\d)? Megh Computing, Inc."
    match = re.search(copyright_regex_apache, lines)
    if not match:
        return None, None

    start_year = match.group()[10:14]
    end_year = match.group()[-25:-21]

    return int(start_year), int(end_year)


def check_file(extensions: list, filepath: str, autofix: bool) -> bool:
    if not os.path.isfile(filepath):
        print(f"File does not exist: {filepath}")
        return False

    ext = os.path.splitext(filepath)[1]
    if ext not in extensions:
        if g_verbose:
            print(f"File extension not on to-check list: {filepath} (automatic success)")
        return True

    # Read the file's tombstone.
    try:
        with open(filepath, "r") as file:
            lines = read_tombstone(file)
    except FileNotFoundError as e:
        print(str(e))
        return False

    # Locate the copyright year.
    # Note: We chose not to support commas. Only YYYY and YYYY-YYYY are supported.
    if re.search(R"Licensed under the Apache License, Version 2", lines):
        # Special case for Apache license.
        start_year, end_year = parse_copyright_apache(lines)
    else:
        start_year, end_year = parse_copyright_megh(lines)

    if not start_year or not end_year:
        print(f"Copyright header check failed for file: {filepath}")
        print("Copyright message not found in file header.")
        print_lines = lines.split("\n")
        print_lines = "\n    > ".join(print_lines)  # type: ignore  # mypy confused about type
        print_lines = "    > " + print_lines  # type: ignore
        print(f"Beginning of file:\n{print_lines}")
        return False

    # Verify the given copyright year is the current year.
    current_year = datetime.date.today().year

    if start_year > current_year:
        print(f"Copyright header check failed for file: {filepath}")
        print(f"File header copyright start year {start_year} is in the future.")
        return False

    if start_year > end_year:
        print(f"Copyright header check failed for file: {filepath}")
        print(f"File header copyright start year {start_year} must be smaller than end year {end_year}.")
        return False

    if end_year != current_year:
        print(f"Copyright header check failed for file: {filepath}")
        print(f"File header copyright year {end_year} does not match current year {current_year}.")
        if not autofix:
            return False
        else:
            print(f"File will be overwritten with the correct year: {filepath}")
            write_current_year(filepath, start_year, current_year)
            # Return false if a file was modified.
            return False

    return True


def get_extensions(extensions_file: str) -> list:
    # Load extensions from file if filename is given.
    if not extensions_file:
        return list(default_extensions)

    extensions_file = os.path.abspath(extensions_file)

    try:
        file_lines = read_file(extensions_file)
        extensions = [line.strip() for line in file_lines]
        extensions = [e for e in extensions if e]  # Remove empties.
    except FileNotFoundError as e:
        print(str(e))
        return []

    # Check extensions formatting.
    for ext in extensions:
        match = re.search(R"\A\.\w*\Z", ext.strip())
        if not match:
            print(f'When reading extensions file "{extensions_file}", found bad extension "{ext}"')
            return []

    if len(extensions) == 0:
        print(f"No file extensions found in the given extensions check file: {extensions_file}")
        return []

    return extensions


def check_all(extensions_file: str, filenames: list, autofix: bool) -> bool:
    extensions = get_extensions(extensions_file)
    if not extensions:
        return False

    # Check each file.
    failed_paths = []
    for rel_path in filenames:
        path = os.path.abspath(rel_path)
        if not check_file(extensions, path, autofix):
            failed_paths.append(path)
            print()

    if g_verbose:
        if failed_paths:
            print("Files failed:")
            for path in failed_paths:
                print(f"    {path}")

        print(f"{len(failed_paths)}/{len(filenames)} files failed.\n")

    if failed_paths:
        return False
    return True


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify the copyright tombstone in a file.",
        epilog=f"You ran with Python {sys.version}.",
    )
    parser.add_argument(
        "-f",
        "--fix",
        action="store_true",
        help="If given, automatically update the copyright year to the current year.",
    )
    parser.add_argument("filename", help="The path(s) of the file(s) to check.", nargs="+", default=[])
    parser.add_argument("-v", "--verbose", action="store_true", help="Print more context.")
    parser.add_argument(
        "-e",
        "--extensions",
        default=None,
        help="The path of a file with a list of extensions to check.\nDefaults: {', '.join(default_extensions)}.",
    )
    return parser


def main() -> int:
    # Parse the arguments.
    parser = make_parser()
    args = parser.parse_args()

    global g_verbose
    if args.verbose:
        g_verbose = True

    if check_all(args.extensions, args.filename, args.fix):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
