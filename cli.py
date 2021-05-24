import uos
from micropython import const
 
#_> STAT BITMASKS
_STAT_FLDR  = const(0x4000)
_STAT_FILE  = const(0x8000)

#_> Linux Terminal FOREGROUND BACKGROUND and MODIFIERS
_NORMAL     = const(0)
_FG_BLACK  , _BG_BLACK  , _BOLD       = const(30), const(40), const(1)
_FG_RED    , _BG_RED    , _SHADE      = const(31), const(41), const(2)
_FG_GREEN  , _BG_GREEN  , _ITALIC     = const(32), const(42), const(3)
_FG_YELLOW , _BG_YELLOW , _UNDERLINE  = const(33), const(43), const(4)
_FG_BLUE   , _BG_BLUE   , _BLINK      = const(34), const(44), const(5)
_FG_MAGENTA, _BG_MAGENTA, _INVERSE    = const(35), const(45), const(7)
_FG_CYAN   , _BG_CYAN   , _STRIKE     = const(36), const(46), const(9)
_FG_WHITE  , _BG_WHITE  , _BOLD_ULINE = const(37), const(47), const(21)

#_> THEME ~ changing just these colors can retheme the entire app
_MAIN       = _FG_CYAN  # HEADERS and CMDLINE (user@host:~/directory $)
_BRIGHT_FG  = _FG_WHITE # over _BG AND _ALT_BG
_FG         = _FG_BLACK # over _BG only
_BG         = _BG_WHITE
_ALT_FG     = _FG_WHITE # over _ALT_BG only
_ALT_BG     = _BG_BLACK

#_> FORMAT TEMPLATES
_FMT1       = '\033[{}m'
_FMT2       = '\033[{};{}m'
_FMT3       = '\033[{};{};{}m'
_FMT4       = '\033[{};{};{};{}m'
_COMBINE    = '{}{}'

#_> STYLESHEET
_E          = _FMT2.format(_BOLD, _FG_RED)                          # error
_D          = _FMT1.format(_NORMAL)                                 # default
_CH         = _FMT4.format(_BOLD_ULINE, _BOLD, _MAIN, _BG_BLACK)    # contrast header
_C1         = _FMT3.format(_BOLD  , _BRIGHT_FG, _BG    )            # contrast 1
_C1_        = _FMT3.format(_NORMAL,        _FG, _BG    )            # subcontrast 1
_C2         = _FMT3.format(_BOLD  , _BRIGHT_FG, _ALT_BG)            # contrast 2
_C2_        = _FMT3.format(_NORMAL,    _ALT_FG, _ALT_BG)            # subcontrast 2

#__> entry
_EHEADER    = '\n{} {:<25} {} {} {:<12} {}'.format(_CH, 'files', _D, _CH,'byte size', _D)
_ENTRY      = '{} {} {} {} {} {}'
_ENTRY1     = _ENTRY.format(_C1, '{:<25}', _D, _C1_, '{:>12}', _D)
_ENTRY2     = _ENTRY.format(_C2, '{:<25}', _D, _C2_, '{:>12}', _D)
_ENTRIES    = (_ENTRY1, _ENTRY2)

#__> help
_HHEADER    = '\n{} {:<8} {} {} {:<30} {} {} {:<33} {}'.format(_CH, 'cmd', _D, _CH,'description', _D, _CH, 'example', _D)
_HELP       = '{} {} {} {} {} {} {} {} {}'
_HELP1      = _HELP.format(_C1, '{:<8}', _D, _C1_, '{:<30}', _D, _C1_, '{:<33}', _D)
_HELP2      = _HELP.format(_C2, '{:<8}', _D, _C2_, '{:<30}', _D, _C2_, '{:<33}', _D)
_HELPS      = (_HELP1, _HELP2)

#_> sysinfo
_SHEADER    = '\n{} {:<77}{}'.format(_CH, 'sysinfo', _D)
_SYSINFO1   = '{} {}{} {} {}{}'.format(_C1, '{:<8}', _D, _C1_, '{:<67}', _D)
_SYSINFO2   = '{} {}{} {} {}{}'.format(_C2, '{:<8}', _D, _C2_, '{:<67}', _D)

#_> print
_FILE       = '\n{} {}{} bytes {}'.format(_CH, '{}/{}', '{:>50}', _FMT3.format(_NORMAL, _FG_WHITE, _BG_BLACK))

#_> continuous
_ERROR      = '\n{}{} {}/{} ({}) {}\n'.format(_E, '{}', '{}', '{}', '{}', _D)
_CMDLINE    = '{}{}{}:{}{} $ {}'.format(_FMT2.format(_BOLD, _MAIN), '{}@{}', _D, _FMT3.format(_BOLD, _SHADE, _MAIN), '~{}', _D)

#__> CLI
_CMDS       = ('exit', 'help', 'sysinfo', 'list', 'clr', 'cd', 'print', 'mkdir', 'del', 'rename')
_AUTOLIST   = ('cd', 'mkdir', 'del', 'rename')

_DESC       = ('exit the CLI', 'prints this help info', 'print system info', 'lists the current directory', 'clear the terminal', 
               'change directory', 'print requested file','creates a new directory', 'delete a file or folder', 'rename a file')
