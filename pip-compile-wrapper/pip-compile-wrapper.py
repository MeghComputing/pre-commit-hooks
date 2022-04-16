#!/usr/bin/env python

# Copyright (c) 2022 Megh Computing, Inc.

# All rights reserved. No warranty, explicit or implied, provided.
# Unauthorized use, modification, or distribution is strictly prohibited.

from subprocess import run  # nosec
from sys import argv, platform


def main():
    if platform == "win32":
        cmd = ("pip-compile", "--output-file", "requirements.win.txt", *argv[1:])
    else:
        cmd = ("pip-compile", *argv[1:])
    return run(cmd).returncode  # nosec


if __name__ == "__main__":
    exit(main())
