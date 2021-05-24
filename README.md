# simple-cli

This is a very simple command line interface written in micropython. This simplifies a handful of filesystem operations on your device and any mounted drive that is connected to it, Currently, it is mostly a wrapper that turns `uos` into a list of commands, and formats, sorts and/or prunes it's return data, but it has a few other tricks that `uos` doesn't provide. This is not currently compatible with anything other than a linux terminal. If you would like to retheme the interface, go to line 19 in the code and read the comments. I made it as simple as I possibly could. Changing just 5 lines can redress the entire app.

<br />

![CLI Example Image](https://i.imgur.com/pU0TYCq.png "CLI Example")


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
**sysinfo** | prints system info           |                                       | `uos.uname()`   (*pruned*)
**list**    | lists the current directory  |                                       | `uos.listdir()` (*sorted*)
**clr**     | clear the terminal           |                                       | *no equivalent*
**cd**      | change directory             | cd path                               | `uos.chdir()`
**print**   | print requested file         | print fileName [r, rb]                | *no equivalent*
**mkdir**   | creates a new directory      | mkdir dirName                         | `uos.mkdir()`
**del**     | delete a file or folder      | del fileOrDirName                     | *no equivalent*
**rename**  | rename a file                | rename oldname newname                | `uos.rename()`
**find**    | find all with term from cwd  | find term                             | *no equivalent*
**syspath** | print or [modify] syspath    | syspath [add, del]                    | `sys.path` [`.append()`, `.remove()`]

<br />

**`cd`, `mkdir`, `del` and `rename` will automatically list the current directory when their operation completes** 

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

