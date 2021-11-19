from typing import List, Callable


class Encryption:
    """a general encryption class holding the method definitions"""

    def __init__(
        self,
        preprocess_raw_string: List[Callable[[str], str]] = [],
        preprocess: List[Callable[[List[any]], List[any]]] = [],
        postprocess: List[Callable[[List[str]], List[str]]] = [],
        group_by=1,
    ) -> None:
        """Initializes the object with the given attributes

        Args:
            preprocess_raw_string (List[Callable[[str], str]], optional): the preprocess functions to be applied to the raw plaintext string before grouping. Defaults to [].
            preprocess (List[Callable[[any], any]], optional): a list of preprocessor functions. Defaults to [].
            postprocess (List[Callable[[any], any]], optional): a list of postprocessor function to run before outputs. Defaults to [].
            group_by (int, optional): The number of characters to group by before processing the plaintext string. Defaults to 1.
        """
        self.preprocess_raw_string = preprocess_raw_string
        self.preprocess = preprocess
        self.postprocess = postprocess
        self.group_by = group_by
        self.decryption_object = None
        self.is_decryption_object = False
        self.params = {}

    def _preprocess_raw_string(self, raw_string: str) -> str:
        """Runs the preprocess functions on the raw string

        Args:
            raw_string (str): the raw string to be processed

        Returns:
            str: the processed raw string
        """
        for f in self.preprocess_raw_string:
            raw_string = f(raw_string)
        return raw_string

    def _group_by(self, text: str) -> List[str]:
        """Groups the text by the group_by attribute

        Args:
            text (str): the text to be grouped

        Returns:
            List[str]: the text grouped in groups of self.group_by
        """
        if self.group_by < 0:
            group_by = len(text)
        else:
            group_by = self.group_by
        return [text[i : i + group_by] for i in range(0, len(text), group_by)]

    def _preprocess(self, grouped_text: List[str]) -> List[any]:
        """Runs the preprocess functions on the grouped text

        Args:
            grouped_text (List[str]): the grouped text to be processed

        Returns:
            List[any]: the processed grouped text
        """
        for f in self.preprocess:
            grouped_text = [f(group) for group in grouped_text]
        return grouped_text

    def _encrypt_group(self, group: str) -> any:
        """Encrypts a single group

        Args:
            group (str): the group to be encrypted

        Raises:
            NotImplementedError: if the method is not implemented

        Returns:
            any: the encrypted group
        """
        raise NotImplementedError

    def _encrypt(self, grouped_text: List[str]) -> List[any]:
        """Encrypts the grouped text

        Args:
            grouped_text (List[str]): the grouped text to be encrypted

        Returns:
            List[any]: the encrypted grouped text
        """
        return [self._encrypt_group(group) for group in grouped_text]

    def _postprocess(self, grouped_text: List[any]) -> List[str]:
        """Runs the postprocess functions on the grouped text

        Args:
            grouped_text (List[any]): the grouped text to be processed

        Returns:
            List[str]: the processed grouped text
        """
        for f in self.postprocess:
            grouped_text = [f(group) for group in grouped_text]
        return grouped_text

    def encrypt(self, plaintext: str) -> str:
        """Encrypts the plaintext

        Args:
            plaintext (str): the plaintext to be encrypted

        Raises:
            NotImplementedError: if the method is not implemented

        Returns:
            str: the encrypted ciphertext
        """

        temp = self._preprocess_raw_string(plaintext)
        temp = self._group_by(temp)
        temp = self._preprocess(temp)
        temp = self._encrypt(temp)
        temp = self._postprocess(temp)
        return "".join(temp)

    def decrypt(self, ciphertext: str) -> str:
        """Decrypts the ciphertext

        Args:
            ciphertext (str): the ciphertext to be decrypted

        Returns:
            str: the decrypted plaintext
        """
        return self.make_decryption_object().encrypt(ciphertext)

    def print_encryption_table(
        self, plaintext: str, cell_width=5, output_processor=None, show_steps=False
    ) -> str:
        """Prints the encryption table for the given plaintext.

        Args:
            plaintext (str): the plaintext to be encrypted
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            output_processor (Callable[[any], str], optional): a function to process the output before printing. Defaults to None.
            show_steps (bool, optional): whether to show the steps of the encryption. Defaults to False.

        Returns:
            str: the encrypted ciphertext
        """
        if output_processor is None:
            output_processor = lambda x: str(x)
        o = lambda text_arr: [output_processor(text) for text in text_arr]

        temp = self._preprocess_raw_string(plaintext)

        prefix = "De" if self.is_decryption_object else "En"
        print(f"{prefix}cryption Table - " + self.__repr__() + f"({temp}):")

        temp = self._group_by(temp)
        groupings = len(temp)

        longest_func_name = max(
            [len("groupings")]
            + [len(f.__name__) for f in self.preprocess + self.postprocess]
        )

        name_width = longest_func_name + 2
        line_length = name_width + 2 + (cell_width + 1) * groupings
        line_str = "-" * line_length

        format_array = ["{:^" + str(cell_width) + "}"] * groupings

        i_arr = list(range(groupings))

        print(line_str)
        print(f"|{'i':^{name_width}}|" + "|".join(format_array).format(*o(i_arr)) + "|")

        print(line_str)
        print(
            f"|{'groupings':^{name_width}}|"
            + "|".join(format_array).format(*o(temp))
            + "|"
        )

        for f in self.preprocess:
            temp = [f(group) for group in temp]
            if show_steps:
                print(line_str)
                print(
                    f"|{f.__name__:^{name_width}}|"
                    + "|".join(format_array).format(*o(temp))
                    + "|"
                )

        temp = self._encrypt(temp)
        if show_steps:
            print(line_str)
            print(
                f"|{'encrypt':^{name_width}}|"
                + "|".join(format_array).format(*o(temp))
                + "|"
            )

        for f in self.postprocess:
            temp = [f(group) for group in temp]
            if show_steps:
                print(line_str)
                print(
                    f"|{f.__name__:^{name_width}}|"
                    + "|".join(format_array).format(*o(temp))
                    + "|"
                )

        if not show_steps:
            print(line_str)
            print(
                f"|{'encrypt':^{name_width}}|"
                + "|".join(format_array).format(*o(temp))
                + "|"
            )
        print(line_str)
        print()

        return "".join(temp)

    def print_decryption_table(
        self, ciphertext: str, cell_width=5, output_processor=None, show_steps=False
    ) -> str:
        """Prints the decryption table for the given ciphertext.

        Args:
            plaintext (str): the plaintext to be plaintext
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            output_processor (Callable[[any], str], optional): a function to process the output before printing. Defaults to None.
            show_steps (bool, optional): whether to show the steps of the decryption. Defaults to False.

        Returns:
            str: the decrypted plaintext
        """
        return self.make_decryption_object().print_encryption_table(
            ciphertext, cell_width, output_processor, show_steps
        )

    def _make_decryption_object(self) -> "Encryption":
        """Creates a decryption object

        Returns:
            Encryption: the decryption object
        """
        raise NotImplementedError

    def make_decryption_object(self) -> "Encryption":
        """Creates a decryption object from the current object

        Returns:
            Encryption: the decryption object
        """
        if self.decryption_object is None:
            self.decryption_object = self._make_decryption_object()
            self.decryption_object.is_decryption_object = True
        return self.decryption_object

    def __call__(self, plaintext: str) -> str:
        """Handles the call to the object and encrypts the plaintext

        Args:
            plaintext (str): the plaintext to be encrypted

        Returns:
            str: the encrypted ciphertext
        """
        return self.encrypt(plaintext)

    def __repr__(self) -> str:
        """A string representation of the object

        Returns:
            str: a string representation of the object
        """
        return self.__class__.__name__
