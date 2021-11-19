from typing import List, Callable, Tuple, Union

from encryption import Encryption
from utils import list_and_space_output_processor, listify


class CompoundCipher(Encryption):
    """A cipher class to run multiple ciphers together"""

    def __init__(
        self,
        ciphers: List[Encryption] = [],
        preprocess_raw_string: List[Callable[[any], any]] = [],
    ):
        """Instantiates a CompoundCipher object

        Args:
            ciphers (List[Encryption], optional): A list of ciphers to run. Defaults to [].
            preprocess_raw_string (List[Callable[[any], any]], optional): Any preprocessing to do on the raw string. Defaults to [].
        """
        super().__init__(preprocess_raw_string=preprocess_raw_string, group_by=-1)
        self.ciphers = ciphers

    def _encrypt_group(self, group: any) -> any:
        """Encrypts a the plain text inputed

        Args:
            group (any): The plain text to encrypt

        Returns:
            any: The encrypted text using the ciphers specified
        """
        for cipher in self.ciphers:
            group = cipher.encrypt(group)
        return group

    def make_encryption_table(
        self,
        plaintext: any,
        output_processor=list_and_space_output_processor,
        show_steps=False,
    ) -> Tuple[List[Tuple[str, List[str]]], any, int]:
        """Generates the encryption table from all the inner cipher tables to print

        Args:
            plaintext (any): the plaintext to be encrypted
            output_processor ([type], optional): The output processor run before display. Defaults to list_and_space_output_processor.
            show_steps (bool, optional): whether or not to show the steps. Defaults to False.

        Returns:
            Tuple[List[Tuple[str, List[str]]], any, int]: The encryption table and the resulting ciphertext and the number of groupings
        """

        table_lines, temp, groupings = [], plaintext, 0

        if output_processor is None:
            output_processor = str
        o = listify(output_processor)

        table_lines = []

        def add_line(name: str, line: Union[List[any], any]) -> None:
            table_lines.append((name, o(line)))

        add_line("raw_string", plaintext)

        temp = plaintext
        for f in self.preprocess_raw_string:
            temp = f(temp)
            if show_steps:
                add_line(f.__name__, temp)

        for i, cipher in enumerate(self.ciphers):
            lines, temp, g = cipher.make_encryption_table(
                temp, output_processor, show_steps
            )
            table_lines += [(f"E{i}::" + line[0], line[1]) for line in lines]
            groupings = max(groupings, g)

        return table_lines, temp, groupings

    def _make_decryption_object(self) -> "CompoundCipher":
        """Creates a new CompoundCipher object to decrypt the encrypted text

        Returns:
            CompoundCipher: A new CompoundCipher object to decrypt the encrypted text
        """
        decryption_ciphers = []
        for cipher in self.ciphers:
            decryption_ciphers.append(cipher.make_decryption_object())
        decryption_ciphers.reverse()
        return CompoundCipher(decryption_ciphers)

    def __repr__(self) -> str:
        """A string representation of the CompoundCipher object

        Returns:
            str: A string representation of the CompoundCipher object
        """
        return f"CompoundCipher({'==>'.join([c.__repr__() for c in self.ciphers])})"
