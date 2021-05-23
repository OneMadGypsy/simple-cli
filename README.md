# simple-cli

This is a very simple command line interface written in micropython. This allows you to perform a handful of file/folder operations on your microcontroller's file system and/or any mounted drive that is connected to it, from the REPL.

![CLI Example Image](https://i.imgur.com/Busi9DL.png "CLI Example")

## Docs:

<br />

**CLI(`clear`, `user`)**

 Arg   | Type   | Default
 ------|--------|--------
 clear | bool   | True
 user  | str    | 'user'
 
 <br />
 
 ## Commands:
 
 <br />
 
>It needs to be noted that this is a very simple CLI. If you consider the following commands to perform operation to or from the directory you are currently in, then you shouldn't have any issues. Attempting to treat this like it will understand or properly handle complex paths will likely be futile. I have aspirations to improve this, eventually. It's current state isn't bad, though. It performs well if you treat it like what it is... a rudimentary CLI that simplifies some filesystem operations on embedded systems.
 
 <br />
 
 
 Cmd    | Description                  | Examples                              |
--------|------------------------------|---------------------------------------|
exit    | exit the terminal            |                                       |
help    | prints this help info        |                                       |
list    | lists the current directory  |                                       |
clr     | clear the terminal           |                                       |
cd      | change directory             | cd path (../ is not supported)        |
print   | print requested file         | print fileName (opt: \'r\' or \'rb\') |
mkdir   | creates a new directory      | mkdir dirName                         |
del     | delete a file or folder      | del fileOrDirName                     |

 <br />
  
## Usage:

 <br />
 
```python
from cli import CLI

CLI(user='yourName')
```

