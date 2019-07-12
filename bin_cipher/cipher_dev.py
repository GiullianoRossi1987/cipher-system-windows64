# coding = utf-8
# using namespace std
import os
import json
from typing import AnyStr
from string import ascii_letters, punctuation, whitespace


"""
This script have important methods and objects to system dev options works!

:var local_ascii : The local Ascii letters!

:type local_ascii : list
"""

local_ascii = [x for x in ascii_letters]
local_ascii += [x for x in punctuation]
local_ascii.append(whitespace)


class CipherCreator(object):
    """

    """
    # class vars
    file_name = AnyStr
    inner_doc = dict()
    cipher_name = AnyStr
    got_data = False
    __creator_version__ = "alpha"

    # exceptions and errors
    class EmptyDataError(BaseException):
        args: object = "The system can't do this action without the main data!"

    class CipherExistsError(BaseException):
        args: object = "This cipher already exists!"

    # methods
    @staticmethod
    def check_cipher_exists(cipher: str) -> bool:
        """
        Checks if the cipher exists!
        :param cipher: The cipher to localize.
        :return: If the cipher exists in the library of ciphers.
        """
        if ".json" not in cipher:
            cipher += ".json"
        return cipher in os.listdir("ciphers")

    def __init__(self, cipher_name: str, author: str):
        """
        Starts the creator!
        :param cipher_name: The cipher name to create.
        """
        if self.check_cipher_exists(cipher_name):
            raise self.CipherExistsError()
        self.file_name = cipher_name + ".json"
        self.cipher_name = cipher_name
        self.got_data = True
        self.inner_doc["Author"] = author
        self.inner_doc["Encoding"] = {}
        self.inner_doc["Decoding"] = {}
        self.inner_doc["Verified"] = self.__creator_version__

    @classmethod
    def check_got_data(cls):
        """
        Checks if the system have started successfully.
        :raise cls.EmptyDataError : if the system don't started successfully.
        """
        if not cls.got_data:
            raise cls.EmptyDataError()

    def get_values_doc(self):
        """
        Get the values to the inner document in the cipher.
        """
        decoding = {}
        for char in local_ascii:
            con = True
            while True:
                vl = str(input(f"Type the value to the character '{char}': "))
                r = int(input("Confirm the value?\n[1]Y\n[2]N\n[3]Cancel\n>>> "))
                if r == 3:
                    con = False
                    break
                if r == 1:
                    break
            if con:
                self.inner_doc["Encoding"][char] = vl
                continue
            else:
                raise KeyboardInterrupt()
        for l, s in self.inner_doc["Encoding"]:
            decoding[s] = l
        self.inner_doc["Decoding"] = decoding
        del decoding

    def create_file(self):
        """
        Creates and updates the cipher file.
        """
        os.chdir("ciphers")
        with open(self.file_name, "w") as file:
            local_doc = json.dumps(self.inner_doc)
            file.write(local_doc)


class CipherManager(object):
    """

    """
    cipher_to = AnyStr
    inner_cipher = dict
    got_data = False

    class EmptyDataError(BaseException):
        args: object = "The system can't do this action without the main data!"

    class CipherNotFound(BaseException):
        args: object = "The cipher don't exists in the library!"

    class InvalidFileType(BaseException):
        args: object = "The system can't open this file type, only '.json' files!"

    class CorruptedDocument(BaseException):
        args: object = "This cipher file have corrupted data in it!"

    @classmethod
    def check_cipher_exists(cls, cipher: str) -> bool:
        """
        Checks if the cipher file exists!
        :param cipher: The cipher to verify if the
        :return: If the cipher file exists in the library!
        """
        if "." in cipher and ".json" not in cipher:
            raise cls.InvalidFileType()
        elif ".json" not in cipher and "." not in cipher:
            cipher += ".json"
        return cipher in os.listdir("ciphers")

    @classmethod
    def check_docs_corrupted(cls, doc: dict) -> bool:
        """
        Checks if the document's not corrupted!
        :param doc: The document to analyze!
        :return: If the document's ok
        """
        try:
            encoding_label: dict = doc["Encoding"]
            decoding_label: dict = doc["Decoding"]
            verified_label = doc["Verified"]
            author_label = doc["Author"]
            if encoding_label is not dict or decoding_label is not dict:
                return True
            if verified_label is not str or author_label is not str:
                return True
            if local_ascii not in encoding_label.keys():
                return True
            if local_ascii not in decoding_label.values():
                return True
        except IndexError:
            return True
        else:
            return False

    def __init__(self, cipher_file: str):
        """
        Starts the system!
        :param cipher_file: The cipher to manage
        """
        nm = cipher_file
        if not self.check_cipher_exists(nm):
            raise self.CipherNotFound()
        del nm
        self.cipher_to = cipher_file
        with open("ciphers/"+cipher_file, "r") as cipher:
            local_doc = json.loads(cipher.read())
            if self.check_docs_corrupted(local_doc):
                raise self.CorruptedDocument()
            else:
                self.inner_cipher = local_doc
        self.got_data = True

    def change_values_(self, letters: str = "*"):
        """
        Alter the values to the cipher
        :param letters: The letters to alter, default *, if '*' the alter all the letters!
        :type letters: str
        """
        if letters == "*":
            # alter the values to
            for char in local_ascii:
                c = True
                while True:
                    new_vl = str(input(f"Type the new value to the char '{char}': "))
                    confirm = int(input("Confirm the value?\n[1]Y\n[2]N\n[3]Cancel\n>>>"))
                    if confirm == 3:
                        c = False
                        break
                    if confirm == 1:
                        break
                if c:
                    old_vl = self.inner_cipher["Encoding"][char]
                    self.inner_cipher["Encoding"][char] = new_vl
                    self.inner_cipher["Decoding"][old_vl] = char
                    continue
                else:
                    raise KeyboardInterrupt()

























