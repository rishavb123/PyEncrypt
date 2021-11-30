from typing import List, Tuple

from encryption import Encryption
from process_funcs import (
    convert_each_2_digits_to_char,
    convert_to_rsa_format,
    pad_numeric_representation,
    remove_spaces,
    to_lower_case,
)

# Preproccess Raw Text
preprocess_raw_string = [to_lower_case, remove_spaces, convert_to_rsa_format]
preprocess_raw_string_decrypt = []

# Preprocess Characters
preprocess_groups = [int]

# Post Process Characters
postprocess_groups = [pad_numeric_representation]
postprocess_groups_decrypt = [pad_numeric_representation, convert_each_2_digits_to_char]

class RSA(Encryption):
    """An RSA Cipher class to perform RSA encryption. Inherits from the Encryption class"""

    def __init__(self, n: int, e: int, p: int=-1, q: int=-1, calculate_p_q: bool=False) -> None:
        """Initializes the RSA Cipher class

        Args:
            n (int): the RSA modulus
            e (int): the RSA public exponent
            p (int, optional): One of the RSA primes. Defaults to -1.
            q (int, optional): The other RSA prime. Defaults to -1.
            calculate_p_q (bool, optional): Whether or not to setup p and q. Defaults to False.
        """        
        
        self.n = n
        self.e = e

        if calculate_p_q and p == -1 and q == -1:
            p, q = RSA.calculate_p_and_q(n, e)
        
        self.set_p_and_q(p, q)

        super().__init__(
            preprocess_raw_string=preprocess_raw_string,
            preprocess=preprocess_groups,
            postprocess=postprocess_groups,
            group_by=RSA.calculate_group_by(n),
        )

    def _encrypt_group(self, group: int) -> int:
        """Encrypts a group of characters represented by an integer

        Args:
            group (int): The group of characters to encrypt represented by an integer

        Returns:
            int: The encrypted group of characters represented by an integer
        """        
        return group ** self.e % self.n

    def _make_decryption_object(self) -> "RSA":
        """Creates a new RSA object that is the decryption object

        Returns:
            RSA: The decryption object
        """
        if self.p == -1 or self.q == -1:
            raise ValueError("Cannot create decryption object without p and q")
        temp = RSA(self.n, self.d)
        temp.preprocess_raw_string = preprocess_raw_string_decrypt
        temp.postprocess = postprocess_groups_decrypt
        return temp

    def set_p_and_q(self, p: int, q: int) -> None:
        """Sets the p and q values of the RSA object

        Args:
            p (int): The first RSA prime
            q (int): The second RSA prime
        """        
        self.p = p
        self.q = q

        if self.p != -1 and self.q != -1:
            if self.n != self.p * self.q:
                raise ValueError("n must equal p * q")
            self.phi = (self.p - 1) * (self.q - 1)
            self.d = RSA.calculate_d(self.e, (self.p - 1) * (self.q - 1))
            if self.e < 1 or self.e >= self.phi:
                raise ValueError("e must be between 1 and phi")

    def __repr__(self) -> str:
        """Returns a string representation of the RSA object

        Returns:
            str: The string representation of the RSA object
        """        
        if self.p != -1 and self.q != -1:
            return super().__repr__() + f"(n={self.n}, e={self.e}, p={self.p}, q={self.q}, phi={self.phi}, d={self.d})"
        return super().__repr__() + f"[n={self.n}, e={self.e}]"

    @staticmethod
    def calculate_group_by(n: int) -> int:
        """Calculates the group by value for the RSA cipher

        Args:
            n (int): the RSA modulus

        Returns:
            int: the group by value
        """              
        s = 25
        c = 0
        while int(s) < n:
            s *= 100
            s += 25
            c += 1
        return c * 2

    @staticmethod
    def calculate_d(e: int, phi: int) -> int:
        """Calculates the d value for the RSA cipher

        Args:
            e (int): the RSA public key
            phi (int): the RSA totient

        Returns:
            int: the d value
        """
        try:
            return pow(e, -1, phi) # only works for python 3.8 or higher
        except:
            return RSA.calculate_d_slow(e, phi)

    @staticmethod
    def calculate_d_slow(e: int, phi: int) -> int:
        """Calculates the d value for the RSA cipher

        Args:
            e (int): the RSA public key
            phi (int): the RSA totient

        Returns:
            int: the d value
        """
        for d in range(phi):
            if (e * d) % phi == 1:
                return d

    @staticmethod
    def calculate_p_and_q(n: int, e: int) -> Tuple[int]:
        """Calculates the p and q values for the RSA cipher

        Args:
            n (int): The RSA modulus
            e (int): The RSA public exponent

        Returns:
            Tuple[int]: The p and q values of the RSA object
        """        
        if n < 2:
            raise ValueError("n must be greater than 1")
        if e < 2:
            raise ValueError("e must be greater than 1")
        if e >= n:
            raise ValueError("e must be less than n")

        for p in range(2, n):
            if (n % p) == 0:
                q = n // p
                if RSA.calculate_d(e, (p - 1) * (q - 1)) != -1:
                    return p, q

        return -1, -1

    @staticmethod
    def make_RSA_object(p: int, q: int, e: int = 65537) -> "RSA":
        """Creates a new RSA object with a public key

        Args:
            p (int): the RSA p value
            q (int): the RSA q value
            e (int): the RSA public key

        Returns:
            RSA: The RSA object
        """
        n = p * q
        return RSA(n, e, p, q)

if __name__ == "__main__":
    rsa = RSA.make_RSA_object(43, 59, e=13)

    plaintext = "hello world"
    ciphertext = rsa.print_encryption_table(plaintext, show_steps=True)

    rsa.print_decryption_table(ciphertext, show_steps=True)