#!/usr/bin/env python3

#  RaceBuff is an open-source overlay application for racing simulation.
#  Copyright (C) 2026 RaceBuff developers, see contributors.md file
#
#  This file is part of RaceBuff.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Run program
"""

import argparse
import os
import sys


def get_cli_argument() -> argparse.Namespace:
    """Get command line argument"""
    parse = argparse.ArgumentParser(
        description="RaceBuff command line arguments",
    )
    parse.add_argument(
        "-l",
        "--log-level",
        choices=range(3),
        default=1,
        type=int,
        help=(
            "set logging output level:"
            " 0 - warning and error only;"
            " 1 - all levels (default);"
            " 2 - output to file;"
        ),
    )
    parse.add_argument(
        "-s",
        "--single-instance",
        choices=range(2),
        default=1,
        type=int,
        help=(
            "set running mode:"
            " 0 - allow running multiple instances;"
            " 1 - single instance (default);"
        ),
    )
    # Disallow version override if run as compiled exe (racebuff)
    if "racebuff.exe" not in sys.executable.lower():
        parse.add_argument(
            "-p",
            "--pyside",
            choices=(2, 6),
            default=2,
            type=int,
            help=(
                "set PySide (Qt for Python) version:"
                " 2 - PySide2;"
                " 6 - PySide6;"
            ),
        )
    return parse.parse_args()


def override_pyside_version(version: int = 6):
    """Override PySide version 2 to 6 so code importing PySide2 gets PySide6."""
    if version != 6:
        return
    # Load PySide6 and submodules first (frozen exe has them under PySide6.*)
    import PySide6  # noqa: F401
    import PySide6.QtCore  # noqa: F401
    import PySide6.QtGui  # noqa: F401
    import PySide6.QtWidgets  # noqa: F401
    import PySide6.QtMultimedia  # noqa: F401
    # Then alias PySide2 -> PySide6 so "from PySide2.QtCore" works
    sys.modules["PySide2"] = PySide6
    sys.modules["PySide2.QtCore"] = PySide6.QtCore
    sys.modules["PySide2.QtGui"] = PySide6.QtGui
    sys.modules["PySide2.QtWidgets"] = PySide6.QtWidgets
    sys.modules["PySide2.QtMultimedia"] = PySide6.QtMultimedia


def override_module(original: str, override: str):
    """Manual import & override module (used when not frozen)."""
    sys.modules[original] = __import__(override, fromlist=[override])


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

    # Load command line arguments
    cli_args = get_cli_argument()

    pyside_override = getattr(cli_args, "pyside", 2)
    # When running as compiled exe, bundle has PySide6 (not PySide2). Detect and use 6.
    if "racebuff.exe" in sys.executable.lower():
        try:
            __import__("PySide6")
            pyside_override = 6
        except ImportError:
            pass  # keep 2 if PySide2 build
    os.environ["PYSIDE_OVERRIDE"] = f"{pyside_override}"  # store to env
    override_pyside_version(pyside_override)

    # Start
    from racebuff.main import start_app

    start_app(cli_args)
