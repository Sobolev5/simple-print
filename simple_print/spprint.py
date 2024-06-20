from pprint import pformat
from textwrap import indent


def spprint(
    data: dict,
    i=0,
) -> None:
    """Pretty print with indent.

    Args:
        data (dict): dict
        i (int, optional): indent. Defaults to 0.
    """
    print(indent(pformat(data), " " * i))
