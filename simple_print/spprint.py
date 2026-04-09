import inspect
from pprint import pformat

from .consts import SIMPLE_PRINT_ENABLED
from .sprint import _colorize


def spprint(
    data: dict,
    i=0,
    c="cyan",
) -> None:
    """Pretty print dict with a box frame.

    Args:
        data (dict): dict
        i (int, optional): indent. Defaults to 0.
        c (str, optional): color. Defaults to "cyan".
    """

    if not SIMPLE_PRINT_ENABLED:
        return

    curr_frame = inspect.currentframe()
    call_frame = curr_frame.f_back
    filename = call_frame.f_code.co_filename
    lineno = call_frame.f_lineno
    function_name = call_frame.f_code.co_name

    content_lines = pformat(data).splitlines()
    location_text = f"{filename}:{lineno} in {function_name}"
    title = f"─ spprint "

    max_content = max((len(line) for line in content_lines), default=0)
    box_width = max(max_content, len(title), len(location_text), 40)

    header = f"  ┌{title}{'─' * max(0, box_width + 2 - len(title))}┐"
    footer = f"  └{'─' * (box_width + 2)}┘"
    location = f"  │ {location_text.ljust(box_width)} │"

    body = ""
    for line in content_lines:
        body += f"{' ' * i}  │ {line.ljust(box_width)} │\n"

    output = (
        f"\n{' ' * i}{header}\n"
        f"{' ' * i}{location}\n"
        f"{' ' * i}  │{' ' * (box_width + 2)}│\n"
        f"{body}"
        f"{' ' * i}{footer}\n"
    )
    print(_colorize(output, color=c))
