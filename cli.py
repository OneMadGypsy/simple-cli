import uos
from usys import path as syspath
from ure import compile as urecompile
from gc import collect as gccollect
from gc import mem_free as gcmemfree
from gc import mem_alloc as gcmemalloc
from time import localtime as tnow
from time import time as ttime
 
_QUOTED     = urecompile('([\'"]([^\'"]*)["\'])')

#_> STAT BITMASKS
_STAT_FLDR  = const(0x4000)
_STAT_FILE  = const(0x8000)

#_> Linux Terminal FOREGROUND BACKGROUND and MODIFIERS
#_> We can't remove these if we make them `const`, and we are going to remove them
_NORMAL = 0
_FG_BLACK  , _BG_BLACK  , _BOLD       = 30, 40, 1
_FG_RED    , _BG_RED    , _SHADE      = 31, 41, 2
_FG_GREEN  , _BG_GREEN  , _ITALIC     = 32, 42, 3
_FG_YELLOW , _BG_YELLOW , _UNDERLINE  = 33, 43, 4
_FG_BLUE   , _BG_BLUE   , _BLINK      = 34, 44, 5
_FG_MAGENTA, _BG_MAGENTA, _INVERSE    = 35, 45, 7
_FG_CYAN   , _BG_CYAN   , _STRIKE     = 36, 46, 9
_FG_WHITE  , _BG_WHITE  , _BOLD_ULINE = 37, 47, 21

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

#_> STYLESHEET
_CH         = _FMT4.format(_BOLD_ULINE, _BOLD , _MAIN  , _BG_BLACK) # contrast header
_D          = _FMT1.format(_NORMAL)                                 # default ~ doesn't get removed
_E          = _FMT2.format(_BOLD  , _FG_RED   )                     # error
_W          = _FMT2.format(_BOLD  , _FG_YELLOW)                     # warning
_C1         = _FMT3.format(_BOLD  , _BRIGHT_FG, _BG    )            # contrast 1
_C1_        = _FMT3.format(_NORMAL,        _FG, _BG    )            # subcontrast 1
_C2         = _FMT3.format(_BOLD  , _BRIGHT_FG, _ALT_BG)            # contrast 2
_C2_        = _FMT3.format(_NORMAL,    _ALT_FG, _ALT_BG)            # subcontrast 2

#__> time
_SYSTIME    = '{}/{:02}/{:02} {:02}:{:02}:{:02}'
_NOW        = '\n{} System Time:{}{} {} {}\n'.format(_C1, _D, _C1_, _SYSTIME, _D)

#__> entry
_EHEADER    = '\n{} {:<26} {} {} {:<12} {}'.format(_CH, 'files', _D, _CH,'byte size', _D)
_ENTRIES    = ('{} {} {} {} {} {}'.format(_C1, '{:<26}', _D, _C1_, '{:>12}', _D),
               '{} {} {} {} {} {}'.format(_C2, '{:<26}', _D, _C2_, '{:>12}', _D))

#__> help
_HHEADER    = '\n{} {:<8} {} {} {:<30} {} {} {:<33} {}'.format(_CH, 'cmd', _D, _CH,'description', _D, _CH, 'example', _D)
_HELPS      = ('{} {} {} {} {} {} {} {} {}'.format(_C1, '{:<8}', _D, _C1_, '{:<30}', _D, _C1_, '{:<33}', _D),
               '{} {} {} {} {} {} {} {} {}'.format(_C2, '{:<8}', _D, _C2_, '{:<30}', _D, _C2_, '{:<33}', _D))

#_> sysinfo
_SHEADER    = '\n{} {:<78}{}'.format(_CH, 'sysinfo', _D)
_SYSINFO1   = '{} {}{} {} {}{}'.format(_C1, '{:<10}', _D, _C1_, '{:<66}', _D)
_SYSINFO2   = '{} {}{} {} {}{}'.format(_C2, '{:<10}', _D, _C2_, '{:<66}', _D)

#_> print
_FILE       = '\n{} {}{} bytes {}'.format(_CH, '{:<58}', '{:>13}', _FMT3.format(_NORMAL, _FG_WHITE, _BG_BLACK))
_COMBINE    = '{}{}'

