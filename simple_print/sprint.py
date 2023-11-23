import io
import sys
import inspect
import traceback
from typing import Any, Union
from executing import Source
from contextlib import contextmanager
from pprint import pformat
from textwrap import indent
from .consts import _HIGHLIGHTS, _ATTRIBUTES,_COLORS, _RESET
from .consts import SIMPLE_PRINT_ENABLED 
from .consts import SIMPLE_PRINT_SHOW_PATH_TO_FILE
from .consts import SIMPLE_PRINT_ADD_LINE_BREAK


def _colorize(
        text, 
        color=None, 
        on_color=None, 
        attrs=None, 
        stream="stdout"
    ) -> None:

    fmt_str = '\033[%dm%s'
    if color is not None:
        text = fmt_str % (_COLORS[color], text)

    if on_color is not None:
        text = fmt_str % (_HIGHLIGHTS[on_color], text)

    if attrs is not None:
        for attr in attrs:
            text = fmt_str % (_ATTRIBUTES[attr], text)

    text += _RESET
    if stream == "stderr":
        print(text, file=sys.stderr)
    else:
        print(text, file=sys.stdout)


def _print(
        arg:Any, 
        arg_name:str, 
        c:Union[None, str], 
        b:Union[None, str], 
        a:Union[None, str], 
        i:int, p:bool, 
        function_name:str, 
        lineno:int, 
        filename:str,
        stream="stdout"
    ) -> None:     

    if i in range(1, 41):
        arg_name = "{} {}".format(" " * i, arg_name)        
    
    if p:     
        if i > 0:
            s = f"░ {arg_name} | type {type(arg)} | line {lineno} |"\
            f" func {function_name} | {filename}" 
        else:
            s = f"░ {arg_name} | type {type(arg)} | line {lineno} |"\
            f" func {function_name}\n░ 📁 {filename}"  
        if SIMPLE_PRINT_ADD_LINE_BREAK:
            s += "\n"        
        _colorize(
            s,
            color=c, on_color=b, attrs=[a] if a else [], stream=stream
        )
    else:
        s = f"░ {arg_name} | type {type(arg)} | line {lineno} | func {function_name}"
        if SIMPLE_PRINT_ADD_LINE_BREAK:
            s += "\n" 
        _colorize(
            s, 
            color=c, on_color=b, attrs=[a] if a else [], stream=stream
        )


def sprint(
        *args, 
        c:Union[None, str]="white", 
        b:Union[None, str]=None, 
        a:Union[None, str]=None, 
        i:int=0, 
        p:bool=SIMPLE_PRINT_SHOW_PATH_TO_FILE, 
        s:bool=False, 
        r:bool=False,
        f:bool=False, 
        stream="stdout",
        **kwargs
    ) -> Union[None, str]:
    """ 
    Usage:
    bob = 1
    sprint(var) >>> bob = 1

    Attrs:
    с:str ~ colors: ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]  
    b:str ~ backgrounds: ["on_grey", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan"]  
    a:str ~ attributes: bold, dark, underline, blink, reverse, concealed   
    i:int ~ indent: 1-40  
    p:bool ~ path: show path to file       
    s:bool ~ string: return as string  
    r:bool ~ string: print and return as string
    f:bool ~ force: print anyway (override DEBUG ENV if exist) 
    stream: ~ standard output & error: ["stdout", "stderr"] 
    github: https://github.com/Sobolev5/simple-print   
    """

    if SIMPLE_PRINT_ENABLED or f:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]
        call_frame = inspect.currentframe().f_back
        call_node = Source.executing(call_frame).node
        source = Source.for_frame(call_frame)

        if s:
            arg_names = []

        for j, arg in enumerate(args):
            try:       
                try:
                    arg_name = source.asttokens().get_text(call_node.args[j])
                except (KeyError, Exception):
                    arg_name = code.replace("sprint", "", 1)[1:-1]  
                arg_name_not_required = arg_name == arg or \
                                arg_name.strip('"').strip("'") == arg or \
                                arg_name.startswith('f"') or \
                                arg_name.startswith("f'") or \
                                ".format" in arg_name or \
                                "%" in arg_name
                arg_name = f"{arg}" if arg_name_not_required else f"{arg_name} = {arg}"
            except Exception:
                arg_name = f"{arg}"
                
            try:
                if hasattr(arg, "id") and arg.id:
                    arg_name += f" ID={arg.id}"
            except (AttributeError, Exception):
                pass

            if s:
                arg_name =\
                f"{arg_name} | {type(arg)} | func {function_name} | line {lineno} | file {filename}"\
                if p else f"{arg_name} | {type(arg)} | func {function_name} | line {lineno}" 
                arg_names.append(arg_name)
            else:
                _print(
                    arg, arg_name, c, b, a, i, p, function_name, lineno, filename,
                    stream=stream
                )
        
        if s:
            return ";".join(arg_names)
        
        if r:
            if len(args) == 1:
                return args[0]
            else:
                return args


def pprint(data:dict, i=0) -> None:
    print(indent(pformat(data),' ' * i))


@contextmanager
def SprintErr(l:int=20) -> None:
    """ 
    Usage:
    bob = []
    with SprintErr(l=40):
        print(bob[2]) >>> pretty error tb (show 40 lines)
    """
    def format_exception(ei) -> str:
        sio = io.StringIO()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        printed_tb = sio.getvalue()
        sio.close()    
        s = ""    
        for tb_line in printed_tb.splitlines()[-l:]:
            s += "░ " + tb_line + "\n"
        return s

    if SIMPLE_PRINT_ENABLED:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-3]

        try:
            yield 
        except Exception:
            ei = sys.exc_info()
            print(
                f"░ 🟥 {function_name} lineno={lineno}"
            )
            print(
                f"░ 📁 {filename}\n"
            )      
            print(format_exception(ei))



