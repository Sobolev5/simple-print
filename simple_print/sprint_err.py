import io
import sys
import traceback
from contextlib import contextmanager
from .consts import SIMPLE_PRINT_ENABLED
from .sprint import _colorize


@contextmanager
def SprintErr(l: int = 20):  # noqa
    """Minified error traceback.

    Args:
        l (int, optional): line numbers. Defaults to 20.

    Example:

    bob = []
    with SprintErr(l=40):
        print(bob[2]) >>> pretty error tb (show 40 lines).

    """

    if SIMPLE_PRINT_ENABLED:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-3]
        try:
            yield
        except Exception:
            ei = sys.exc_info()
            exception_type = ei[0].__name__
            exception_msg = str(ei[1])
            sio = io.StringIO()
            traceback.print_exception(ei[0], ei[1], ei[2], None, sio)
            tb_lines = sio.getvalue().splitlines()[-l:]
            sio.close()
            title = f"─ {exception_type}: {exception_msg} "
            location_text = f"{filename}:{lineno} in {function_name}"
            max_tb = max((len(line) for line in tb_lines), default=0)
            box_width = max(max_tb, len(title), len(location_text), 40)
            header = f"  ┌{title}{'─' * max(0, box_width + 2 - len(title))}┐"
            footer = f"  └{'─' * (box_width + 2)}┘"
            location = f"  │ {location_text.ljust(box_width)} │"
            tb_body = ""
            for tb_line in tb_lines:
                tb_body += f"  │ {tb_line.ljust(box_width)} │\n"
            output = (
                f"\n{header}\n"
                f"{location}\n"
                f"  │{' ' * (box_width + 2)}│\n"
                f"{tb_body}"
                f"{footer}\n"
            )
            print(_colorize(output, color="red"))
