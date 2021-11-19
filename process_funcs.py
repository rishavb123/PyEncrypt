from utils import listify


@listify
def to_lower_case(s: str) -> str:
    """Converts string to lower case string

    Args:
        s (str): the string to convert to lower case

    Returns:
        str: the lower case string
    """
    return s.lower()


@listify
def numeric_representation(c: str) -> int:
    """Converts a character to a numeric representation

    Args:
        c (str): the character to convert to a numeric representation

    Returns:
        int: the numeric representation of the character
    """
    return ord(c) - 97


@listify
def character_representation(c: int) -> str:
    """Converts a numeric representation to a character

    Args:
        c (int): the numeric representation to convert to a character

    Returns:
        str: the character representation of the numeric representation
    """
    return chr(c + 97)


@listify
def pad_numeric_representation(c: int) -> str:
    """Pads a numeric representation to an even number of characters

    Args:
        c (int): the numeric representation to pad

    Returns:
        str: the padded numeric representation
    """
    s = str(c)
    return s.zfill(len(s) + 1) if len(s) % 2 == 1 else s


@listify
def convert_to_rsa_format(s: str) -> str:
    """Converts a string to the RSA format

    Args:
        s (str): the string to convert

    Returns:
        str: the string in the RSA format
    """
    return "".join(pad_numeric_representation(numeric_representation(c)) for c in s)


@listify
def remove_spaces(s: str) -> str:
    """Removes spaces from a string

    Args:
        s (str): the string to remove spaces from

    Returns:
        str: the string without spaces
    """
    return s.replace(" ", "")


@listify
def convert_each_2_digits_to_char(s: str) -> str:
    """Converts each two digits to a character

    Args:
        s (str): the string to convert

    Returns:
        str: the string converted to a character
    """
    return "".join(
        character_representation(int(s[i : i + 2])) for i in range(0, len(s), 2)
    )
