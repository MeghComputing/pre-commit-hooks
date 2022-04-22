# Copyright (c) 2022 Megh Computing, Inc.

# All rights reserved. No warranty, explicit or implied, provided.
# Unauthorized use, modification, or distribution is strictly prohibited.

import datetime
import os

import pytest
from pyparsing import alphanums

import copyrighter

copyright_megh_python = """{0}\
# Copyright (c) {1} Megh Computing, Inc.

# All rights reserved. No warranty, explicit or implied, provided.
# Unauthorized use, modification, or distribution is strictly prohibited.
"""

# Skip the shebang, though it could work with one.
copyright_megh_cpp = """\
/*******************************************************************************
* Copyright (c) {1} Megh Computing, Inc.
*
* All rights reserved. No warranty, explicit or implied, provided.
* Unauthorized use, modification, or distribution is strictly prohibited.
*******************************************************************************/
"""

copyright_apache_python = """{0}\
# Copyright {1} Megh Computing, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

# Skip the shebang, though it could work with one.
copyright_apache_cpp = """\
/*******************************************************************************
* Copyright {1} Megh Computing, Inc.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*   http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/
"""

shebang = "#!/usr/bin/env python3\n"

shebang_params = [
    "optional_shebang",
    [
        (""),
        (shebang),
        (shebang + "\n\n\n\n"),
    ],
]


def test_parse_empty():
    lines = ""
    start_year, end_year = copyrighter.parse_copyright_megh(lines)
    assert start_year is None
    assert end_year is None

    start_year, end_year = copyrighter.parse_copyright_apache(lines)
    assert start_year is None
    assert end_year is None


@pytest.mark.parametrize(*shebang_params)
def test_parse_single_year(optional_shebang: str):
    # Test Megh copyright.
    for copyright in (copyright_megh_python, copyright_megh_cpp):
        lines = copyright.format(optional_shebang, 2021)
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year == 2021 and end_year == 2021

        lines = copyright.format(optional_shebang, 202)
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "blah")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year is None and end_year is None

    # Repeat for Apache copyright.
    for copyright in (copyright_apache_python, copyright_apache_cpp):
        lines = copyright.format(optional_shebang, 2021)
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year == 2021 and end_year == 2021

        lines = copyright.format(optional_shebang, 202)
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "blah")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year is None and end_year is None


@pytest.mark.parametrize(*shebang_params)
def test_parse_year_range(optional_shebang: str):
    for copyright in (copyright_megh_python, copyright_megh_cpp):
        lines = copyright.format(optional_shebang, "2017-2019")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year == 2017 and end_year == 2019

        lines = copyright.format(optional_shebang, "2040-2020")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year == 2040 and end_year == 2020

        lines = copyright.format(optional_shebang, "2023-2021")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year == 2023 and end_year == 2021

        lines = copyright.format(optional_shebang, "2023-blah")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "2021, 2022")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "2017-2019, 2022")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "2017, 2019-2022")
        start_year, end_year = copyrighter.parse_copyright_megh(lines)
        assert start_year is None and end_year is None

    for copyright in (copyright_apache_python, copyright_apache_cpp):
        lines = copyright.format(optional_shebang, "2017-2019")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year == 2017 and end_year == 2019

        lines = copyright.format(optional_shebang, "2040-2020")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year == 2040 and end_year == 2020

        lines = copyright.format(optional_shebang, "2023-2021")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year == 2023 and end_year == 2021

        lines = copyright.format(optional_shebang, "2023-blah")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "2021, 2022")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "2017-2019, 2022")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year is None and end_year is None

        lines = copyright.format(optional_shebang, "2017, 2019-2022")
        start_year, end_year = copyrighter.parse_copyright_apache(lines)
        assert start_year is None and end_year is None


@pytest.mark.parametrize(*shebang_params)
def test_parse_bad_format(optional_shebang: str):
    current_year = datetime.date.today().year

    # Turn off psf/black (linting) autoformatting
    # fmt: off
    #                              correct  f"{optional_shebang}\n\nCopyright (c) 2020-{current_year} Megh Computing, Inc."
    assert copyrighter.parse_copyright_megh(f"{optional_shebang}\n\nCopyright 2020-{current_year} Megh Computing, Inc.") == (None, None)
    assert copyrighter.parse_copyright_megh(f"{optional_shebang}\n\nCopyright (c) 200-{current_year} Megh Computing, Inc.") == (None, None)
    assert copyrighter.parse_copyright_megh(f"{optional_shebang}\n\nCopyright (c) 2020-223 Megh Computing, Inc.") == (None, None)
    assert copyrighter.parse_copyright_megh(f"{optional_shebang}\n\nCopyright(c) 2020-{current_year} Megh Computing, Inc.") == (None, None)
    assert copyrighter.parse_copyright_megh(f"{optional_shebang}\n\nCopyright (c) 2020-{current_year} Meg Computing, Inc.") == (None, None)

    #                              correct:   f"{optional_shebang}\n\nCopyright 2020-{current_year} Megh Computing, Inc."
    assert copyrighter.parse_copyright_apache(f"{optional_shebang}\n\nCopyright (c) 2020-{current_year} Megh Computing, Inc.") == (None, None)
    assert copyrighter.parse_copyright_apache(f"{optional_shebang}\n\nCopyright 200-{current_year} Megh Computing, Inc.") == (None, None)
    assert copyrighter.parse_copyright_apache(f"{optional_shebang}\n\nCopyright 2020-223 Megh Computing, Inc.") == (None, None)
    assert copyrighter.parse_copyright_apache(f"{optional_shebang}\n\nCopyright2020-{current_year} Megh Computing, Inc.") == (None, None)
    assert copyrighter.parse_copyright_apache(f"{optional_shebang}\n\nCopyright 2020-{current_year} Meg Computing, Inc.") == (None, None)
    # fmt: on


@pytest.mark.parametrize(*shebang_params)
def test_write_year_1(mocker, optional_shebang):
    given = copyright_megh_python.format(optional_shebang, "2021").split("\n")
    expected = copyright_megh_python.format(optional_shebang, "2021-2022").split("\n")
    mocker.patch("copyrighter.read_file", return_value=given)
    mocker.patch("copyrighter.write_file")
    copyrighter.write_current_year("", 2021, 2022)
    copyrighter.write_file.assert_called_once_with("", expected)


@pytest.mark.parametrize(*shebang_params)
def test_write_year_2(mocker, optional_shebang):
    given = copyright_apache_python.format(optional_shebang, "2020").split("\n")
    expected = copyright_apache_python.format(optional_shebang, "1912-1954").split("\n")
    mocker.patch("copyrighter.read_file", return_value=given)
    mocker.patch("copyrighter.write_file")
    copyrighter.write_current_year("", 1912, 1954)
    copyrighter.write_file.assert_called_once_with("", expected)


@pytest.mark.parametrize(*shebang_params)
def test_write_year_3(mocker, optional_shebang):
    given = copyright_megh_cpp.format(optional_shebang, "2021-2022").split("\n")
    expected = copyright_megh_cpp.format(optional_shebang, "1903-1995").split("\n")
    mocker.patch("copyrighter.read_file", return_value=given)
    mocker.patch("copyrighter.write_file")
    copyrighter.write_current_year("", 1903, 1995)
    copyrighter.write_file.assert_called_once_with("", expected)


@pytest.mark.parametrize(*shebang_params)
def test_write_year_4(mocker, optional_shebang):
    given = copyright_apache_cpp.format(optional_shebang, "2017").split("\n")
    expected = copyright_apache_cpp.format(optional_shebang, "1906-1992").split("\n")
    mocker.patch("copyrighter.read_file", return_value=given)
    mocker.patch("copyrighter.write_file")
    copyrighter.write_current_year("", 1906, 1992)
    copyrighter.write_file.assert_called_once_with("", expected)


@pytest.mark.parametrize(*shebang_params)
def test_write_year_5(mocker, optional_shebang):
    # Make sure that other lines in the file aren't changed.
    body = [str(i) + alphanums + "\n" for i in range(300)] + ["\n"]
    given = copyright_megh_python.format(optional_shebang, "2021").split("\n") + body
    expected = copyright_megh_python.format(optional_shebang, "2021-2022").split("\n") + body

    mocker.patch("copyrighter.read_file", return_value=given)
    mocker.patch("copyrighter.write_file")
    copyrighter.write_current_year("", 2021, 2022)
    copyrighter.write_file.assert_called_once_with("", expected)


class TestCheckFile:
    filename = "test-file-delete-me.py"
    current_year = datetime.date.today().year

    def setup_class(self):
        with open(self.filename, "w"):
            pass

    def teardown_class(self):
        assert os.path.isfile(self.filename)
        os.remove(self.filename)

    @pytest.mark.parametrize(*shebang_params)
    def test_check_file(self, mocker, optional_shebang):
        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, self.current_year)
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            assert copyrighter.check_file([".py"], self.filename, autofix=False) is True

        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, f"2017-{self.current_year}")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            assert copyrighter.check_file([".py"], self.filename, autofix=False) is True

        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, f"207-{self.current_year}")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            assert copyrighter.check_file([".py"], self.filename, autofix=False) is False

        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, f"blah-{self.current_year}")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            assert copyrighter.check_file([".py"], self.filename, autofix=False) is False

    @pytest.mark.parametrize(*shebang_params)
    def test_check_file_future_year(self, mocker, optional_shebang):
        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, "2071")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            assert copyrighter.check_file([".py"], self.filename, autofix=False) is False

        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, f"2071-{self.current_year}")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            assert copyrighter.check_file([".py"], self.filename, autofix=False) is False

    @pytest.mark.parametrize(*shebang_params)
    def test_check_file_backward_year(self, mocker, optional_shebang):
        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, "2021-2017")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            assert copyrighter.check_file([".py"], self.filename, autofix=False) is False

    @pytest.mark.parametrize(*shebang_params)
    def test_check_file_auto_fix(self, mocker, optional_shebang):
        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, "2017")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            mocker.patch("copyrighter.write_current_year")
            assert copyrighter.check_file([".py"], self.filename, autofix=True) is False
            copyrighter.write_current_year.assert_called_once_with(self.filename, 2017, self.current_year)

        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, "2020-2021")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            mocker.patch("copyrighter.write_current_year")
            assert copyrighter.check_file([".py"], self.filename, autofix=True) is False
            copyrighter.write_current_year.assert_called_once_with(self.filename, 2020, self.current_year)

        for copyright in (copyright_megh_python, copyright_apache_python):
            given = copyright.format(optional_shebang, "2020-2071")
            mocker.patch("copyrighter.read_tombstone", return_value=given)
            mocker.patch("copyrighter.write_current_year")
            assert copyrighter.check_file([".py"], self.filename, autofix=True) is False
            copyrighter.write_current_year.assert_called_once_with(self.filename, 2020, self.current_year)

    def test_check_file_ext_list(self):
        assert copyrighter.check_file([".x"], self.filename, autofix=False) is True


class TestExtensions:
    filename = "non-existent-file"

    def test_defaults(self):
        assert len(copyrighter.get_extensions(None)) > 0

    def test_good(self, mocker):
        file_lines = [".py\n", ".cpp\n", " \n", "\t\n", "\n", ".\n"]
        mocker.patch("copyrighter.read_file", return_value=file_lines)
        assert copyrighter.get_extensions(self.filename) == [".py", ".cpp", "."]

    def test_empty(self, mocker):
        file_lines = [""]
        mocker.patch("copyrighter.read_file", return_value=file_lines)
        assert not copyrighter.get_extensions(self.filename)

        file_lines = ["\n", "\t\n", "  \n"]
        mocker.patch("copyrighter.read_file", return_value=file_lines)
        assert not copyrighter.get_extensions(self.filename)

    def test_bad_extension(self, mocker):
        file_lines = ["x.py\n"]
        mocker.patch("copyrighter.read_file", return_value=file_lines)
        assert not copyrighter.get_extensions(self.filename)

        file_lines = ["py\n"]
        mocker.patch("copyrighter.read_file", return_value=file_lines)
        assert not copyrighter.get_extensions(self.filename)

        file_lines = ["x.\n"]
        mocker.patch("copyrighter.read_file", return_value=file_lines)
        assert not copyrighter.get_extensions(self.filename)
