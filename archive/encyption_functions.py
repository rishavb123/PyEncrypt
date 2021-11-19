import random


def caesar_cipher(k):
    """Generates a shift function based on the key k.

    Args:
        k (int): the shift key

    Returns:
        function: the shift function
    """
    return lambda x: (x + k) % 26


def transposition_cipher(sigma):
    """Generates a transposition function based on the permutation sigma.

    Args:
        sigma (list): the key

    Returns:
        function: the transposition function
    """

    def transposition_function(p_arr, i):
        """Transposition function.

        Args:
            p_arr (list): list of the numeric representations of the characters to encrypt.
            i (int): the index of the character to encrypt.

        Returns:
            int: the numeric representation of the encrypted character
        """
        div = i // len(sigma)
        mod = i % len(sigma)
        idx = div * len(sigma) + sigma[mod]
        return p_arr[idx]

    return transposition_function
