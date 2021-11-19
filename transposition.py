from typing import List, Callable, Union

from encryption import Encryption


class TranspositionCipher(Encryption):
    """A Transposition Cipher class to perform transpotion ciphers. Inherits from the Encryption class"""

    def __init__(
        self, sigma: Union[List[int], Callable[[int], int]], n: int = -1
    ) -> None:
        """Initializes the Transposition Cipher class.

        Args:
            sigma (Union[List[int], Callable[[int], int]]): The function or list map to use as the transposition function in the cipher.
            n (int, optional): The grouping number (length of the set to permute). Defaults to len(sigma).
        """
        if type(sigma) == Callable[[int], int]:
            if n == -1:
                raise Exception("If sigma is a function, n must be specified.")
            else:
                sigma = [sigma(i) for i in range(n)]

        if n == -1:
            n = len(sigma)

        if n != len(sigma):
            raise Exception("The length of sigma must equal n.")

        def pad(s: str) -> str:
            """Pads a string to the nearest multiple of n.

            Args:
                s (str): The string to pad.

            Returns:
                str: The padded string.
            """
            return s + "?" * (n - (len(s) - 1) % n - 1)

        self.sigma = sigma
        super().__init__(preprocess_raw_string=[pad], group_by=n)

    def _encrypt_group(self, group: str) -> any:
        """Encrypts a group of characters.

        Args:
            group (str): the transposed group of characters.

        Returns:
            any: [description]
        """
        s = [""] * self.group_by
        for i in range(self.group_by):
            s[self.sigma[i]] = group[i]
        return "".join(s)

    def _make_decryption_object(self) -> "TranspositionCipher":
        """Creates a decryption object using sigma as the inverse of the encryption object's sigma.

        Returns:
            TranspositionCipher: the decryption object.
        """
        return TranspositionCipher(
            [self.sigma.index(i) for i in range(self.group_by)], self.group_by
        )

    def __repr__(self) -> str:
        s = ""
        for i in range(self.group_by):
            s += f"{i}->{self.sigma[i]}; "
        return super().__repr__() + f"[{s[:-2]}]"


if __name__ == "__main__":
    plaintext = "1234567890"
    cipher = TranspositionCipher(sigma=[3, 2, 1, 0, 4])

    ciphertext = cipher.print_encryption_table(plaintext)
    cipher.print_decryption_table(ciphertext)
