#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Copyright (c) 2010-21 Fabien Boutantin
#
# This script is the result of merging multiple recipes and answers from the internet
# into one single script.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


"""
Module that helps writing more colorful console applications.

It proposes coloring for foreground and background colors for Linux terminal supporting ANSI escape
characters, and windows terminals (powershell and cmd) based on Win32 API.

It also provides some utility functions like requesting acknowledgment, or choice selection, etc...
"""


__version__ = '1.00'
__author__ = 'Fabien Boutantin'
__license__ = 'MIT'


try:
    range = xrange
except NameError:
    pass

import os
import sys
import shutil
import types  # types is well used but in generated code
try:
    types
except Exception as e:
    raise e

DEBUG = False

try:
    input = raw_input
except NameError:
    pass

# do we print to a terminal or not?
is_output_atty = sys.stdout.isatty()

if os.name == "nt":
    from ctypes import windll, Structure, c_short, c_ushort, byref
    SHORT = c_short
    WORD = c_ushort

    class COORD(Structure):
        """struct in wincon.h."""
        _fields_ = [
            ("X", SHORT),
            ("Y", SHORT)]

    class SMALL_RECT(Structure):
        """struct in wincon.h."""
        _fields_ = [
            ("Left", SHORT),
            ("Top", SHORT),
            ("Right", SHORT),
            ("Bottom", SHORT)]

    class CONSOLE_SCREEN_BUFFER_INFO(Structure):
        """struct in wincon.h."""
        _fields_ = [
            ("dwSize", COORD),
            ("dwCursorPosition", COORD),
            ("wAttributes", WORD),
            ("srWindow", SMALL_RECT),
            ("dwMaximumWindowSize", COORD)]
    # winbase.h
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
    GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

    COLORS_DICT = {
        'BOLD': None,
        'FOREGROUND': {
            'WHITE': 0x0007,
            'BLACK': 0x0000,
            'BLUE': 0x0001,
            'GREEN': 0x0002,
            'CYAN': 0x0003,
            'RED': 0x0004,
            'MAGENTA': 0x0005,
            'YELLOW': 0x0006,
            'GREY': 0x0007,
        },
        'FG_INTENSITY': 0x0008,
        'BACKGROUND': {
            'WHITE': 0x0070,
            'BLACK': 0x0000,
            'BLUE': 0x0010,
            'GREEN': 0x0020,
            'CYAN': 0x0030,
            'RED': 0x0040,
            'MAGENTA': 0x0050,
            'YELLOW': 0x0060,
            'GREY': 0x0070,
        },
        'BG_INTENSITY': 0x0080,
    }

elif os.name == "posix":
    COLORS_DICT = {
        'BOLD': 1,
        'FOREGROUND': {
            'WHITE': 37,
            'BLACK': 30,
            'BLUE': 34,
            'GREEN': 32,
            'CYAN': 36,
            'RED': 31,
            'MAGENTA': 35,
            'YELLOW': 33,
            'GREY': 37,
        },
        'FG_INTENSITY': 0x0,
        'BACKGROUND': {
            'WHITE': 47,
            'BLACK': 40,
            'BLUE': 44,
            'GREEN': 42,
            'CYAN': 46,
            'RED': 41,
            'MAGENTA': 45,
            'YELLOW': 43,
            'GREY': 47,
        },
        'BG_INTENSITY': 0x0,
    }

NT = 1
POSIX = 2


