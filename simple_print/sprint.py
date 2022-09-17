import os
import inspect
import traceback
from typing import Any, Union
from termcolor import cprint
from executing import Source


DEBUG = os.getenv("DEBUG","").lower() in ("1", "true", "yes", "y")
SIMPLE_PRINT_PATH_TO_FILE = os.getenv("SPRINT_PATH_TO_FILE","").lower() in ("1", "true", "yes", "y")


def _colored_print(arg:Any, arg_name:str, c:Union[None, str], b:Union[None, str], a:Union[None, str], i:int, p:bool, function_name:str, lineno:int, filename:str) -> None:  
    
    if i in range(1, 41):
        arg_name = "{} {}".format(" " * i, arg_name)
        
    if p:       
        cprint(f"{arg_name} | type {type(arg)} | line {lineno} | func {function_name} | file {filename}", color=c, on_color=b, attrs=[a] if a else [])
    else:
        cprint(f"{arg_name} | type {type(arg)} | line {lineno} | func {function_name}", color=c, on_color=b, attrs=[a] if a else [])


def sprint(*args, c:Union[None, str]="white", b:Union[None, str]=None, a:Union[None, str]="bold", i:int=0, p:bool=SIMPLE_PRINT_PATH_TO_FILE, s:bool=False, **kwargs) -> Union[None, str]:
    """     
    sprint:
    с:str ~ colors: ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    b:str ~ backgrounds: ["on_grey", "on_red", "on_green", "on_yellow", "on_blue", "on_magenta", "on_cyan"]
    a:str ~ attributes: bold, dark, underline, blink, reverse, concealed 
    i:int ~ indent: 1-40
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

        for j, arg in enumerate(args):
            try:
                arg_name = source.asttokens().get_text(call_node.args[j])
                _ = arg_name == arg or arg_name.strip('"').strip("'") == arg or arg_name.startswith('f"') or arg_name.startswith("f'")
                arg_name = f"{arg}" if _ else f"{arg_name} = {arg}"
            except:
                arg_name = f"{arg}"

            if s:
                arg_name = f"{arg_name} | {type(arg)} | func {function_name} | line {lineno} | file {filename}" if p else f"{arg_name} | {type(arg)} | func {function_name} | line {lineno}"
                arg_names.append(arg_name)
            else:
                _colored_print(arg, arg_name, c, b, a, i, p, function_name, lineno, filename)
        
        if s:
            return ";".join(arg_names)