_EXS        = ('', '', '', '', '', 'cd path', 'print fileName [r | rb]', 'mkdir dirName', 'del fileOrDirName', 'rename oldname newname')

      
class CLI(object):
    #__> COMMAND LINE INTERFACE
    def __init__(self, clear:bool=True, user:str='user') -> None:
        print('' if not clear else '\n'*100)
        
        host = uos.uname().sysname
        CLI.__list(uos.getcwd())
        
        while True:
            args = input(_CMDLINE.format(user, host, uos.getcwd())).split(' ')
            cmd  = args.pop(0)
            path = uos.getcwd() if len(args) < 1 else args.pop(0)
            alt  = None         if len(args) < 1 else args.pop(0)
            
            try:
                mode = uos.stat(path)[0]
            except OSError as err:
                if cmd == 'mkdir':
                    uos.mkdir(path)
                else:
                    print(_ERROR.format('Path Error', uos.getcwd()[1:], path, err))
                    continue
                    
            if cmd in _CMDS:
                if   cmd == 'exit'   : break
                elif cmd == 'clr'    : print('\n'*100)
                elif cmd == 'help'   : CLI.__help()
                elif cmd == 'sysinfo': CLI.__sysinfo()
                elif cmd == 'del'    : CLI.__delete(path, mode)
                elif cmd == 'list'   : CLI.__list(path)              if mode & _STAT_FLDR else None
                elif cmd == 'print'  : CLI.__print(path, alt)        if mode & _STAT_FILE else None
                elif cmd == 'cd'     : uos.chdir(path)               if mode & _STAT_FLDR else None
                elif cmd == 'rename' : uos.rename(path, alt) if alt and mode & _STAT_FILE else None
                    
            if cmd in _AUTOLIST:
                CLI.__list(uos.getcwd())
                
      
    #__> Reads And Yields A File In 512 Byte Chunks
    @staticmethod
    def __read(path:str, format='r', buffsize:int=512):
        buff = bytearray(buffsize)
        try:
            file = open(path, 'rb')
        except OSError as err:
            print(_ERROR.format('Path Error', uos.getcwd()[1:], path, err))
            return None
        
        while True:
            buff = file.read(buffsize)
            yield buff if format == 'rb' else buff.decode()
            if not buff:
                file.close()
                break;
                
        return None
    
    #__> Sorts A List By Directories First Plus Alphabetical First Letter Plus Name Length
    @staticmethod            
    def __dirsort(item:str) -> int:
        return ((uos.stat(item)[0] & _STAT_FILE)*1000)+(ord(item[0])*10)+len(item)
    
    #__> Prints System Info  
    @staticmethod
    def __sysinfo() -> None: 
        print(_SHEADER)
        print(_SYSINFO1.format('sysname', uos.uname().sysname))
        print(_SYSINFO2.format('machine', uos.uname().machine))
        print(_SYSINFO1.format('upython', uos.uname().version))
        print()
    
    #__> Prints The Help Info
    @staticmethod
    def __help() -> None:
        print(_HHEADER)
        for n, (cmd, desc, ex) in enumerate(zip(_CMDS, _DESC, _EXS)):
            print(_HELPS[n%2].format(cmd, desc, (ex if len(ex) else '')))
        print()
        
    #__> Lists The Contents Of The Supplied Path
    @staticmethod
    def __list(path:str) -> None:
        print(_EHEADER)
        fs = uos.listdir(path)
        fs.sort(reverse=False, key=CLI.__dirsort)
        svi = 0
        for n, item in enumerate(fs):
            mode, size  = uos.stat(item)[0], uos.stat(item)[6]
            if mode & _STAT_FLDR:
                if item != "System Volume Information":
                    print(_ENTRIES[(n+svi)%2].format(item+'/', ''))
                else:
                    svi = 1
            else:
                print(_ENTRIES[(n+svi)%2].format(item, size))
        print()
    
    #__> Prints The Contents Of The supplied Path   
    @staticmethod
    def __print(path:str, fmt:str) -> None:
        fmt = fmt if fmt else 'r'
        hold = ''
        print(_FILE.format(uos.getcwd()[1:], path, uos.stat(path)[6]))
        for output in CLI.__read(path, fmt):
            if not output is None:
                #__> New Line Juggler
                L, N = len(output), (-1 if fmt == 'rb' else output.rfind('\n')) #length, last position of \n
                n    = N if N > -1 else L                                       #last position of \n if \n else length
                out  = _COMBINE.format(hold, output[0:n])                       #left  side of last \n if \n
                hold = output[n+1:] if n < L else ''                            #right side of last \n if \n
                if out:
                    print(out)      #print up to last \n if \n (and provides previous "last \n" via behavior)
        print(_D)

    #__> Recursively Deletes Directories And Contents Side-stepping EACCESS Issues With Populated Directories
    @staticmethod
    def __delete(path:str, mode:int) -> None:
        try:
            if mode & _STAT_FILE:
                uos.remove(path)
            elif mode & _STAT_FLDR:
                cwd = uos.getcwd()
                uos.chdir(path)
                for item in uos.listdir():
                    mode = uos.stat(item)[0]
                    CLI.__delete(item, mode)
                uos.chdir(cwd)
                uos.rmdir(path)
        except OSError as err:
            print(_ERROR.format('Cannot Delete', uos.getcwd()[1:], path, err))
        
        
