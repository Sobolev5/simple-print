import os
import io
import sys
import inspect
import traceback
from typing import Any, Union
from termcolor import cprint
from executing import Source
from contextlib import contextmanager


if os.getenv("SIMPLE_PRINT_ENABLED"):
    if os.getenv("SIMPLE_PRINT_ENABLED").lower() in ("1", "true", "yes", "y"):
        SIMPLE_PRINT_ENABLED = True
    else:
        SIMPLE_PRINT_ENABLED = False
else:
    SIMPLE_PRINT_ENABLED = True


if os.getenv("SIMPLE_PRINT_SHOW_PATH_TO_FILE"):
    if os.getenv("SIMPLE_PRINT_SHOW_PATH_TO_FILE").lower() in ("1", "true", "yes", "y"):
        SIMPLE_PRINT_SHOW_PATH_TO_FILE = True
    else:
        SIMPLE_PRINT_SHOW_PATH_TO_FILE = False    
else:
    SIMPLE_PRINT_SHOW_PATH_TO_FILE = False


def _colored_print(arg:Any, arg_name:str, c:Union[None, str], b:Union[None, str], a:Union[None, str], i:int, p:bool, function_name:str, lineno:int, filename:str) -> None:     

    if i in range(1, 41):
        arg_name = "{} {}".format(" " * i, arg_name)        
    
    if p:       
        cprint(f"░ {arg_name} | type {type(arg)} | line {lineno} | func {function_name} | file {filename}", color=c, on_color=b, attrs=[a] if a else [])
    else:
        cprint(f"░ {arg_name} | type {type(arg)} | line {lineno} | func {function_name}", color=c, on_color=b, attrs=[a] if a else [])


def sprint(*args, c:Union[None, str]="white", b:Union[None, str]=None, a:Union[None, str]=None, i:int=0, p:bool=SIMPLE_PRINT_SHOW_PATH_TO_FILE, s:bool=False, f:bool=False, **kwargs) -> Union[None, str]:
    """     
    с:str ~ colors: ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]  
    b:str ~ backgrounds: ["on_grey", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan"]  
    a:str ~ attributes: bold, dark, underline, blink, reverse, concealed   
    i:int ~ indent: 1-40  
    p:bool ~ path: show path to file       
    s:bool ~ string: return as string  
    f:bool ~ force: print anyway (override DEBUG ENV if exist)  
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
                except:
                    arg_name = code.replace("sprint", "", 1)[1:-1]  
                arg_name_not_required = arg_name == arg or \
                                arg_name.strip('"').strip("'") == arg or \
                                arg_name.startswith('f"') or \
                                arg_name.startswith("f'") or \
                                ".format" in arg_name or \
                                "%" in arg_name
                arg_name = f"{arg}" if arg_name_not_required else f"{arg_name} = {arg}"
            except Exception as e:
                arg_name = f"{arg}"
                
            try:
                if hasattr(arg, "id") and arg.id:
                    arg_name += f" ID={arg.id}"
            except:
                pass

            if s:
                arg_name = f"{arg_name} | {type(arg)} | func {function_name} | line {lineno} | file {filename}" if p else f"{arg_name} | {type(arg)} | func {function_name} | line {lineno}"
                arg_names.append(arg_name)
            else:
                _colored_print(arg, arg_name, c, b, a, i, p, function_name, lineno, filename)
        
        if s:
            return ";".join(arg_names)


@contextmanager
def SprintErr(DEBUG=True):

    def format_exception(ei) -> str:
        sio = io.StringIO()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == "\n":
            s = s[:-1]
        return s

    if DEBUG:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-3]

        cprint(f"░░░░░░░░░░ SprintErr. f_name={filename} lineno={lineno} [ ENTER ]", color="green")
        try:
            yield 
        except Exception as e:
            cprint(f"░░░░░░░░░░ SprintErr. f_name={filename} lineno={lineno} [ ERRORS FOUND ]\n", color="red")
            ei = sys.exc_info()
            print(format_exception(ei))
        finally:
            cprint(f"░░░░░░░░░░ SprintErr. f_name={filename} lineno={lineno} [ EXIT ]\n", color="green")


