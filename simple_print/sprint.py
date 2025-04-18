import contextlib
import sys
import inspect
import traceback
from datetime import datetime
from typing import Any, Union
from executing import Source
from .consts import _HIGHLIGHTS, _ATTRIBUTES, _COLORS, _RESET
from .consts import SIMPLE_PRINT_ENABLED


def _colorize(
    text, 
    color=None, 
    on_color=None, 
    attrs=None,
) -> str:
    fmt_str = "\033[%dm%s"
    if color is not None:
        text = fmt_str % (_COLORS[color], text)

    if on_color is not None:
        text = fmt_str % (_HIGHLIGHTS[on_color], text)

    if attrs is not None:
        for attr in attrs:
            text = fmt_str % (_ATTRIBUTES[attr], text)

    text += _RESET
    return text


def _print(
    arg: Any,
    arg_name: str,
    c: Union[None, str], # noqa: E741
    b: Union[None, str], # noqa: E741
    a: Union[None, str], # noqa: E741
    i: int, # noqa: E741
    p: bool, # noqa: E741
    l: bool, # noqa: E741
    function_name: str,
    lineno: int,
    filename: str,
    stream="stdout",
) -> None:

    if i in range(1, 41):
        arg_name = "{} {}".format(" " * i, arg_name)
        
    s = _colorize(
        f"▒ {arg_name} ", 
        color=c, 
        on_color=b, 
        attrs=[a] if a else [],
    )
    
    now = datetime.now().strftime("%H:%M:%S")
    
    if not l:
        s += f"\33[90m | {type(arg)} | {lineno} | {function_name} | {now}\033[0m"
        
    if p:
        s += f"\33[90m | {filename} \033[0m"
    
    match stream:
        case "stdout":
            print(s, file=sys.stdout)
        case "stderr":
            print(s, file=sys.stderr)
        case "null":
            pass
        

def sprint(
    *args,
    c: Union[None, str] = "white", # noqa: E741
    b: Union[None, str] = None, # noqa: E741
    a: Union[None, str] = None, # noqa: E741
    i: int = 0, # noqa: E741
    p: bool = False, # noqa: E741
    l: bool = False, # noqa: E741
    s: bool = False, # noqa: E741
    r: bool = False, # noqa: E741
    f: bool = False, # noqa: E741
    stream="stdout",
) -> str | tuple[Any] | None:
    """Print variable value with its name in code.

    Args:
        c (Union[None, str], optional): color.
        grey, red, green, yellow, blue, magenta, cyan, white
        Defaults to white.

        b (Union[None, str], optional): background.
        on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan
        Defaults to None.

        a (Union[None, str], optional): attribute.
        bold, dark, underline, blink, reverse, concealed
        Defaults to None.

        i (int, optional): indent. Defaults to 0.

        p (bool, optional): path to file. Defaults to False.
        
        l (bool, optional): print without fn name and lineno. Defaults to False.

        s (bool, optional): return string. Defaults to False.

        r (bool, optional): print and return string. Defaults to False.

        f (bool, optional): force print anyway (override DEBUG ENV if exist). Defaults to False.

        stream (str, optional): stream. Defaults to "stdout".
        stdout", stderr, null

    Example:

    bob = 1
    sprint(bob)
    >>> bob = 1

    """

    if SIMPLE_PRINT_ENABLED or f:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]

        with contextlib.suppress(Exception):
            filename = "{}/{}".format(
                filename.split('/')[-2], 
                filename.split('/')[-1],
            )
        
        curr_frame = inspect.currentframe()
        if not curr_frame:    
            return None
        
        call_frame = curr_frame.f_back
        call_node = Source.executing(call_frame).node
        source = Source.for_frame(call_frame)

        if s:
            arg_names = []

        for j, arg in enumerate(args):
               
            try:
                arg_name = source.asttokens().get_text(call_node.args[j])
            except Exception:
                continue
            
            arg_name_not_required = (
                arg_name == arg
                or arg_name.strip('"').strip("'") == arg
                or arg_name.startswith('f"')
                or arg_name.startswith("f'")
                or ".format" in arg_name
                or "%" in arg_name
            )
            arg_name = f"{arg}" if arg_name_not_required else f"{arg_name} = {arg}"

            try:
                if hasattr(arg, "id") and arg.id:
                    arg_name += f" ID={arg.id}"
            except (AttributeError, Exception):
                pass

            if s:
                now = datetime.now().strftime("%H:%M:%S")
                arg_name = (
                    f"{arg_name} | {type(arg)} | {function_name} | {lineno} | {now} | {filename}"
                    if p
                    else f"{arg_name} | {type(arg)} | {function_name} | {lineno} | {now}"
                )
                arg_names.append(arg_name)
            else:
                _print(
                    arg,
                    arg_name,
                    c,
                    b,
                    a,
                    i,
                    p,
                    l,
                    function_name,
                    lineno,
                    filename,
                    stream=stream,
                )

        if s:
            return ";".join(arg_names)

        if r:
            if len(args) == 1:
                return args[0]
            else:
                return args
            
    return None


def lsprint(
    *args,
    c: Union[None, str] = "white", # noqa: E741
    b: Union[None, str] = None, # noqa: E741
    a: Union[None, str] = None, # noqa: E741
    i: int = 0, # noqa: E741
    s: bool = False, # noqa: E741
    r: bool = False, # noqa: E741
    f: bool = False, # noqa: E741
    stream="stdout",
    **kwargs,
) -> str | tuple[Any] | None:
    """Print variable value with its name in code.

    Args:
        c (Union[None, str], optional): color.
        grey, red, green, yellow, blue, magenta, cyan, white
        Defaults to white.

        b (Union[None, str], optional): background.
        on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan
        Defaults to None.

        a (Union[None, str], optional): attribute.
        bold, dark, underline, blink, reverse, concealed
        Defaults to None.

        i (int, optional): indent. Defaults to 0.

        s (bool, optional): return string. Defaults to False.

        r (bool, optional): print and return string. Defaults to False.

        f (bool, optional): force print anyway (override DEBUG ENV if exist). Defaults to False.

        stream (str, optional): stream. Defaults to "stdout".
        stdout", stderr, null

    Example:

    bob = 1
    lsprint(bob)
    >>> bob = 1

    """

    if SIMPLE_PRINT_ENABLED or f:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]
        
        curr_frame = inspect.currentframe()
        if not curr_frame:    
            return None
        
        call_frame = curr_frame.f_back
        call_node = Source.executing(call_frame).node
        source = Source.for_frame(call_frame)

        if s:
            arg_names = []

        for j, arg in enumerate(args):
               
            try:
                arg_name = source.asttokens().get_text(call_node.args[j])
            except Exception:
                continue
            
            arg_name_not_required = (
                arg_name == arg
                or arg_name.strip('"').strip("'") == arg
                or arg_name.startswith('f"')
                or arg_name.startswith("f'")
                or ".format" in arg_name
                or "%" in arg_name
            )
            arg_name = f"{arg}" if arg_name_not_required else f"{arg_name} = {arg}"

            try:
                if hasattr(arg, "id") and arg.id:
                    arg_name += f" ID={arg.id}"
            except (AttributeError, Exception):
                pass

            _print(
                arg,
                arg_name,
                c,
                b,
                a,
                i,
                False,
                True,
                function_name,
                lineno,
                filename,
                stream=stream,
            )

        if s:
            return ";".join(arg_names)

        if r:
            if len(args) == 1:
                return args[0]
            else:
                return args
            
    return None