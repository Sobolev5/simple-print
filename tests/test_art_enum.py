from simple_print import ArtEnum


def test_art_enum() -> None:
    """Test ArtEnum
    
    Run:
        pytest tests/test_art_enum.py -s
    """
    print(ArtEnum.PACMAN_1)
    print(ArtEnum.KEY)