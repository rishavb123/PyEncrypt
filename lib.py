def numeric_representation(c):
    """Create a numeric representation of a character.

    Args:
        c (string): the character to represent.

    Returns:
        int: the numeric representation of the character.
    """
    if c == ' ':
        return ' '
    return ord(c) - ord('a')

def character_representation(n):
    """Create a character representation of a numeric value.

    Args:
        n (int): the numeric value to represent.

    Returns:
        string: the character representation of the numeric value.
    """   
    if n == ' ':
        return ' '
    return chr(ord('a') + n)

def function_wrapper(f):
    """Create a wrapper function for a given encryption function.

    Args:
        f (function): the encryption function (inputs and outputs a numeric representation).

    Returns:
        function: the wrapper function.
    """
    def wrapper(p):
        """Wrapper function for a given encryption function.

        Args:
            p (int): the numeric representation of the character to encrypt.

        Returns:
            int: the encrypted numeric representation of the character.
        """
        if type(p) != int or p < 0 or p > 25:
            return p
        return f(p)
    return wrapper

def print_encryption_table(s, f, cell_width=5):
    """Print the encryption table for a given string and key.

    Args:
        s (string): the string to encrypt.
        f (function): the encryption function (inputs and outputs a numeric representation).
    """

    f = function_wrapper(f)

    print("Encryption table:")
    i_arr = list(range(len(s)))
    s_arr = list(s)
    p_arr = [numeric_representation(c) for c in s_arr]
    q_arr = [f(p) for p in p_arr]
    t_arr = [character_representation(q) for q in q_arr]

    i_str = ''.join(['{:^' + str(cell_width) + '}|' for i in i_arr])
    s_str = ''.join(['{:^' + str(cell_width) + '}|' for s in s_arr])
    p_str = ''.join(['{:^' + str(cell_width) + '}|' for p in p_arr])
    q_str = ''.join(['{:^' + str(cell_width) + '}|' for q in q_arr])
    t_str = ''.join(['{:^' + str(cell_width) + '}|' for t in t_arr])

    i_str = f"{'i':^{cell_width}}|" + i_str.format(*i_arr)
    line_str = '-' * len(i_str)

    print(line_str)
    print(i_str)

    print(line_str)
    print(f"{'s[i]':^{cell_width}}|" + s_str.format(*s_arr))

    print(line_str)
    print(f"{'pi':^{cell_width}}|" + p_str.format(*p_arr))

    print(line_str)
    print(f"{'qi':^{cell_width}}|" + q_str.format(*q_arr))

    print(line_str)
    print(f"{'t[i]':^{cell_width}}|" + t_str.format(*t_arr))

    print(line_str)