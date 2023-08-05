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

class AP_Parser(Reference_Parser):

    def __init__(self, configurations: dict = None):
        super().__init__(configurations)
        self.configurations = configurations

    def convert_to_obj(self, book, match_string, one_chapter_book=False):
        ref_logger.debug(f"Converting match string {match_string} to object")
        # the input string is known to be a valid reference
        chapter_verse = re.search(r"\d{1,3}\.?:?\d{0,3}-?\d{0,3}", match_string).group(0)
        numbers = re.findall(r"\d{1,3}", chapter_verse)
        if book in ("Philemon", "2 John", "3 John", "Jude"):
            # these books only have one chapter
            one_chapter_book = True
        if len(numbers) == 1:
            if one_chapter_book:
                # the book only has one chapter
                chapter = "1"
                verse = numbers[0]
            else:
                # the book has multiple chapters
                chapter = numbers[0]
                verse = "0"
        elif len(numbers) == 2:
            chapter = numbers[0]
            verse = numbers[1]
        elif len(numbers) == 3:
            chapter = numbers[0]
            verse = numbers[1] + "-" + numbers[2]
        else:
            # something went wrong
            ref_logger.error(f"Could not parse reference {match_string}")
            return None
        ref_logger.debug(f"Returning object {Index_Models.Bible_Reference(book, chapter, verse)}")
        return Index_Models.Bible_Reference(book, chapter, verse)
    
    def parse(self, reference_string: str) -> list[Index_Models.Bible_Reference]:
        """
        Parses a reference string for a New Testament reference
        """
        ref_logger.debug(f"Parsing reference string {reference_string}")
        reference = []
        for alias in self.alias_dict:
            a = list(alias.keys())[0]
            matches = re.findall(f"{a}" + r"\.?\s\d{1,3}\.?:?\d{0,3}-?\d{0,3}", reference_string)
            ref_logger.debug(f"Found {len(matches)} matches for alias {a}")
            for match in matches:
                ref_logger.debug(f"Converting match {match} to object")
                reference.append(self.convert_to_obj(alias[a], match))
        return reference

class NT_Parser(Reference_Parser):

    def __init__(self, configurations: dict = None):
        super().__init__(configurations)
        self.configurations = configurations

    def convert_to_obj(self, book, match_string, one_chapter_book=False):
        ref_logger.debug(f"Converting match string {match_string} to object")
        # the input string is known to be a valid reference
        chapter_verse = re.search(r"\d{1,3}\.?:?\d{0,3}-?\d{0,3}", match_string).group(0)
        numbers = re.findall(r"\d{1,3}", chapter_verse)
        if book in ("Philemon", "2 John", "3 John", "Jude"):
            # these books only have one chapter
            one_chapter_book = True
        if len(numbers) == 1:
            if one_chapter_book:
                # the book only has one chapter
                chapter = "1"
                verse = numbers[0]
            else:
                # the book has multiple chapters
                chapter = numbers[0]
                verse = "0"
        elif len(numbers) == 2:
            chapter = numbers[0]
            verse = numbers[1]
        elif len(numbers) == 3:
            chapter = numbers[0]
            verse = numbers[1] + "-" + numbers[2]
        else:
            # something went wrong
            ref_logger.error(f"Could not parse reference {match_string}")
            return None
        
        return Index_Models.Bible_Reference(book, chapter, verse)
    
    def parse(self, reference_string: str) -> list[Index_Models.Bible_Reference]:
        """
        Parses a reference string for a New Testament reference
        """
        ref_logger.debug(f"Parsing reference string {reference_string}")
        reference = []
        for alias in self.alias_dict:
            a = list(alias.keys())[0]
            matches = re.findall(f"{a}" + r"\.?\s\d{1,3}\.?:?\d{0,3}-?\d{0,3}", reference_string)
            ref_logger.debug(f"Found {len(matches)} matches for alias {a}")
            for match in matches:
                ref_logger.debug(f"Converting match {match} to object")
                reference.append(self.convert_to_obj(alias[a], match))
        return reference

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
                chapter = 1
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
    
class DSS_Parser(Reference_Parser):

    def __init__(self, configurations: dict = None):
        super().__init__(configurations)
        self.configurations = configurations

    def convert_to_obj(self, match_string):
        Cave_Number = re.search(r"\d{1,2}", match_string).group(0)
        Manuscript_Designator = re.search(r"Q[A-Z]?\d{0,3}[a-z]{0,5}", match_string).group(0)
        # remove the leading Q
        if Manuscript_Designator[0] == "Q":
            Manuscript_Designator = Manuscript_Designator[1:]
        
        segment_indicator = re.search(r"[a-z]", match_string).group(0)
        column_number = re.search(r"[ivxIVX]{1,10}", match_string).group(0)
        line_number = re.search(r"\d{1,3}", match_string).group(0)
        use_captial_columns = column_number.isupper()
        ref_logger.debug(f"Found Cave_Number {Cave_Number}")
        ref_logger.debug(f"Found Manuscript_Designator {Manuscript_Designator}")
        ref_logger.debug(f"Found segment indicator {segment_indicator}")
        ref_logger.debug(f"Found column number {column_number}")
        ref_logger.debug(f"Found line number {line_number}")
        return Index_Models.DSS_Reference(Cave_Number, Manuscript_Designator,  column_number, line_number, Segment_Indicator=segment_indicator, Use_Capital_Columns=True)

    def parse(self, reference_string: str) -> list[Index_Models.DSS_Reference]:
        """
        Parses a reference string for a Dead Sea Scrolls reference
        """
        ref_logger.debug(f"Parsing reference string {reference_string}")
        references = []
        matches = re.findall(r"\d{1,3}Q[A-Z]?\d{0,3}[a-z]{0,5},?\s[ivxIVX]{1,10}[.:,\s]\s?\d{1,3}", reference_string)
        ref_logger.debug(f"Found {len(matches)} matches")
        for m in matches:
            ref_logger.debug(f"Converting match {m} to object")
            reference = self.convert_to_obj(m)
            references.append(reference)
        return references
    
class Main_Parser:

    def __init__(self, parser_names=[]):
        self.parsers = []
        self.load_parsers(parser_names)

    def load_parsers(self, names=[]):
        if len(names) == 0:
            names = ["NT", "OT", "AP"]
        for name in names:
            if name == "NT":
                self.parsers.append(NT_Parser().load_alias_file('aliases/NT.json'))
            elif name == "OT":
                self.parsers.append(OT_Parser().load_alias_file('aliases/OT.json'))
            elif name == "AP":
                self.parsers.append(AP_Parser().load_alias_file('aliases/AP.json'))
            elif name == "DSS":
                self.parsers.append(DSS_Parser())
            else:
                ref_logger.critical(f"Could not load parser {name}")
                raise ValueError(f"Could not load parser {name}")
                

    def parse(self, reference_string: str) -> list:
        """
        Parses a reference string for a reference
        """
        ref_logger.debug(f"Parsing reference string {reference_string}")
        references = []
        for parser in self.parsers:
            ref_logger.debug(f"Using parser {parser}")
            references.extend(parser.parse(reference_string))
        return references