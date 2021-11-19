from encryption import Encryption

# Preproccess Raw Text
def to_lower_case(s: str) -> str:
    return s.lower()


preprocess_raw_string = [to_lower_case]

# Preprocess Characters
def numeric_representation(c: str) -> int:
    return ord(c) - 97


preprocess_groups = [numeric_representation]

# Post Process Characters
def character_representation(c: int) -> str:
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
        self, plaintext: str, cell_width=5, show_steps=False
    ) -> str:
        """Prints the encryption table for the given plaintext

        Args:
            plaintext (str): The plaintext to encrypt
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            show_steps (bool, optional): whether to show the steps of the encryption. Defaults to False.

        Returns:
            str: the encrypted ciphertext
        """
        return super().print_encryption_table(
            plaintext,
            cell_width=cell_width,
            output_processor=lambda x: " " if x == -65 else str(x),
            show_steps=show_steps,
        )

    def make_decryption_object(self) -> "CaesarCipher":
        """Makes a new CaesarCipher object that is the reverse of this one

        Returns:
            [type]: [description]
        """
        return CaesarCipher(-self.shift)


if __name__ == "__main__":

    cipher = CaesarCipher(5)
    plaintext = "discrete math is fun"

    cipher.print_encryption_table(plaintext, show_steps=True)

    cipher.make_decryption_object().print_encryption_table(
        cipher.print_encryption_table(plaintext, show_steps=True), show_steps=True
    )
