from index_loggers import ref_logger


class Mishnah_Tosefta_Reference:
    def __init__(self, type: str, tractate: str, chapter: str, paragraph: str):
        self.type = type.lower()
        if self.type not in ["m", "t"]:
            raise Exception(f"Invalid type {self.type}. Must be 'm' or 't'")
        self.tractate = tractate
        self.chapter = chapter
        self.paragraph = paragraph

    def __str__(self) -> str:
        return f"{self.type}{self.tractate} {self.chapter}:{self.paragraph}"

    def __dict__(self) -> dict:
        return {
            "type": self.type,
            "tractate": self.tractate,
            "chapter": self.chapter,
            "paragraph": self.paragraph,
        }

    def __eq__(self, __value: object) -> bool:
        if type(__value) is Mishnah_Tosefta_Reference:
            return self.__dict__() == __value.__dict__()
        return False

    def __neq__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self):
        return hash((self.type, self.tractate, self.chapter, self.paragraph))

    def __setitem__(self, key, value):
        if key == "type":
            self.type = value
        elif key == "tractate":
            self.tractate = value
        elif key == "chapter":
            self.chapter = value
        elif key == "paragraph":
            self.paragraph = value
        else:
            raise KeyError(f"Invalid key {key}")

    def __getitem__(self, key):
        if key == "type":
            return self.type
        elif key == "tractate":
            return self.tractate
        elif key == "chapter":
            return self.chapter
        elif key == "paragraph":
            return self.paragraph
        else:
            raise KeyError(f"Invalid key {key}")

    def __iter__(self):
        return iter(self.__dict__())

    def __contains__(self, item):
        return item in self.__dict__()

    def __len__(self):
        return len(self.__dict__())

    def keys(self):
        return self.__dict__().keys()


class Talmud_Reference:
    def __init__(self, type: str, tractate: str, folio: str, page_letter: str):
        self.type = type.lower()
        if self.type not in ["b", "y", "j"]:
            raise Exception(f"Invalid type {self.type}. Must be 'b', 'y', or 'j'")
        self.tractate = tractate
        self.folio = folio
        self.page_letter = page_letter
        if self.page_letter not in ["a", "b"]:
            raise Exception(
                f"Invalid page letter {self.page_letter}. Must be 'a' or 'b'"
            )

    def __str__(self) -> str:
        return f"{self.type}{self.tractate} {self.folio}{self.page_letter}"

    def __dict__(self) -> dict:
        return {
            "type": self.type,
            "tractate": self.tractate,
            "folio": self.folio,
            "page_letter": self.page_letter,
        }

    def __eq__(self, __value: object) -> bool:
        if type(__value) is Talmud_Reference:
            return self.__dict__() == __value.__dict__()
        return False

    def __neq__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self):
        return hash((self.type, self.tractate, self.folio, self.page_letter))

    def __setitem__(self, key, value):
        if key == "type":
            self.type = value
        elif key == "tractate":
            self.tractate = value
        elif key == "folio":
            self.folio = value
        elif key == "page_letter":
            self.page_letter = value
        else:
            raise KeyError(f"Invalid key {key}")

    def __getitem__(self, key):
        if key == "type":
            return self.type
        elif key == "tractate":
            return self.tractate
        elif key == "folio":
            return self.folio
        elif key == "page_letter":
            return self.page_letter
        else:
            raise KeyError(f"Invalid key {key}")

    def __iter__(self):
        return iter(self.__dict__())

    def __contains__(self, item):
        return item in self.__dict__()

    def __len__(self):
        return len(self.__dict__())

    def keys(self):
        return self.__dict__().keys()


class DSS_Reference:
    def __init__(
        self,
        Cave_Number: str,
        Manuscript_Designator: str,
        Column: str,
        Line: str,
        Segment_Indicator="",
        Use_Capital_Columns=True,
    ):
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
            "Cave_Number": self.Cave_Number,
            "Manuscript_Designator": self.Manuscript_Designator,
            "Column": self.Column,
            "Line": self.Line,
            "Segment_Indicator": self.Segment_Indicator,
            "Use_Capital_Columns": self.Use_Capital_Columns,
        }

    def __eq__(self, __value: object) -> bool:
        if type(__value) is DSS_Reference:
            return self.__dict__() == __value.__dict__()
        return False

    def __neq__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self):
        return hash(
            (
                self.Cave_Number,
                self.Manuscript_Designator,
                self.Column,
                self.Line,
                self.Segment_Indicator,
                self.Use_Capital_Columns,
            )
        )

    def __setitem__(self, key, value):
        if key == "Cave_Number":
            self.Cave_Number = value
        elif key == "Manuscript_Designator":
            self.Manuscript_Designator = value
        elif key == "Column":
            self.Column = value
        elif key == "Line":
            self.Line = value
        elif key == "Segment_Indicator":
            self.Segment_Indicator = value
        elif key == "Use_Capital_Columns":
            self.Use_Capital_Columns = value == "True" or value == True
        else:
            raise KeyError(f"Invalid key {key}")

    def __getitem__(self, key):
        if key == "Cave_Number":
            return self.Cave_Number
        elif key == "Manuscript_Designator":
            return self.Manuscript_Designator
        elif key == "Column":
            return self.Column
        elif key == "Line":
            return self.Line
        elif key == "Segment_Indicator":
            return self.Segment_Indicator
        elif key == "Use_Capital_Columns":
            return self.Use_Capital_Columns
        else:
            raise KeyError(f"Invalid key {key}")

    def __iter__(self):
        return iter(self.__dict__())

    def __contains__(self, item):
        return item in self.__dict__()

    def __len__(self):
        return len(self.__dict__())

    def keys(self):
        return self.__dict__().keys()


class Bible_Reference:
    def __init__(self, book, chapter, verse):
        self.book = str(book)
        self.chapter = str(chapter)
        self.verse = str(verse)

    def __str__(self):
        if self.chapter == 0:
            return f"{self.book} {self.verse}"  # for one chapter books
        else:
            return f"{self.book} {self.chapter}:{self.verse}"

    def __hash__(self):
        return hash((self.book, self.chapter, self.verse))

    def __setitem__(self, key, value):
        if key == "book":
            self.book = value
        elif key == "chapter":
            self.chapter = value
        elif key == "verse":
            self.verse = value
        else:
            raise KeyError(f"Invalid key {key}")

    def __getitem__(self, key):
        if key == "book":
            return self.book
        elif key == "chapter":
            return self.chapter
        elif key == "verse":
            return self.verse
        else:
            raise KeyError(f"Invalid key {key}")

    def __repr__(self):
        return "Bible_Reference({},{},{})".format(self.book, self.chapter, self.verse)

    def __dict__(self):
        return {"book": self.book, "chapter": self.chapter, "verse": self.verse}

    def __eq__(self, __value: object) -> bool:
        if type(__value) is Bible_Reference:
            return self.__dict__() == __value.__dict__()
        return False

    def __neq__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __iter__(self):
        return iter(self.__dict__())

    def __contains__(self, item):
        return item in self.__dict__()

    def __len__(self):
        return len(self.__dict__())

    def keys(self):
        return self.__dict__().keys()