class ColorConsole(object):
    def __init__(self):
        # some forward declaration for linters
        self.white = None
        self.black = None
        self.blue = None
        self.green = None
        self.cyan = None
        self.red = None
        self.magenta = None
        self.yellow = None
        self.grey = None

        if os.name == "nt":
            self.__mode = NT
            self.__bcp_attrs = self._get_text_attr()
        elif os.name == "posix":
            self.__mode = POSIX
            self.__hist = list()
        # copy sys to prevent errors in __del__
        self.__sys = sys

        if os.environ.get("CC_PROGRESS_MODE", None) == "PACMAN":
            self.progress = self.progress_pacman

        for item in COLORS_DICT['FOREGROUND']:
            name = item.lower()
            value = COLORS_DICT['FOREGROUND'][item] | COLORS_DICT["FG_INTENSITY"]
            exec("self.%s = types.MethodType(lambda x: x._o(%d), self)" % (name, value))
            if DEBUG:
                eval("self.%s()" % name)
                print("Foreground", name)
        self.reset()

        for item in COLORS_DICT['BACKGROUND']:
            name = 'bg_' + item.lower()
            value = COLORS_DICT['BACKGROUND'][item] | COLORS_DICT["BG_INTENSITY"]
            exec("self.%s = types.MethodType(lambda x: x._o(%d), self)" % (name, value))
            if DEBUG:
                eval("self.%s()" % name)
                print("\nBackground", item, end=' ')
        self.reset()

    def get_size(self):
        """ Returns size of the console: Columns, lines """
        try:
            return shutil.get_terminal_size()
        except Exception:
            if not is_output_atty:
                return 80, 24
            try:
                lines, cols = os.popen('stty size', 'r').read().split()
                return int(cols), int(lines)
            except Exception:
                return 80, 24

    def __del__(self):
        self.reset()
    if os.name == "posix":
        def reset(self):
            self.__hist = list()
            if is_output_atty:
                self.__sys.stdout.write("\x1b[!p\x1b[?3;4l\x1b[4l\x1b>")
            self._o(10)
            self._o(0)
            self.__sys.stdout.flush()

        def __clear_screen(self):
            if is_output_atty:
                self.__sys.stdout.write("\x1b[H\x1b[2J")
            self.__sys.stdout.flush()

        def _o(self, msg):
            msg = "%02i" % msg
            self.__hist.append(msg)
            if is_output_atty:
                self.__sys.stdout.write("\x1b[%sm" % (";".join(self.__hist)))
            self.__sys.stdout.flush()

    elif os.name == "nt":
        def reset(self):
            self._o(self.__bcp_attrs)
            self.__sys.stdout.flush()

        def _get_text_attr(self):
            csbi = CONSOLE_SCREEN_BUFFER_INFO()
            GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
            return csbi.wAttributes

        def _o(self, color):
            if is_output_atty:
                SetConsoleTextAttribute(stdout_handle, color)
            self.__sys.stdout.flush()

    def message(self, *argv):
        print(" ".join(map(str, argv)), end='')

    def success(self, *argv):
        if is_output_atty:
            self.green()
            self.bold()
        self.message(*argv)
        if is_output_atty:
            self.reset()

    def acknowledgment(self, msg, default=True):
        if is_output_atty:
            self.blue()
            self.bold()
        res = None
        if default:
            tail = "[Y/n]"
        else:
            tail = "[y/N]"
        while res not in ("", "y", "n"):
            print(msg, tail, end=' ')
            try:
                if is_output_atty:
                    res = input().lower()
                else:
                    self.warning("\n > Acknowledgment asked in non interactive mode, return default value\n")
                    res = ""
            except KeyboardInterrupt as e:
                self.reset()
                raise e
        if is_output_atty:
            self.reset()
        if res == "":
            return default
        else:
            return res != "n"

    def choice(self, msg, choices, default=0):
        assert(default in range(len(choices)))
        if is_output_atty:
            self.blue()
            self.bold()
        res = None
        tail = "[%d]" % default
        actual_msg = msg + "\n"
        for i, c in enumerate(choices):
            actual_msg += "%2d - %s\n" % (i, c)
        actual_msg += "Enter your selection then ENTER"
        while res not in range(len(choices)):
            print(actual_msg, tail, end=' ')
            try:
                if is_output_atty:
                    try:
                        res = input().lower()
                        if res == "":
                            res = default
                        else:
                            res = int(res)
                    except Exception as e:
                        print(e)
                        res = None
                else:
                    self.warning("\n > Choice asked in non interactive mode, return default value\n")
                    res = default
            except KeyboardInterrupt as e:
                self.reset()
                raise e
        if is_output_atty:
            self.reset()
        return res, choices[res]

    def multi_choice(self, msg, choices, default=[0]):
        def validate_selection(selection):
            if selection is None:
                return False
            return all([x in range(len(choices)) for x in selection])
        assert(validate_selection(default))
        if is_output_atty:
            self.blue()
            self.bold()
        res = None
        tail = "[%s]" % " ".join(map(str, default))
        actual_msg = msg + "\n"
        choices_strings = list()
        for i, c in enumerate(choices):
            choices_strings.append("%2d - %s " % (i, c))
        choices_per_line = self.get_size()[0] // max(map(len, choices_strings))
        choice_size = self.get_size()[0] // choices_per_line
        while choices_strings:
            for i in range(choices_per_line):
                if choices_strings:
                    actual_msg += choices_strings.pop(0).ljust(choice_size)
            actual_msg += "\n"
        actual_msg += "Enter your selection (space-separated) then ENTER"
        while not validate_selection(res):
            print(actual_msg, tail, end=' ')
            try:
                if is_output_atty:
                    try:
                        res = input().lower()
                        if res == "":
                            res = default
                        else:
                            res = list(map(int, res.split()))
                    except Exception as e:
                        print(e)
                        res = None
                else:
                    self.warning("\n > Choice asked in non interactive mode, return default value\n")
                    res = default
            except KeyboardInterrupt as e:
                self.reset()
                raise e
        if is_output_atty:
            self.reset()
        return res, [choices[x] for x in res]

    def warning(self, *argv):
        if is_output_atty:
            self.yellow()
            self.bold()
        self.message(*argv)
        if is_output_atty:
            self.reset()

    def error(self, *argv):
        if is_output_atty:
            self.red()
            self.bold()
        self.message(*argv)
        if is_output_atty:
            self.reset()

    def progress(self, current, maximum=100, display_on_non_tty=False):
        """
        Given a current progress value and a maximum, display a progress bar
        in the terminal.
        If output is not a terminal and display_on_non_tty is true, then
        display figures for progress.
        """
        progress_txt = "[Progress: %3d/%d]" % (current, maximum)
        if is_output_atty:
            self.green()
            self.bold()
            print("\r" + progress_txt, end="")
            self.reset()

            max_width = self.get_size()[0] - 1 - len(progress_txt)
            if os.name == "nt":
                # account for the blinking cursor
                max_width -= 1
            if current >= maximum:
                progress = max_width
            else:
                progress = int(max_width * current / maximum)
            try:
                print(
                    " " + ("\u2588" * progress) + ("\u2591" * (max_width - progress)),
                    end=""
                )
            except Exception:
                print(
                    (" [") + ("#" * (progress - 2)) + (" " * (max_width - progress - 2)),
                    end="]"
                )
        elif display_on_non_tty:
            print(progress_txt)

    def progress_pacman(self, current, maximum=100, display_on_non_tty=False):
        """
        Given a current progress value and a maximum, display a progress bar
        in the terminal (using some kind of Pacman ascciart).
        If output is not a terminal and display_on_non_tty is true, then
        display figures for progress.
        """
        progress_txt = "[Progress: %3d/%d]" % (current, maximum)
        if is_output_atty:
            self.green()
            self.bold()
            print("\r" + progress_txt, end="")
            self.reset()

            max_width = self.get_size()[0] - 1 - len(progress_txt)
            if os.name == "nt":
                max_width -= 1
            if current >= maximum:
                progress = max_width
            else:
                progress = int(max_width * current / maximum)
            try:
                # Print a line of pac-gums and ghost
                print("\u2022 \u2022 \u15E3 " * ((max_width - 1) // 6), end="")
                print("\r" + progress_txt, end="")
                # Prints only dots (Pacman already passed through)
                print(" " + ("\u00B7 " * (progress // 2)), end="")
                if progress < max_width:
                    self.bold()
                    self.yellow()
                    # Make Pacman close and open (2B24 is large circle,
                    # but doesn't suit monospace)
                    pacman = '\u25CF' if current % 2 == 0 else '\u25D6'
                    print(pacman, end="")
                    self.reset()
            except Exception as e:
                print(
                    " [" + ("#" * (progress - 2)) + (" " * (max_width - progress - 2)),
                    end="]"
                )
                print(e)
        elif display_on_non_tty:
            print(progress_txt)

    def bold(self):
        if not is_output_atty:
            return
        if os.name == "posix":
            self._o(COLORS_DICT['BOLD'])
        else:
            pass


def test_placeholder():
    """Makes pytest happy :P"""
    pass


if __name__ == "__main__":
    DEBUG = True
    cc = ColorConsole()
    print()
    cc.message("simple message\n")
    cc.success("Success message\n")
    cc.warning("Warning message\n")
    cc.error("Error message\n")
    cc.bold()
    print(cc.acknowledgment("OK?", True))
    print(cc.acknowledgment("Cancel?", False))
    cc.reset()
    print(
        cc.choice(
            "Which choice are you going to make?",
            [1, 2, 3, "Neither", None],
            4)
    )
    print()
