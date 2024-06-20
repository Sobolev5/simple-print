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

    def format_exception(ei) -> str:
        sio = io.StringIO()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        printed_tb = sio.getvalue()
        sio.close()
        s = ""
        for tb_line in printed_tb.splitlines()[-l:]:
            s += "▒ " + tb_line + "\n"
        return s

    if SIMPLE_PRINT_ENABLED:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-3]

        try:
            yield
        except Exception:
            ei = sys.exc_info()
            _colorize(
                f"\n▒ 😈 {function_name} lineno={lineno}\n"
                f"▒ u {filename}\n"
                f"{format_exception(ei)}",
                color="red",
            )
