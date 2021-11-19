def to_lower_case(s: str) -> str:
    """Converts string to lower case string

    Args:
        s (str): the string to convert to lower case

    Returns:
        str: the lower case string
    """
    return s.lower()


def numeric_representation(c: str) -> int:
    """Converts a character to a numeric representation

    Args:
        c (str): the character to convert to a numeric representation

    Returns:
        int: the numeric representation of the character
    """
    return ord(c) - 97


def character_representation(c: int) -> str:
    """Converts a numeric representation to a character

    Args:
        c (int): the numeric representation to convert to a character

    Returns:
        str: the character representation of the numeric representation
    """
    return chr(c + 97)
