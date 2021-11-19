from inspect import signature


def numeric_representation(c):
    """Create a numeric representation of a character.

    Args:
        c (string): the character to represent.

    Returns:
        int: the numeric representation of the character.
    """
    return ord(c) - ord("a")


def character_representation(n):
    """Create a character representation of a numeric value.

    Args:
        n (int): the numeric value to represent.

    Returns:
        string: the character representation of the numeric value.
    """
    return chr(ord("a") + n)


def function_wrapper(f):
    """Create a wrapper function for a given encryption function.

    Args:
        f (function): the encryption function (inputs and outputs a numeric representation).

    Returns:
        function: the wrapper function.
    """

    sig = signature(f)

    if len(sig.parameters) == 1:

        def wrapper(p_arr, i):
            """Wrapper function for a given encryption function

            Args:
                p_arr (list): list of the numeric representations of the characters to encrypt.
                i (int): the index of the character to encrypt.

            Returns:
                int: the encrypted numeric representation of the character.
            """
            if type(p_arr) != list or type(i) != int or i < 0 or i >= len(p_arr):
                return "?"
            p = p_arr[i]
            if type(p) != int or p < 0 or p > 25:
                return p
            return f(p)

        return wrapper
    else:

        def wrapper(p_arr, i):
            """Wrapper function for a given encryption function

            Args:
                p_arr (list): list of the numeric representations of the characters to encrypt.
                i (int): the index of the character to encrypt.

            Returns:
                int: the encrypted numeric representation of the character.
            """
            if type(p_arr) != list or type(i) != int or i < 0 or i >= len(p_arr):
                return "?"
            return f(p_arr, i)

        return wrapper


def print_encryption_table(
    s,
    f,
    cell_width=5,
    print_numeric_representation=False,
    preprocess=lambda arr: [" " if a == -65 else a for a in arr],
    name=None,
):
    """Print an encryption table for a given string.

    Args:
        s (string): the string to encrypt.
        f (function): the encryption function (inputs and outputs a numeric representation).
        cell_width (int, optional): the width of each table cell. Defaults to 5.
        print_numeric_representation (bool, optional): whether or not to print numeric representations. Defaults to False.
        preprocess (function, optional): a preprocessor function before output. Defaults to lambdaarr:[" " if a == -65 else a for a in arr].
        name (string, optional): the name of the encryption table. Defaults to None.

    Returns:
        string: the encrypted string.
    """

    f = function_wrapper(f)

    print(f"Encryption Table - {name}:" if name else "Encryption Table:")
    i_arr = list(range(len(s)))
    s_arr = list(s)
    p_arr = [numeric_representation(c) for c in s_arr]
    q_arr = [f(p_arr, i) for i in i_arr]
    t_arr = [character_representation(q) for q in q_arr]

    i_str = "".join(["{:^" + str(cell_width) + "}|" for _ in i_arr])
    s_str = "".join(["{:^" + str(cell_width) + "}|" for _ in s_arr])
    p_str = "".join(["{:^" + str(cell_width) + "}|" for _ in p_arr])
    q_str = "".join(["{:^" + str(cell_width) + "}|" for _ in q_arr])
    t_str = "".join(["{:^" + str(cell_width) + "}|" for _ in t_arr])

    i_str = f"{'i':^{cell_width}}|" + i_str.format(*preprocess(i_arr))
    line_str = "-" * len(i_str)

    print(line_str)
    print(i_str)

    print(line_str)
    print(f"{'s[i]':^{cell_width}}|" + s_str.format(*preprocess(s_arr)))

    if print_numeric_representation:
        print(line_str)
        print(f"{'pi':^{cell_width}}|" + p_str.format(*preprocess(p_arr)))

        print(line_str)
        print(f"{'qi':^{cell_width}}|" + q_str.format(*preprocess(q_arr)))

    print(line_str)
    print(f"{'t[i]':^{cell_width}}|" + t_str.format(*preprocess(t_arr)))

    print(line_str)

    return "".join(t_arr)


def encypt(s, f):
    """Encrypt a string using a given encryption function.

    Args:
        s (string): the string to encrypt.
        f (function): the encryption function (inputs and outputs a numeric representation).

    Returns:
        string: the encrypted string.
    """

    f = function_wrapper(f)

    s_arr = list(s)
    p_arr = [numeric_representation(c) for c in s_arr]
    q_arr = [f(p_arr, i) for i in range(len(p_arr))]
    t_arr = [character_representation(q) for q in q_arr]

    return "".join(t_arr)
