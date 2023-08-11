from Index_Models import Bible_Reference
from abc import ABC, abstractmethod

class Base_Reference_Formatter():

    def __init__(self, format_config):
        self.format_config = format_config
        self.parse_format_config()

    def parse_format_config(self):
        assert isinstance(self.format_config, dict), "format_config must be a dictionary"


    def format(self, reference):
        raise NotImplementedError("format() not implemented")
    
class Bible_Reference_Formatter(Base_Reference_Formatter):

    def format(self, reference):
        assert isinstance(reference, Bible_Reference), "reference must be a Bible_Reference object"
        book = reference.book
        chapter = reference.chapter
        verse = reference.verse
        output = ""
        if self.format_config["book"]:
            output += book
        if self.format_config["book"] and self.format_config["chapter"]:
            output += self.format_config["book-chapter-sep"]
        if self.format_config["chapter"]:
            output += f"{chapter}"
        if self.format_config["chapter"] and self.format_config["verse"]:
            output += self.format_config["chapter-verse-sep"]
        if self.format_config["verse"]:
            output += f"{verse}"
        return output
    
    def parse_format_config(self):
        if self.format_config is None:
            self.format_config = {
                "book": True,
                "chapter": True,
                "verse": True,
                "chapter-verse-sep": ":",
                "book-chapter-sep": " "
            }
        else:
            if "book" not in self.format_config:
                self.format_config["book"] = True
            if "chapter" not in self.format_config:
                self.format_config["chapter"] = True
            if "verse" not in self.format_config:
                self.format_config["verse"] = True
            if "chapter-verse-sep" not in self.format_config:
                self.format_config["chapter-verse-sep"] = ":"
            if "book-chapter-sep" not in self.format_config:
                self.format_config["book-chapter-sep"] = " "

class Base_Index_Formatter(ABC):

    def __init__(self, format_config):
        self.format_config = format_config
        self.parse_format_config()

    def parse_format_config(self):
        raise NotImplementedError("parse_format_config() not implemented")
    
    def format(self, reference_page_pair: tuple):
        raise NotImplementedError("format() not implemented")