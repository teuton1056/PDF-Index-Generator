import json 
from index_loggers import ref_logger
import re 
import Index_Models

class Reference_Parser:

    """
    The base class for the reference parsers which would parse various types of references
    """

    def __init__(self, configurations: dict = None):
        self.configurations = configurations

    def parse(self, reference_string: str):
        """
        The base method for parsing a reference string
        """
        raise NotImplementedError("The parse method must be implemented by a subclass")
    
    def load_alias_file(self, fname):
        try:
            with open(fname) as f:
                self.alias_dict = json.load(f)
        except FileNotFoundError:
            ref_logger.error(f"Could not find alias file {fname}")
            self.alias_dict = {}


class OT_Parser(Reference_Parser):

    def __init__(self, configurations: dict = None):
        super().__init__(configurations)
        self.configurations = configurations

    def convert_to_obj(self, book, match_string, one_chapter_book=False):
        ref_logger.debug(f"Converting match string {match_string} to object")
        # the input string is known to be a valid reference
        # split the string into book, chapter, and verse
        if book == "Obadiah":
            # the book of Obadiah only has one chapter
            one_chapter_book = True
        chapter_verse = re.search(r"\d{1,3}\.?:?\d{0,3}-?\d{0,3}", match_string).group(0)
        numbers = re.findall(r"\d{1,3}", chapter_verse)
        if len(numbers) == 1:
            # only a chapter number was found
            if one_chapter_book:
                # the book only has one chapter
                chapter = 0
                verse = numbers[0]
            else:
                chapter = numbers[0]
                verse = 0
        elif len(numbers) == 2:
            # a chapter and verse number were found
            chapter = numbers[0]
            verse = numbers[1] 
        elif len(numbers) == 3:
            # a chapter and verse range were found
            chapter = numbers[0]
            verse = f"{numbers[1]}-{numbers[2]}"
        else:
            # something went wrong
            ref_logger.error(f"Could not parse chapter and verse from {match_string}")
        ref_logger.debug(f"Found chapter and verse {chapter_verse}")
        # strip off any trailing punctuation
        verse = verse.rstrip(".,:!?")
        chapter = chapter.rstrip(".,:")
        book = book
        # create the object
        return Index_Models.Bible_Reference(book, chapter, verse)

    def parse(self, reference_string: str) -> list[Index_Models.Bible_Reference]:
        """
        Parses a reference string for an Old Testament reference
        """
        ref_logger.debug(f"Parsing reference string {reference_string}")
        references = []
        for alias in self.alias_dict:
            a = list(alias.keys())[0]
            matches = re.findall(f"{a}" + r"\.?\s\d{1,3}\.?:?\d{0,3}-?\d{0,3}", reference_string)
            ref_logger.debug(f"Found {len(matches)} matches for alias {a}")
            for m in matches:
                book_name = alias[a]
                ref_logger.debug(f"Converting match {m} to object")
                obj = self.convert_to_obj(book_name, m)
                references.append(obj)
        return references