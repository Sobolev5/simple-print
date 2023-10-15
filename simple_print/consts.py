import os

_YES = ("1", "true", "yes", "y")

_ATTRIBUTES = dict(
        list(zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
            ],
            list(range(1, 9))
            ))
        )

_HIGHLIGHTS = dict(
        list(zip([
            'on_grey',
            'on_red',
            'on_green',
            'on_yellow',
            'on_blue',
            'on_magenta',
            'on_cyan',
            'on_white'
            ],
            list(range(40, 48))
            ))
        )

_COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            ],
            list(range(30, 39))
            ))
        )

_RESET = '\033[0m'

if os.getenv("SIMPLE_PRINT_ENABLED"):
    if os.getenv("SIMPLE_PRINT_ENABLED").lower() in _YES:
        SIMPLE_PRINT_ENABLED = True
    else:
        SIMPLE_PRINT_ENABLED = False
else:
    SIMPLE_PRINT_ENABLED = True

if os.getenv("SIMPLE_PRINT_SHOW_PATH_TO_FILE"):
    if os.getenv("SIMPLE_PRINT_SHOW_PATH_TO_FILE").lower() in _YES:
        SIMPLE_PRINT_SHOW_PATH_TO_FILE = True
    else:
        SIMPLE_PRINT_SHOW_PATH_TO_FILE = False    
else:
    SIMPLE_PRINT_SHOW_PATH_TO_FILE = False

if os.getenv("SIMPLE_PRINT_ADD_LINE_BREAK"):
    if os.getenv("SIMPLE_PRINT_ADD_LINE_BREAK").lower() in _YES:
        SIMPLE_PRINT_ADD_LINE_BREAK = True
    else:
        SIMPLE_PRINT_ADD_LINE_BREAK = False
else:
    SIMPLE_PRINT_ADD_LINE_BREAK = False
    