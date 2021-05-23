# simple-cli

This is a very simple command line interface written in micropython. This allows you to perform a handful of file/folder operations on your microcontroller's file system and/or any mounted drive that is connected to it, from the REPL.

![CLI Example Image](https://i.imgur.com/Busi9DL.png "CLI Example")


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
 
>It needs to be noted that this is a very simple CLI. If you consider the following commands to perform operation to or from the directory you are currently in, then you shouldn't have any issues. Attempting to treat this like it will understand or properly handle complex paths will likely be futile. I have aspirations to improve this, eventually. It's current state isn't bad, though. It performs well if you treat it like what it is... a rudimentary CLI that simplifies some filesystem operations on embedded systems.
 
 <br />

 Cmd        | Description                  | Examples                              | Same As
------------|------------------------------|---------------------------------------|--------------------------------
**exit**    | exit the CLI                 |                                       | *no equivalent*
**help**    | prints this help info        |                                       | *no equivalent*
**sysinfo** | prints system info           |                                       | `uos.uname()` *pruned*
**list**    | lists the current directory  |                                       | `uos.listdir()`
**clr**     | clear the terminal           |                                       | `print('\n'*100)`
**cd**      | change directory             | cd path (../ is not supported)        | `uos.chdir()`
**print**   | print requested file         | print fileName [opt: \'r\' or \'rb\'] | *no equivalent*
**mkdir**   | creates a new directory      | mkdir dirName                         | `uos.mkdir()`
**del**     | delete a file or folder      | del fileOrDirName                     | `uos.remove()` and `uos.rmdir()`
**rename**  | rename a file                | rename oldname newname                | `uos.rename()`

<br />

**`mkdir`, `del` and `rename` will automatically list the current directory when their operation completes** 

<br />
 
------
 
<br />
 
  
## Usage:

 <br />
 
```python
from cli import CLI

CLI(clear=True, user='yourName')
```

