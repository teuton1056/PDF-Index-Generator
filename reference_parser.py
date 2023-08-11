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

    def __init__(self, configurations: dict = {}):
        super().__init__(configurations)
        self.configurations = configurations

    def convert_to_obj(self, match_string):
        # compile re's
        Cave_Number_Regex = re.compile(r"\d{1,2}")
        Manuscript_Designator_Regex = re.compile(r"Q[A-Z]?\d{0,3}[a-z]{0,5}")
        Alpha_Manuscript_Designator_Regex = re.compile(r"Q[A-Za-z]{0,5}")
        Digit_Manuscript_Designator_Regex = re.compile(r"Q\d{0,3}")
        segment_indicator_regex = re.compile(r"[a-z]")
        column_number_regex = re.compile(r"[ivxIVX]{1,10}")
        line_number_regex = re.compile(r"\d{1,3}")

        ## find the cave number
        Cave_Number = Cave_Number_Regex.search(match_string).group(0)
        # remove the cave number from the match string
        match_string = match_string[len(Cave_Number):]
        
        Manuscript_Designator = None
        # is the user has supplies a list of valid manuscript names, use it to find the manuscript designator
        if 'valid_manuscript_names' in self.configurations and type(self.configurations['valid_manuscript_names']) is list:
            for name in self.configurations['valid_manuscript_names']:
                if name == match_string[:len(name)] or f"Q{name}" == match_string[:len(f"Q{name}")]:
                    Manuscript_Designator = name
                    if match_string[0] == 'Q':
                        match_string = match_string[len(f"Q{name}"):]
                    else:
                        match_string = match_string[len(name):]
                    break
            if Manuscript_Designator is None:
                ref_logger.debug(f"Could not find manuscript designator in {match_string}, trying to find a numeric manuscript designator")
                # the user provided a list of valid manuscript names, but the manuscript designator is not in the list
                # so we have to assume that the manuscript designator is a number
                Manuscript_Designator = Digit_Manuscript_Designator_Regex.search(match_string).group(0)
                match_string = match_string[len(Manuscript_Designator):]
            # now we can look for a segment indicator
            if match_string[0].isalpha() and match_string[0].islower():
                segment_indicator = segment_indicator_regex.search(match_string).group(0)
                match_string = match_string[len(segment_indicator):]
                if Manuscript_Designator[0] == "Q":
                    Manuscript_Designator = Manuscript_Designator[1:]
        else:
        # the user did not provide a list of valid identifiers: so we have to assume that there will be no segment indicator or the manuscript designator will be a number
            ## find the manuscript designator
            if match_string[0].isalpha():
                Manuscript_Designator = Alpha_Manuscript_Designator_Regex.search(match_string).group(0)
                match_string = match_string[len(Manuscript_Designator):]
                segment_indicator = None
            else:
                Manuscript_Designator = Digit_Manuscript_Designator_Regex.search(match_string).group(0)
                match_string = match_string[len(Manuscript_Designator):]
                # if the manuscript designator is a number, the letters following it are the segment indicator
                segment_indicator = segment_indicator_regex.search(match_string).group(0)
                match_string = match_string[len(segment_indicator):]

            # remove the leading Q from manuscript designator if it exists
            if Manuscript_Designator[0] == "Q":
                Manuscript_Designator = Manuscript_Designator[1:]

        # find the column number
        column_number = column_number_regex.search(match_string).group(0)
        match_string = match_string[len(column_number):]

        # find the line number
        line_number = line_number_regex.search(match_string).group(0)
        match_string = match_string[len(line_number):]

        use_captial_columns = column_number.isupper()
        ref_logger.debug(f"Found Cave_Number {Cave_Number}")
        ref_logger.debug(f"Found Manuscript_Designator {Manuscript_Designator}")
        ref_logger.debug(f"Found segment indicator {segment_indicator}")
        ref_logger.debug(f"Found column number {column_number}")
        ref_logger.debug(f"Found line number {line_number}")
        return Index_Models.DSS_Reference(Cave_Number, Manuscript_Designator,  column_number, line_number, Segment_Indicator=segment_indicator, Use_Capital_Columns=use_captial_columns)

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
                parser = NT_Parser()
                parser.load_alias_file('aliases/NT.json')
                self.parsers.append(parser)
            elif name == "OT":
                parser = OT_Parser()
                parser.load_alias_file('aliases/OT.json')
                self.parsers.append(parser)
            elif name == "AP":
                parser = AP_Parser()
                parser.load_alias_file('aliases/AP.json')
                self.parsers.append(parser)
            elif name == "DSS":
                with open("aliases/DSS.json") as f:
                    self.parsers.append(DSS_Parser(json.load(f)))
            else:
                ref_logger.critical(f"Could not load parser {name}")
                raise ValueError(f"Could not load parser {name}")
                

    def parse_over_page_break(self, page_a_string: str, page_b_string: str) -> list:
        """
        Parses a group of text which crosses a page break, returns references found only in the union of the two page, 
        excluding references found in either page alone. This handles cases where a reference is split between two pages.
        """
        union = self.parse(page_a_string + page_b_string)
        ref_logger.debug(f"Found {len(union)} references in the union of the two pages")
        page_a = self.parse(page_a_string)
        ref_logger.debug(f"Found {len(page_a)} references in page a")
        page_b = self.parse(page_b_string)
        ref_logger.debug(f"Found {len(page_b)} references in page b")
        for x in page_a:
            union.remove(x)
        for x in page_b:
            union.remove(x)
        return union


    def parse(self, reference_string: str) -> list:
        """
        Parses a reference string for a reference
        """
        if len(self.parsers) == 0:
            ref_logger.critical(f"No parsers loaded")
            raise ValueError(f"No parsers loaded")
        ref_logger.debug(f"Parsing reference string {reference_string}")
        references = []
        for parser in self.parsers:
            ref_logger.debug(f"Using parser {parser}")
            references.extend(parser.parse(reference_string))
        return references
    
    def parse_lines(self, lines: list) -> list:
        """
        Parses a list of lines for references
        """
        references = []
        for i, line in enumerate(lines):
            if type(line) is str:
                references.extend(self.parse(line))
                if i > 0:
                    references.extend(self.parse_over_page_break(lines[i-1], line))
            elif type(line) is dict:
                text = line['Raw_Text']
                references.extend(self.parse(text))
                if i > 0:
                    references.extend(self.parse_over_page_break(lines[i-1]['Raw_Text'], line))
            
        return references