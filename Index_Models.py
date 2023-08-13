from index_loggers import ref_logger

class Mishnah_Tosefta_Reference:

    def __init__(self, type: str, tractate: str, chapter: str, paragraph: str):
        self.type = type.lower()
        if self.type not in ['m','t']:
            raise Exception(f"Invalid type {self.type}. Must be 'm' or 't'")
        self.tractate = tractate
        self.chapter = chapter
        self.paragraph = paragraph

    def __str__(self) -> str:
        return f"{self.type}{self.tractate} {self.chapter}:{self.paragraph}"

    def __dict__(self) -> dict:
        return {'type':self.type,'tractate':self.tractate,'chapter':self.chapter,'paragraph':self.paragraph}

    def __eq__(self, __value: object) -> bool:
        if type(__value) is Mishnah_Tosefta_Reference:
            return self.__dict__() == __value.__dict__()
        return False

class Talmud_Reference:

    def __init__(self, type: str, tractate: str, folio: str, page_letter: str):
        self.type = type.lower()
        if self.type not in ['b','y', 'j']:
            raise Exception(f"Invalid type {self.type}. Must be 'b', 'y', or 'j'")
        self.tractate = tractate
        self.folio = folio
        self.page_letter = page_letter
        if self.page_letter not in ['a','b']:
            raise Exception(f"Invalid page letter {self.page_letter}. Must be 'a' or 'b'")
        
    def __str__(self) -> str:
        return f"{self.type}{self.tractate} {self.folio}{self.page_letter}"
    

    def __dict__(self) -> dict:
        return {'type':self.type,'tractate':self.tractate,'folio':self.folio,'page_letter':self.page_letter}
    
    def __eq__(self, __value: object) -> bool:
        if type(__value) is Talmud_Reference:
            return self.__dict__() == __value.__dict__()
        return False

class DSS_Reference:

    def __init__(self, Cave_Number: str, Manuscript_Designator: str, Column: str, Line: str, Segment_Indicator='', Use_Capital_Columns=True):
        self.Cave_Number = Cave_Number
        self.Manuscript_Designator = Manuscript_Designator
        self.Column = Column
        self.Line = Line
        self.Segment_Indicator = Segment_Indicator
        self.Use_Capital_Columns = Use_Capital_Columns

    def __str__(self):
        return f"{self.Cave_Number}Q{self.Manuscript_Designator}{self.Segment_Indicator} {self.Column}{self.Line}"
    
    def __repr__(self):
        return f"DSS_Reference({self.Cave_Number},{self.Manuscript_Designator},{self.Column},{self.Line},{self.Segment_Indicator},{self.Use_Capital_Columns})"
    
    def __dict__(self):
        return {
            "Cave_Number":self.Cave_Number,
            "Manuscript_Designator":self.Manuscript_Designator,
            "Column":self.Column,
            "Line":self.Line,
            "Segment_Indicator":self.Segment_Indicator,
            "Use_Capital_Columns":self.Use_Capital_Columns}

    def __eq__(self, __value: object) -> bool:
        if type(__value) is DSS_Reference:
            return self.__dict__() == __value.__dict__()
        return False

class Bible_Reference:

    def __init__(self, book, chapter, verse):
        self.book = str(book)
        self.chapter = str(chapter)
        self.verse = str(verse)

    def __str__(self):
        if self.chapter == 0:
            return f"{self.book} {self.verse}" # for one chapter books 
        else:
            return f"{self.book} {self.chapter}:{self.verse}"
        
    def __repr__(self):
        return "Bible_Reference({},{},{})".format(self.book,self.chapter,self.verse)
    
    def __dict__(self):
        return {'book':self.book,'chapter':self.chapter,'verse':self.verse}

    def __eq__(self, __value: object) -> bool:
        if type(__value) is Bible_Reference:
            return self.__dict__() == __value.__dict__()
        return False
    
    def __neq__(self, __value: object) -> bool:
        return not self.__eq__(__value)

class Index_Entry:

    def __init__(self, reference, page_number: str):
        self.reference = reference # must be a reference object, one of the above
        self.page_number = page_number

    def __str__(self):
        return f"{self.reference} {self.page_number}"
    
    def __repr__(self):
        return f"Index_Entry({self.reference},{self.page_number})"
    
    def __dict__(self):
        return {'reference':dict(self.reference), 'page_number':str(self.page_number)}