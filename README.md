# PythonColorConsole

## Introduction

A multi platform lightweight script to print using colors in terminals using Python.

It's tested and working with both Python2 and Python3, and on Windows and Linux.
Not tested on Mac.

This script is a mix of many answers and recipes found on internet (StackOverflow, etc...).
I claim no paternity on the full stuff, but I've added some code of my onw and made the full stuff works fine (python3 port for instance).
That's why I publish with the MIT license (see attached file).

I hope it can be useful to someone, if so, I would be happy to hear it.

Regards,

## Usage

Import module and create a `ColorConsole` object, then use it before you print to set color:

```python
from PythonColorConsole.color_console import ColorConsole

cc = ColorConsole()
cc.red()
print("Hello,", end=" ")
cc.blue()
print("world", end="")
cc.bold()
cc.green()
print("!")
cc.reset()
```

Which will display this:

<pre><font color="#CC0000">Hello, </font><font color="#3465A4">world</font><font color="#4E9A06"><b>!</b></font></pre>

## Installation

You can use this script in 2 ways:

- copy it near the script that will use it
- install it either for your user or system-wide

To find the best place for installing it, start a python interpreter and type:

```python
>>> import sys, pprint
>>> pprint.pprint(sys.path)
```

This will print out a list of places where python is searching for modules.
For instance, on my Ubuntu 22.04.3:

```python
['',
 '/usr/lib/python310.zip',
 '/usr/lib/python3.10',
 '/usr/lib/python3.10/lib-dynload',
 '/home/fboutantin/.local/lib/python3.10/site-packages',
 '/usr/local/lib/python3.10/dist-packages',
 '/usr/lib/python3/dist-packages']
```

Depending on the path you choose, it will be a user or system wide installation.
If you install it system wide, you will need to have administrator/root privileges to do so.

To install, simply copy the full directory of this repository inside the chosen directory.
For instance, system wide: `/usr/lib/python3/dist-packages/PythonColorConsole`, or only for me: `/home/fboutantin/.local/lib/python3.10/site-packages/PythonColorConsole`

## Test that installed script is working

Using this command line, you can test the installation, and see a full range of what is proposed:

<pre>$ python -m PythonColorConsole.color_console
<font color="#D3D7CF">Foreground white</font>
<font color="#2E3436">Foreground black</font>
<font color="#3465A4">Foreground blue</font>
<font color="#4E9A06">Foreground green</font>
<font color="#06989A">Foreground cyan</font>
<font color="#CC0000">Foreground red</font>
<font color="#75507B">Foreground magenta</font>
<font color="#C4A000">Foreground yellow</font>
<font color="#D3D7CF">Foreground grey</font>

<span style="background-color:#D3D7CF">Background WHITE </span>
<span style="background-color:#2E3436">Background BLACK </span>
<span style="background-color:#3465A4">Background BLUE </span>
<span style="background-color:#4E9A06">Background GREEN </span>
<span style="background-color:#06989A">Background CYAN </span>
<span style="background-color:#CC0000">Background RED </span>
<span style="background-color:#75507B">Background MAGENTA </span>
<span style="background-color:#C4A000">Background YELLOW </span>
<span style="background-color:#D3D7CF">Background GREY </span>
simple message
<font color="#4E9A06"><b>Success message</b></font>
<font color="#C4A000"><b>Warning message</b></font>
<font color="#CC0000"><b>Error message</b></font>
<font color="#3465A4"><b>OK? [Y/n] y</b></font>
True
<font color="#3465A4"><b>Cancel? [y/N]  </b></font>
False
<font color="#3465A4"><b>Which choice are you going to make?</b></font>
<font color="#3465A4"><b> 0 - 1</b></font>
<font color="#3465A4"><b> 1 - 2</b></font>
<font color="#3465A4"><b> 2 - 3</b></font>
<font color="#3465A4"><b> 3 - Neither</b></font>
<font color="#3465A4"><b> 4 - None</b></font>
<font color="#3465A4"><b>Enter your selection then ENTER [4] </b></font>
(4, None)
</pre>