from typing import List, Callable, Union

from utils import list_and_space_output_processor, listify


class Encryption:
    """a general encryption class holding the method definitions"""

    def __init__(
        self,
        preprocess_raw_string: List[Callable[[any], str]] = [],
        preprocess: List[Callable[[List[any]], List[any]]] = [],
        postprocess: List[Callable[[List[any]], List[any]]] = [],
        group_by: int = 1,
        consolidator: Callable[[List[any]], any] = "".join,
    ) -> None:
        """Initializes the object with the given attributes

        Args:
            preprocess_raw_string (List[Callable[[any], any]], optional): the preprocess functions to be applied to the raw plaintext string before grouping. Defaults to [].
            preprocess (List[Callable[[any], any]], optional): a list of preprocessor functions. Defaults to [].
            postprocess (List[Callable[[any], any]], optional): a list of postprocessor function to run before outputs. Defaults to [].
            group_by (int, optional): The number of characters to group by before processing the plaintext string. Defaults to 1.
            consolidator (Callable[[List[any]], any], optional): the function to consolidate the grouped text. Defaults to "".join.
        """
        self.preprocess_raw_string = preprocess_raw_string
        self.preprocess = preprocess
        self.postprocess = postprocess
        self.group_by = group_by
        self.consolidator = consolidator
        self.decryption_object = None
        self.is_decryption_object = False
        self.params = {}

    def _preprocess_raw_string(self, raw_string: any) -> any:
        """Runs the preprocess functions on the raw string

        Args:
            raw_string (any): the raw string to be processed

        Returns:
            any: the processed raw string
        """
        for f in self.preprocess_raw_string:
            raw_string = f(raw_string)
        return raw_string

    def _group_by(self, text: any) -> List[str]:
        """Groups the text by the group_by attribute

        Args:
            text (any): the text to be grouped

        Returns:
            List[any]: the text grouped in groups of self.group_by
        """
        if self.group_by < 0:
            group_by = len(text)
        else:
            group_by = self.group_by
        text = str(text)
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

    def _encrypt_group(self, group: any) -> any:
        """Encrypts a single group

        Args:
            group (any): the group to be encrypted

        Raises:
            NotImplementedError: if the method is not implemented

        Returns:
            any: the encrypted group
        """
        raise NotImplementedError

    def _encrypt(self, grouped_text: List[any]) -> List[any]:
        """Encrypts the grouped text

        Args:
            grouped_text (List[any]): the grouped text to be encrypted

        Returns:
            List[any]: the encrypted grouped text
        """
        return [self._encrypt_group(group) for group in grouped_text]

    def _postprocess(self, grouped_text: List[any]) -> List[any]:
        """Runs the postprocess functions on the grouped text

        Args:
            grouped_text (List[any]): the grouped text to be processed

        Returns:
            List[any]: the processed grouped text
        """
        for f in self.postprocess:
            grouped_text = [f(group) for group in grouped_text]
        return grouped_text

    def encrypt(self, plaintext: any) -> any:
        """Encrypts the plaintext

        Args:
            plaintext (any): the plaintext to be encrypted

        Raises:
            NotImplementedError: if the method is not implemented

        Returns:
            any: the encrypted ciphertext
        """

        temp = self._preprocess_raw_string(plaintext)
        temp = self._group_by(temp)
        temp = self._preprocess(temp)
        temp = self._encrypt(temp)
        temp = self._postprocess(temp)
        temp = self.consolidator(temp)
        return temp

    def decrypt(self, ciphertext: any) -> any:
        """Decrypts the ciphertext

        Args:
            ciphertext (any): the ciphertext to be decrypted

        Returns:
            any: the decrypted plaintext
        """
        return self.make_decryption_object().encrypt(ciphertext)

    def print_encryption_table(
        self,
        plaintext: any,
        cell_width=5,
        output_processor=list_and_space_output_processor,
        show_steps=False,
    ) -> any:
        """Prints the encryption table for the given plaintext.

        Args:
            plaintext (any): the plaintext to be encrypted
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            output_processor (Callable[[any], str], optional): a function to process the output before printing. Defaults to list_and_space_output_processor.
            show_steps (bool, optional): whether to show the steps of the encryption. Defaults to False.

        Returns:
            any: the encrypted ciphertext
        """
        if output_processor is None:
            output_processor = str
        o = listify(output_processor)

        prefix = "De" if self.is_decryption_object else "En"
        print(f"{prefix}cryption Table - " + self.__repr__() + f"({plaintext}):")
        prefix = prefix.lower()

        table_lines = []

        def add_line(name: str, line: Union[List[any], any]) -> None:
            table_lines.append((name, o(line)))

        longest_func_name = max(
            [len("process_raw_string")]
            + [
                len(f.__name__)
                for f in self.preprocess_raw_string + self.preprocess + self.postprocess
            ]
        )
        name_width = longest_func_name + 2

        add_line("raw_string", plaintext)

        temp = plaintext
        for f in self.preprocess_raw_string:
            temp = f(temp)
            if show_steps:
                add_line(f.__name__, temp)

        temp = self._group_by(temp)
        groupings = len(temp)
        i_arr = list(range(groupings))

        add_line("i", i_arr)
        add_line("groupings", temp)

        for f in self.preprocess:
            temp = [f(group) for group in temp]
            if show_steps:
                add_line(f.__name__, temp)

        temp = self._encrypt(temp)
        if show_steps:
            if self.is_decryption_object:
                add_line("decrypt", temp)
            else:
                add_line("encrypt", temp)

        for f in self.postprocess:
            temp = [f(group) for group in temp]
            if show_steps:
                add_line(f.__name__, temp)

        if not show_steps:
            if self.is_decryption_object:
                add_line("decrypt", temp)
            else:
                add_line("encrypt", temp)

        temp = self.consolidator(temp)
        add_line("consolidated", temp)

        max_cell_in_line = lambda line: len(max(line[1], key=len))
        cell_width = max(
            cell_width,
            max_cell_in_line(max(table_lines, key=max_cell_in_line)) + 2,
        )

        line_length = name_width + 2 + (cell_width + 1) * groupings
        row_space = line_length - name_width - 3

        line_str = "-" * line_length

        format_array = ["{:^" + str(cell_width) + "}"] * groupings

        for name, line in table_lines:
            print(line_str)
            if isinstance(line, list):
                print(
                    f"|{name:^{name_width}}|" + "|".join(format_array).format(*line) + "|"
                )
            else:
                print(
                    f"|{name:^{name_width}}|{output_processor(line):^{row_space}}|"
                )

        print(line_str)
        print()

        return temp

    def print_decryption_table(
        self, ciphertext: any, cell_width=5, output_processor=None, show_steps=False
    ) -> any:
        """Prints the decryption table for the given ciphertext.

        Args:
            plaintext (any): the plaintext to be plaintext
            cell_width (int, optional): the width of each table cell. Defaults to 5.
            output_processor (Callable[[any], str], optional): a function to process the output before printing. Defaults to None.
            show_steps (bool, optional): whether to show the steps of the decryption. Defaults to False.

        Returns:
            any: the decrypted plaintext
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

    def __call__(self, plaintext: any) -> any:
        """Handles the call to the object and encrypts the plaintext

        Args:
            plaintext (any): the plaintext to be encrypted

        Returns:
            any: the encrypted ciphertext
        """
        return self.encrypt(plaintext)

    def __repr__(self) -> str:
        """A string representation of the object

        Returns:
            str: a string representation of the object
        """
        return self.__class__.__name__
