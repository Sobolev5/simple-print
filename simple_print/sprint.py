import sys
import inspect
import traceback
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
    c: Union[None, str],
    b: Union[None, str],
    a: Union[None, str],
    i: int,
    p: bool,
    function_name: str,
    lineno: int,
    filename: str,
    stream="stdout",
) -> None:

    if i in range(1, 41):
        arg_name = "{} {}".format(" " * i, arg_name)
        
    s = _colorize(f"▒ {arg_name} " , color=c, on_color=b, attrs=[a] if a else [])
    s += _colorize( f" | typ {type(arg)} | ln {lineno} | fn {function_name}" , color="green", on_color=None, attrs=[])
        
    if p:
        s += f"\n▒ 🚀 {filename}"

    if stream == "stdout":
        print(s, file=sys.stdout)
    elif stream == "stderr":
        print(s, file=sys.stderr)
    elif stream == "null":
        # do nothing
        pass
        
def sprint(
    *args,
    c: Union[None, str] = "white",
    b: Union[None, str] = None,
    a: Union[None, str] = None,
    i: int = 0,
    p: bool = False,
    s: bool = False,
    r: bool = False,
    f: bool = False,
    stream="stdout",
) -> Union[None, str]:
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
        call_frame = inspect.currentframe().f_back
        call_node = Source.executing(call_frame).node
        source = Source.for_frame(call_frame)

        if s:
            arg_names = []

        for j, arg in enumerate(args):
               
            try:
                arg_name = source.asttokens().get_text(call_node.args[j])
            except Exception as exc:
                raise ModuleNotFoundError from exc
            
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
                arg_name = (
                    f"{arg_name} | {type(arg)} | func {function_name} | line {lineno} | file {filename}"
                    if p
                    else f"{arg_name} | {type(arg)} | func {function_name} | line {lineno}"
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
