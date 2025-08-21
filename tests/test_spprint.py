from simple_print import spprint


def test_spprint():
    """Test spprint.

    Run:
        pytest tests/test_spprint.py -s

    """

    spprint({"hello":"world", "lorem": "ipsum"}, i=20)