from typing import List

from encryption import Encryption
from process_funcs import (
    to_lower_case,
    numeric_representation,
    character_representation,
)
from utils import list_and_space_output_processor

# Preproccess Raw Text
preprocess_raw_string = [to_lower_case]

# Preprocess Characters
preprocess_groups = [list, numeric_representation]

# Post Process Characters
postprocess_groups = [character_representation, "".join]


class VigenereCipher(Encryption):
    """A Vigenere Cipher class to perform shift ciphers. Inherits from the Encryption class"""

    def __init__(self, key: str) -> None:
        """Initialize the Vigenere Cipher class

        Args:
            key (str): The key to use for the encryption
        """
        self.key = numeric_representation(list(key))

        super().__init__(
            preprocess_raw_string=preprocess_raw_string,
            preprocess=preprocess_groups,
            postprocess=postprocess_groups,
            group_by=-1,
        )

    def _encrypt_group(self, l: List[int]) -> List[int]:
        """Encrypts the full string using a vigenere cipher

        Args:
            l (List[int]): The list of numeric representation of characters to encrypt

        Returns:
            iList[int]nt: the encrypted numeric representations of the characters
        """
        result = []
        for i in range(len(l)):
            if l[i] == -65:
                result.append(-65)
            else:
                result.append((l[i] + self.key[i % len(self.key)]) % 26)
        return result


    def print_encryption_table(
        self,
        plaintext: str,
        cell_width=5,
        output_processor=list_and_space_output_processor,
        show_steps=False,
    ) -> str:
        """Prints the encryption table for the given plaintext

        Args:
            plaintext (str): The plaintext to encrypt
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            output_processor (function, optional): the function to process the output of the encryption steps. Defaults to list_and_space_output_processor.
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
        output_processor=list_and_space_output_processor,
        show_steps=False,
    ) -> str:
        """Prints the decryption table for the given ciphertext

        Args:
            ciphertext (str): The ciphertext to encrypt
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            output_processor (function, optional): the function to process the output of the decryption steps. Defaults to list_and_space_output_processor.
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

    def _make_decryption_object(self) -> "VigenereCipher":
        """Makes a new VigenereCipher object that is the reverse of this one

        Returns:
            VigenereCipher: the reverse VigenereCipher object
        """
        n_key = "".join(character_representation([26 - i for i in self.key]))
        return VigenereCipher(n_key)


if __name__ == "__main__":

    cipher = VigenereCipher("abcde")

    ciphertext = cipher.print_encryption_table("hello world", show_steps=True)

    cipher.print_decryption_table(ciphertext, show_steps=False)