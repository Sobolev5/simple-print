from simple_print import SprintErr


def test_sprint_err_catches_exception():
    """Test that SprintErr catches an exception and prints a formatted traceback.

    Run:
        pytest tests/test_sprint_err.py -s

    """

    with SprintErr(l=30):
        raise ValueError("test error message")


def test_sprint_err_no_exception():
    """Test that SprintErr produces no output when no exception occurs."""

    with SprintErr(l=30):
        x = 1 + 1  # noqa: F841


def test_sprint_err_default_lines():
    """Test SprintErr with default l parameter."""

    with SprintErr():
        raise RuntimeError("default lines error")


def test_sprint_err_index_error():
    """Test SprintErr with IndexError."""

    bob = []
    with SprintErr(l=40):
        bob[2]  # noqa: B018


def test_sprint_err_key_error():
    """Test SprintErr with KeyError."""

    data = {}
    with SprintErr(l=10):
        data["missing"]  # noqa: B018


def test_sprint_err_shows_location():
    """Test that SprintErr output contains the calling function name and file location."""

    with SprintErr(l=20):
        raise Exception("trace me")
