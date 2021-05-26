# simple-cli

This is a very simple command line interface written in micropython. This simplifies a handful of filesystem operations on your device and any mounted drive that is connected to it, Currently, it is mostly a wrapper that turns `uos` into a list of commands, and formats, sorts and/or prunes it's return data, but it has a few other tricks that `uos` doesn't provide. This is only properly supported by a linux terminal. Windows will understand the formatting but interpret it differently. If you would like to retheme the interface it can be done easily by modifying lines 28 through 33. There are also some alternate theme ideas at [the bottom of this repo](https://github.com/OneMadGypsy/simple-cli/blob/main/README.md#theme-ideas).

<br />

![CLI Example Image](https://i.imgur.com/aJYEYnx.png "CLI Example")


### Community:

_To officially file a bug report or feature request you can use these templates:_   [bug report](https://github.com/OneMadGypsy/simple-cli/blob/main/.github/ISSUE_TEMPLATE/bug_report.md) | [feature request](https://github.com/OneMadGypsy/simple-cli/blob/main/.github/ISSUE_TEMPLATE/feature_request.md)

_To discus features, bugs or share your own project that utilize code in this repo:_   [join the discussion](https://github.com/OneMadGypsy/simple-cli/discussions/1)

<br />

------

<br />

## Ports:

### cli.py
>This can be uploaded directly to the board, but is intended to be used as a frozen module. For information regarding how to setup the sdk and freeze a module you can refer to [this post](https://www.raspberrypi.org/forums/viewtopic.php?f=146&t=306449#p1862108) on the Raspberry Pi forum.


### cli.mpy
>This is a cross-compiled version of `cli.py`. It is intended to be uploaded to your board as you would any normal `.py` script.

<br />

-------

<br />

## Docs:

<br />

**CLI(`clear`, `user`)**

 Arg       | Type   | Description                    | Default
 ----------|--------|--------------------------------|--------
 **clear** | bool   | clears the terminal on startup | True
 **user**  | str    | personalize `user@sysname:~/`  | 'user'
 
 <br />
 
 ------
 
 <br />
 
 ## Commands:
 
 <br />
 
>Whereas the **`Same As`** section of the below table is accurate, very few commands are identical to their equivalent. This is because returned information has formatting, sorting and/or pruning applied, and may trigger another command as a convenience.
 
 <br />

 Cmd        | Description                  | Examples                              | Same As
------------|------------------------------|---------------------------------------|---------------------------------------
**exit**    | exit the CLI                 |                                       | *no equivalent*
**help**    | prints this help info        |                                       | *no equivalent*
**now**     | prints system timestamp      |                                       | `localtime(time())`
**sysinfo** | prints system info           |                                       | `uos.uname()`   (*pruned*)
**clr**     | clear the terminal           |                                       | *no equivalent*
**list**    | lists the current directory  | list [path]                           | `uos.listdir()` (*sorted*)
**cd**      | change directory             | cd path                               | `uos.chdir()`
**print**   | print requested file         | print fileName [r, rb]                | *no equivalent*
**mkdir**   | creates a new directory      | mkdir dirName                         | `uos.mkdir()`
**del**     | delete a file or folder      | del fileOrDirName                     | *no equivalent*
**rename**  | rename a file                | rename oldname newname                | `uos.rename()`
**find**    | find all with term from cwd  | find term                             | *no equivalent*
**syspath** | print or [modify] syspath    | syspath [add, del]                    | `sys.path` [`.append()`, `.remove()`]
**copy**    | copy a file                  | copy source destination [w, wb]       | *no equivalent*

<br />

-------

<br />

## Info

<br />

1) `cd`, `mkdir`, `del` and `rename` will automatically list the current directory when their operation completes
2) `sypath` will automatically list all paths when an `add` or `del` operation completes
3) `copy` will automatically list the parent directory of the destination file when the operation completes
4) `/absolute/path`, `relative/path`, and `../relative path` are all supported
5) wrap paths that contain spaces in quotes `'path/with space/file name.ext'`
6) most operations can be performed from anywhere as long as the path argument(s) are correct

<br />
 
------
 
<br />
 
  
## Usage:

 <br />
 
**simple**


```python
from cli import CLI

CLI(user='yourName') #auto-clears
```


```python
from cli import CLI

CLI(False, 'yourName') #wont auto-clear
```



**on button release**


```python
from cli import CLI
from machine import Pin

cli = Pin(3, Pin.IN, Pin.PULL_DOWN)
cli.irq(lambda p:CLI(user="yourName"), Pin.IRQ_FALLING) #on release

```

<br />
 
------
 
<br />
 
## Theme Ideas:

>Here are a few alternate themes that can be copy/pasted over lines 28 through 33. If you create an interesting theme [share it here](https://github.com/OneMadGypsy/simple-cli/discussions/1) so others can enjoy it.

<br />

### Happy Jack

```python
_MAIN       = _FG_BLACK 
_BRIGHT_FG  = _FG_YELLOW
_FG         = _FG_BLACK 
_BG         = _BG_RED
_ALT_FG     = _FG_RED   
_ALT_BG     = _BG_BLACK
```

![Happy Jack Example](https://i.imgur.com/UVmYvEX.png "Happy Jack Theme")

<br />

### Mardi Gras

```python
_MAIN       = _FG_MAGENTA
_BRIGHT_FG  = _FG_YELLOW 
_FG         = _FG_BLACK  
_BG         = _BG_GREEN
_ALT_FG     = _FG_GREEN  
_ALT_BG     = _BG_BLACK
```

![Mardi Gras Example](https://i.imgur.com/rzKK3se.png "Mardi Gras Theme")

<br />

### Snow Capped

```python
_MAIN       = _FG_WHITE
_BRIGHT_FG  = _FG_BLUE 
_FG         = _FG_WHITE
_BG         = _BG_BLUE
_ALT_FG     = _FG_WHITE
_ALT_BG     = _BG_BLACK
```

![Surf Example](https://i.imgur.com/N7EpGFq.png "Surf Theme")

<br />

### Minimalist

```python
_MAIN       = _FG_WHITE
_BRIGHT_FG  = _FG_WHITE
_FG         = _FG_WHITE
_BG         = _BG_BLACK
_ALT_FG     = _FG_WHITE
_ALT_BG     = _BG_BLACK
```

![Minimalist Example](https://i.imgur.com/Vt5d84L.png "Minimalist Theme")
