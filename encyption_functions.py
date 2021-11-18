def caesar_cipher(k):
    """Generates a shift function based on the key k.

    Args:
        k (int): the shift key

    Returns:
        function: the shift function
    """    
    return lambda x: (x + k) % 26