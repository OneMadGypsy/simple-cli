import uos, math
 
#__> CLI
_CMDS        = ('exit', 'help', 'list', 'clr', 'cd', 'print', 'mkdir', 'del')
_DESC        = ('exit the terminal', 'prints this help info', 'lists the current directory', 'clear the terminal', 
                'change directory', 'print requested file','creates a new directory', 'delete a file or folder ')
_EXS         = ('', '', '', '', 'cd path (../ is not supported)', 'print fileName [opt: \'r\' or \'rb\']', 'mkdir dirName', 'del fileOrDirName')
_STAT_FLDR   = const(0x4000)
_STAT_FILE   = const(0x8000)
_HEADER      = '\n{:<48}\n| {:<25} | {:<16} |\n{:<48}'
_ENTRY       = '| {:<25} | {:>16} |'
_SEP         = '{:<48}'.format('-'*48)
_DIRECTORY   = '| {:<44} |'
_FILEHEADER  = '\n{}\n {}/{} ~ {}b \n{}\n'
_COMBINE     = '{}{}'
_HELP        = ' {:<6}: {:<30} {}'
      
class CLI(object):
    def __init__(self, clear:bool=True, user:str='user') -> None:
        print('' if not clear else '\n'*100)
        
        while True:
            cmdline = input("{}@pico:~{} $ ".format(user, uos.getcwd()))
            chain   = cmdline.split(' ')
            cmd     = chain.pop(0)
            path    = uos.getcwd() if len(chain) < 1 else chain.pop(0)
            fmt     = 'r' if len(chain) < 1 else chain.pop(0)
            
            try:
                mode = uos.stat(path)[0]
            except OSError:
                if cmd == 'mkdir':
                    uos.mkdir(path)
                    CLI.__list(uos.getcwd())
            
            if cmd in _CMDS:
                if   cmd == 'exit':
                    break
                elif cmd == 'clr':
                    print('\n'*100)
                elif cmd == 'help':
                    CLI.__help()
                elif cmd == 'list':
                    if mode & _STAT_FLDR:
                        CLI.__list(path)
                elif cmd == 'cd':
                    if mode & _STAT_FLDR:
                        uos.chdir(path)
                elif cmd == 'print':
                    if mode & _STAT_FILE:
                        CLI.__print(path, fmt)
                elif cmd == 'del':
                    if mode & _STAT_FILE:
                        uos.remove(path)
                        CLI.__list(uos.getcwd())
                    elif mode & _STAT_FLDR:
                        uos.rmdir(path)
                        CLI.__list(uos.getcwd())
        
        
    @staticmethod
    def __read(path:str, format='r', buffsize:int=0x200):
        buff = bytearray(buffsize)
        try:
            file = open(path, 'rb')
        except OSError as err:
            pass
        
        while True:
            buff = file.read(buffsize)
            yield buff if format == 'rb' else buff.decode()
            if not buff:
                file.close()
                break;
                
        yield None
    
    @staticmethod            
    def __dirsort(item:str):
        f = (uos.stat(item)[0] & _STAT_FILE)
        return (f*1000)+(ord(item[0])*10)+len(item)
       
    @staticmethod
    def __help():
        print('\n COMMANDLINE OPTIONS:\n')
        for cmd, desc, ex in zip(_CMDS, _DESC, _EXS):
            print(_HELP.format(cmd, desc, ('ex: '+ex if len(ex) else '')))
        print()
        
    @staticmethod
    def __list(path:str) -> None:
        print(_HEADER.format(_SEP, 'file', 'bytesize', _SEP))
        fs = uos.listdir(path)
        fs.sort(reverse=False, key=CLI.__dirsort)
        for item in fs:
            mode, size  = uos.stat(item)[0], uos.stat(item)[6]
            if mode & _STAT_FLDR:
                if item != "System Volume Information":
                    print(_DIRECTORY.format(item+'/'))
            else:
                print(_ENTRY.format(item, size))
        print(_SEP, '\n')
        
    @staticmethod
    def __print(path:str, fmt:str='r') -> None:
        hold = ''
        print(_FILEHEADER.format(_SEP, uos.getcwd()[1:], path, uos.stat(path)[6], _SEP))
        for output in CLI.__read(path, fmt):
            if not output is None:
                L, N = len(output), (-1 if fmt == 'rb' else output.rfind('\n'))
                n    = N if N > -1 else L
                out  = _COMBINE.format(hold, output[0:n])
                if n < L:
                    hold = output[n+1:]
                if out:
                    print(out)
        print(_SEP, '\n')

