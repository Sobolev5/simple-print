from simple_print import ArtEnum
from simple_print import spprint


def test_spprint():
    """Test spprint
    
    Run:
        pytest tests/test_spprint.py -s
    """
    spprint(ArtEnum.PACMAN_1, i=20)