#_> generic one column
_IHEADER    = '\n{} {}{}'.format(_CH, '{:<42}', _D)
_ITEMS      = ('{} {}{}'.format(_C1, '{:<42}', _D),
               '{} {}{}'.format(_C2, '{:<42}', _D))

#_> continuous
_TWARNING   = '\n{} Command ({}) for use with {} only! {}\n'.format(_W, '{}', '{}', _D)
_EWARNING   = '\n{} Command ({}) does not exist! {}\n'.format(_W, '{}', _D)
_ERROR      = '\n{} {} {}\n'.format(_E, '{}', _D)
_OSERROR    = '\n{} {} {} ({}) {}\n'.format(_E, '{}', '{}', '{}', _D)
_CMDLINE    = '{}{}{}:{}{} $ {}'.format(_FMT2.format(_BOLD, _MAIN), '{}@{}', _D, _FMT3.format(_BOLD, _SHADE, _MAIN), '~{}', _D)

#__> CLI
_CMDS       = ('exit', 'help', 'sysinfo', 'clr', 'now', 'collect', 'list', 'cd', 'print', 'mkdir', 'del', 'rename', 'find', 'syspath', 'copy')
_AUTOLIST   = ('mkdir', 'del', 'rename', 'cd')
_FILEONLY   = ('copy', 'print', 'rename')
_FLDRONLY   = ('list', 'cd')

#_> description
_DESC       = ('exit the CLI', 'prints this help info', 'print system info', 'clear the terminal', 'prints system time', 'run garbage collection',
               'lists the current directory', 'change directory', 'print requested file','creates a new directory', 'delete a file or folder', 'rename a file', 
               'find all with term from cwd', 'print or [modify] syspath', 'copy a file')
               
#_> examples
_EXS        = ('', '', '', '', '', '', 'list [path]', 'cd path', 'print fileName [r | rb]', 'mkdir dirName', 'del fileOrDirName', 'rename oldname newname',
               'find term', 'syspath [add | del]', 'copy source destination [w | wb]')

_PATH_ERR   = 'Path Error:'
_DEL_ERR    = 'Cannot Delete:' 

#__> ALL FORMATS ARE CREATED. REMOVE DEAD WEIGHT AND RECLAIM MEMORY
del urecompile
del _FMT1, _FMT2, _FMT3, _FMT4 
del _E, _W, _CH, _C1, _C1_, _C2, _C2_
del _MAIN, _BRIGHT_FG, _FG, _BG, _ALT_FG, _ALT_BG, 
del _FG_BLACK, _FG_RED, _FG_GREEN, _FG_YELLOW, _FG_BLUE, _FG_MAGENTA, _FG_CYAN, _FG_WHITE
del _BG_BLACK, _BG_RED, _BG_GREEN, _BG_YELLOW, _BG_BLUE, _BG_MAGENTA, _BG_CYAN, _BG_WHITE
del _NORMAL, _BOLD, _SHADE, _ITALIC, _UNDERLINE, _BLINK, _INVERSE, _STRIKE, _BOLD_ULINE 
gccollect()


