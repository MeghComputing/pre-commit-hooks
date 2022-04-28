# copyrighter

`copyrighter` is a script that checks the copyright head in a given file. It detects detects if the header is missing. It can also detect if the year does not match the current year, and can automatically update it.

## Usage

```
usage: copyrighter [-h] [-f] [-v] [-e EXTENSIONS] filename [filename ...]

positional arguments:
  filename              The path(s) of the file(s) to check.

optional arguments:
  -h, --help            show this help message and exit
  -f, --fix             If given, automatically update the copyright year to
                        the current year.
  -v, --verbose         Print more context.
  -e EXTENSIONS, --extensions EXTENSIONS
                        The path of a file with a list of extensions to check.
                        Defaults: .c, .cpp, .cs, .css, .h, .hpp, .java, .js,
                        .php, .py.
```

There is currently only support for Megh's copyright header in proprietary, shared, and Apache 2.0 form. Only a single year (e.g. `2022`) or one range of years (e.g. `2020-2022`) is supported.

All files given will be checked.

`__init__.py` files are ignored.

### `-f`, `--fix`

If given, copyrighter will overwrite the copyright's end year with the current year. It will not attempt to add a missing header. It cannot fix issues with the start year.

### `-e EXTENSIONS`, `--extensions EXTENSIONS`

Give a path to a text file containing a newline-delimited list of extensions to check. All other extensions will be ignored (automatic success).

Here is an example file.

`cr-extensions.txt`

```
.py
.cpp
```

The command `copyrighter -e cr-extensions.txt` will only check `.py` and `.cpp` files. Other files will automatically succeed.

If not given, the default file extensions (shown previously) are used.

## pre-commit hook

By default, the hook calls copyrighter with the `--fix` arg, but this can be overridden.
