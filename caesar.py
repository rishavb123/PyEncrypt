from encryption import Encryption

# Preproccess Raw Text
def to_lower_case(s: str) -> str:
    """Converts string to lower case string

    Args:
        s (str): the string to convert to lower case

    Returns:
        str: the lower case string
    """
    return s.lower()


preprocess_raw_string = [to_lower_case]

# Preprocess Characters
def numeric_representation(c: str) -> int:
    """Converts a character to a numeric representation

    Args:
        c (str): the character to convert to a numeric representation

    Returns:
        int: the numeric representation of the character
    """
    return ord(c) - 97


preprocess_groups = [numeric_representation]

# Post Process Characters
def character_representation(c: int) -> str:
    """Converts a numeric representation to a character

    Args:
        c (int): the numeric representation to convert to a character

    Returns:
        str: the character representation of the numeric representation
    """
    return chr(c + 97)


postprocess_groups = [character_representation]


class CaesarCipher(Encryption):
    """A Caesar Cipher class to perform shift ciphers. Inherits from the Encryption class"""

    def __init__(self, shift: int) -> None:
        """Initialize the Caesar Cipher class

        Args:
            shift (int): The amount to shift the characters by
        """
        self.shift = shift

        super().__init__(
            preprocess_raw_string=preprocess_raw_string,
            preprocess=preprocess_groups,
            postprocess=postprocess_groups,
        )

    def _encrypt_group(self, c: int) -> int:
        """Encrypts a single character

        Args:
            c (int): the numeric representation of the character

        Returns:
            int: the encrypted numeric representation of the character
        """
        if c == -65:
            return -65
        return (c + self.shift) % 26

    def print_encryption_table(
        self,
        plaintext: str,
        cell_width=5,
        output_processor=lambda x: " " if x == -65 else str(x),
        show_steps=False,
    ) -> str:
        """Prints the encryption table for the given plaintext

        Args:
            plaintext (str): The plaintext to encrypt
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            output_processor (function, optional): the function to process the output of the encryption steps. Defaults to lambda x: " " if x == -65 else str(x).
            show_steps (bool, optional): whether to show the steps of the encryption. Defaults to False.

        Returns:
            str: the encrypted ciphertext
        """
        return super().print_encryption_table(
            plaintext,
            cell_width=cell_width,
            output_processor=output_processor,
            show_steps=show_steps,
        )

    def print_decryption_table(
        self,
        ciphertext: str,
        cell_width=5,
        output_processor=lambda x: " " if x == -65 else str(x),
        show_steps=False,
    ) -> str:
        """Prints the decryption table for the given ciphertext

        Args:
            ciphertext (str): The ciphertext to encrypt
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            output_processor (function, optional): the function to process the output of the decryption steps. Defaults to lambda x: " " if x == -65 else str(x).
            show_steps (bool, optional): whether to show the steps of the decryption. Defaults to False.

        Returns:
            str: the decrypted plaintext
        """
        return super().print_decryption_table(
            ciphertext,
            cell_width=cell_width,
            output_processor=output_processor,
            show_steps=show_steps,
        )

    def _make_decryption_object(self) -> "CaesarCipher":
        """Makes a new CaesarCipher object that is the reverse of this one

        Returns:
            [type]: [description]
        """
        return CaesarCipher(-self.shift)


if __name__ == "__main__":

    cipher = CaesarCipher(5)
    plaintext = "discrete math is fun"

    cipher.print_decryption_table(
        cipher.print_encryption_table(plaintext, show_steps=True), show_steps=True
    )