class CLI(object):
    #__> COMMAND LINE INTERFACE
    def __init__(self, clear:bool=True, user:str='user') -> None:
        print('' if not clear else '\n'*100)
        host = uos.uname().sysname
        CLI.__list(uos.getcwd())
        
        while True:
            args = input(_CMDLINE.format(user, host, uos.getcwd()))
            
            if not args:
                continue
            
            args = CLI.__tokenize(args).split(' ')
            cmd  = args.pop(0)
            
            if not cmd in _CMDS:
                print(_EWARNING.format(cmd))
                continue
            
            term = uos.getcwd() if len(args) < 1 else args.pop(0)
            foo  = None         if len(args) < 1 else args.pop(0)    # contextual
            bar  = None         if len(args) < 1 else args.pop(0)    # contextual
            path = CLI.__fullpath(term)
            
            try:
                mode = uos.stat(path)[0]
            except OSError as err:
                if   cmd == 'mkdir'  : uos.mkdir(path)
                elif cmd == 'find'   :
                    print(_IHEADER.format('found'))
                    CLI.__find(term.replace('%20', ' '))
                    print()
                    continue
                elif cmd == 'syspath': 
                    CLI.__syspath(term, foo)                         #add or del
                    continue
                else:
                    print(_OSERROR.format(_PATH_ERR, path, err))
                    continue
                    
            if cmd in _FILEONLY and (mode & _STAT_FLDR):
                print(_TWARNING.format(cmd, 'file'))
                continue
            elif cmd in _FLDRONLY and (mode & _STAT_FILE):
                print(_TWARNING.format(cmd, 'directory'))
                continue
                    
            if cmd in _CMDS:
                if   cmd == 'exit'   : break
                elif cmd == 'clr'    : print('\n'*100)
                elif cmd == 'now'    : print(_NOW.format(*tnow(ttime())[:6]))
                elif cmd == 'collect': gccollect(), CLI.__sysinfo()
                elif cmd == 'help'   : CLI.__help()
                elif cmd == 'sysinfo': CLI.__sysinfo()
                elif cmd == 'syspath': CLI.__syspath(None, None)     #print
                elif cmd == 'copy'   : CLI.__copy(path, foo, bar)    if mode & _STAT_FILE else None
                elif cmd == 'list'   : CLI.__list(path)              if mode & _STAT_FLDR else None
                elif cmd == 'print'  : CLI.__print(path, foo)        if mode & _STAT_FILE else None
                elif cmd == 'cd'     : uos.chdir(path)               if mode & _STAT_FLDR else None
                elif cmd == 'rename' : uos.rename(path, foo) if foo and mode & _STAT_FILE else None
                elif cmd == 'del'    : 
                    uos.chdir('/'.join(path.split('/')[0:-1]))       #goto parent directory
                    CLI.__delete(path, mode)
                
            if cmd in _AUTOLIST:
                CLI.__list(uos.getcwd())
                
        gccollect() #clean up before leaving
                
    #__> Tokenize Quoted Strings So They Don't Get Split On Space  
    @staticmethod
    def __tokenize(args):
        m, g, n = _QUOTED.search(args), [], 0
        while m:
            n += m.end()
            g.append(m.groups())
            m = _QUOTED.search(args[n:])
            
        for a, b in g:
            args = args.replace(a, b.replace(' ', '%20'))
        
        return args
      
    #__> Reads And Yields A File In 512 Byte Chunks
    @staticmethod
    def __read(path:str, format='r', buffsize:int=512):
        buff = bytearray(buffsize)
        try:
            file = open(path, 'rb')
        except OSError as err:
            print(_OSERROR.format(_PATH_ERR, CLI.__fullpath(path), err))
            return None
        
        while True:
            buff = file.read(buffsize)
            try:
                yield buff if format == 'rb' else buff.decode()
            except UnicodeError as err:
                print(_ERROR.format('UnicodeError: this file needs to be read as bytes.\n Use the rb flag with print or the wb flag with copy.'))
                return None
            if not buff:
                file.close()
                break;
                
        return None
        
    #__> Try To Determine Absolute Path
    @staticmethod
    def __fullpath(path:str) -> str:
        path = path.replace('%20', ' ')
        if path[0] == '/': #considered absolute
            return path
            
        #else considered relative
        head = [d for d in uos.getcwd().split('/') if d]
        tail = []
        
        for d in path.split('/'):
            if d == '..':
                head.pop() if len(head) else None
            else: tail.append(d)
            
        full_path = r'/{}'.format('/'.join(head+tail))
        
        return full_path
    
    #__> Sorts A List By Directories First Plus Alphabetical First Letter Plus Name Length
    @staticmethod            
    def __dirsort(item:str) -> int:
        return ((uos.stat(item)[0] & _STAT_FILE)*1000)+(ord(item[0])*10)+len(item)
    
    #__> Prints System Info And Other Related Information 
    @staticmethod
    def __sysinfo() -> None: 
        print(_SHEADER)
        print(_SYSINFO1.format('machine' , uos.uname().machine))
        print(_SYSINFO2.format('sysname' , uos.uname().sysname))
        print(_SYSINFO1.format('systime' , _SYSTIME.format(*tnow(ttime())[:6])))
        print(_SYSINFO2.format('memalloc', gcmemalloc()))
        print(_SYSINFO1.format('memfree' , gcmemfree()))
        print(_SYSINFO2.format('upython' , uos.uname().version))
        print()
    
    #__> Prints The Help Info
    @staticmethod
    def __help() -> None:
        print(_HHEADER)
        for n, (cmd, desc, ex) in enumerate(zip(_CMDS, _DESC, _EXS)):
            print(_HELPS[n%2].format(cmd, desc, (ex if len(ex) else '')))
        print()
        
    #__> Copy A File To A Destination Path And List Destination Directory When Copy Is Complete
    @staticmethod
    def __copy(source:str, dest:str, fmt:str) -> None:
        dest = CLI.__fullpath(dest)
        fmt  = 'w' if fmt is None or fmt == 'w' else 'wb'
        fmt2 = 'r' if fmt == 'w' else 'rb'
        
        try:
            with open(dest, fmt) as out:
                for output in CLI.__read(source, fmt2): 
                    if not output is None: out.write(output)
        except OSError as err:
            print(_OSERROR.format(_PATH_ERR, 'source: {} destination: {}'.format(source, dest), err))
        
        #list parent directory of new copy
        dest = '/'.join(dest.split('/')[0:-1])
        try:    
            uos.chdir(dest)
            CLI.__list(dest)
        except OSError as err:
            print(_OSERROR.format(_PATH_ERR, dest, err))
                    
    #__> Lists The Contents Of The Supplied Path
    @staticmethod
    def __list(path:str) -> None:
        print(_EHEADER)
        try:
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
        except OSError as err:
            print(_OSERROR.format(_PATH_ERR, path, err))
    
    #__> Prints The Contents Of The supplied Path   
    @staticmethod
    def __print(path:str, fmt:str) -> None:
        hold = ''
        fmt  = fmt if fmt else 'r'
        print(_FILE.format(path, uos.stat(path)[6]))
        for output in CLI.__read(path, fmt):
            if not output is None:
                #__> New Line Juggler
                L, N = len(output), (-1 if fmt == 'rb' else output.rfind('\n')) #length, last position of \n
                n    = N if N > -1 else L                                       #last position of \n if \n else length
                out  = _COMBINE.format(hold, output[0:n])                       #left  side of last \n if \n
                hold = output[n+1:] if n < L else ''                            #right side of last \n if \n
                if out:
                    print(out)      #print up to last \n if \n (and provides previous "last \n" via behavior)
        print(_D) # this is why _D doesn't get removed putting an equivalent here is no different than keeping _D

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
            print(_OSERROR.format(_DEL_ERR, path, err))
      
    #__> Find All Items Containing Term Recursing from CWD
    @staticmethod
    def __find(term:str, r:int=1) -> int:
        cwd = uos.getcwd()
        for item in uos.listdir():
            ip = CLI.__fullpath(item)
            if term in item:
                r = not r
                print(_ITEMS[r].format(ip))
            if uos.stat(ip)[0] & _STAT_FLDR:
                uos.chdir(ip)
                r = CLI.__find(term, r)
                uos.chdir(cwd)
        return r
        
    #__> Print And Add or Remove Applied To sys.path
    @staticmethod
    def __syspath(term:str, path:str) -> None:
        if term in ('add', 'del') and path:
            path = CLI.__fullpath(path)
            try:
                if uos.stat(path)[0] & _STAT_FLDR and not path in syspath:
                    if   term == 'add': syspath.append(path)
                    elif term == 'del': syspath.remove(path)
            except OSError as err:
                print(_OSERROR.format(_PATH_ERR, path, err))
                return
                   
        print(_IHEADER.format('syspaths'))
        r = 1;
        for path in syspath:
            if path:
                r = not r
                print(_ITEMS[r].format(path))
        print()

