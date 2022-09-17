import os
import inspect
import traceback
from typing import Any, Union
from termcolor import cprint
from executing import Source


DEBUG = os.getenv("DEBUG","").lower() in ("1", "true", "yes", "y")
SIMPLE_PRINT_PATH_TO_FILE = os.getenv("SPRINT_PATH_TO_FILE","").lower() in ("1", "true", "yes", "y")


def _colored_print(arg:Any, arg_name:str, c:Union[None, str], b:Union[None, str], a:Union[None, str], p:bool, function_name:str, lineno:int, filename:str) -> None:  
    prefix_1, prefix_2 = ('·······', '·······') if p else ('···', '···') 
    if p:       
        cprint(f"{prefix_1} {arg_name} | type {type(arg)} | line {lineno} | func {function_name}", color=c, on_color=b, attrs=[a] if a else [])
        cprint(f"{prefix_2} file {filename}", color=c, on_color=b, attrs=[a])
    else:
        cprint(f"{prefix_1} {arg_name} | type {type(arg)} | line {lineno} | func {function_name}", color=c, on_color=b, attrs=[a] if a else [])


def sprint(*args, c:Union[None, str]="white", b:Union[None, str]=None, a:Union[None, str]="bold", p:bool=SIMPLE_PRINT_PATH_TO_FILE, s:bool=False, **kwargs) -> Union[None, str]:
    """     
    sprint:
    с:str ~ colors: ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    b:str ~ backgrounds: ["on_grey", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan"]
    a:str ~ attributes: bold, dark, underline, blink, reverse, concealed 
    p:bool ~ path: show path to file    
    s:bool ~ string: return as string

    github: https://github.com/Sobolev5/simple-print

    """

    if DEBUG:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]
        call_frame = inspect.currentframe().f_back
        call_node = Source.executing(call_frame).node
        source = Source.for_frame(call_frame)

        if s:
            arg_names = []

        for i, arg in enumerate(args):
            try:
                arg_name = source.asttokens().get_text(call_node.args[i])
                _ = arg_name == arg or arg_name.strip('"').strip("'") == arg or arg_name.startswith('f"') or arg_name.startswith("f'")
                arg_name = f"{arg}" if _ else f"{arg_name} = {arg}"
            except:
                arg_name = f"{arg}"

            if s:
                arg_name = f"{arg_name} | {type(arg)} | func {function_name} | line {lineno} | file {filename}" if p else f"{arg_name} | {type(arg)} | func {function_name} | line {lineno}"
                arg_names.append(arg_name)
            else:
                _colored_print(arg, arg_name, c, b, a, p, function_name, lineno, filename)
        
        if s:
            return ";".join(arg_names)

