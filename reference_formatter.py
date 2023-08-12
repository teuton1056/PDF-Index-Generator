from Index_Models import Bible_Reference, DSS_Reference, Mishnah_Tosefta_Reference, Talmud_Reference

class Base_Reference_Formatter:

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

class DSS_Reference_Formatter(Base_Reference_Formatter):

    def parse_format_config(self):
        if self.format_config == {}: # default config
            self.format_config = {
                "cave_number": True,
                "manuscript_designator": True,
                "segment_indicator": True,
                "column": True,
                "line": True,
                "location_id": "Q",
                "ms_segment_sep": "",
                "seg_column_sep": " ",
                "ms_column_sep": " ",
                "col_line_sep": ", ",
            }
        else:
            if "cave_number" not in self.format_config:
                self.format_config["cave_number"] = True
            if "manuscript_designator" not in self.format_config:
                self.format_config["manuscript_designator"] = True
            if "segment_indicator" not in self.format_config:
                self.format_config["segment_indicator"] = True
            if "column" not in self.format_config:
                self.format_config["column"] = True
            if "line" not in self.format_config:
                self.format_config["line"] = True
            if "location_id" not in self.format_config:
                self.format_config["location_id"] = "Q"
            if "ms_segment_sep" not in self.format_config:
                self.format_config["ms_segment_sep"] = ""
            if "seg_column_sep" not in self.format_config:
                self.format_config["seg_column_sep"] = " "
            if "ms_column_sep" not in self.format_config:
                self.format_config["ms_column_sep"] = " "
            if "col_line_sep" not in self.format_config:
                self.format_config["col_line_sep"] = ", "
        return super().parse_format_config()
    
    def format(self, reference):
        assert isinstance(reference, DSS_Reference), "reference must be a DSS_Reference object"
        cave = reference.Cave_Number 
        manuscript = reference.Manuscript_Designator
        column = reference.Column
        if reference.Use_Capital_Columns:
            column = column.upper()
        else:
            column = column.lower()
        line = reference.Line
        segment = reference.Segment_Indicator
        if segment is None or not self.format_config["segment_indicator"]:
            output = f"{cave}{self.format_config['location_id']}{manuscript}{self.format_config['ms_column_sep']}{column}{self.format_config['col_line_sep']}{line}"
        else:
            output = f"{cave}{self.format_config['location_id']}{manuscript}{self.format_config['ms_segment_sep']}{segment}{self.format_config['seg_column_sep']}{column}{self.format_config['col_line_sep']}{line}"
        return output
class Base_Pair_Formatter:

    def __init__(self, format_config):
        self.format_config = format_config
        self.parse_format_config()

    def parse_format_config(self):
        assert isinstance(self.format_config, dict), "format_config must be a dictionary"
    
    def format(self, reference_page_pair: tuple):
        raise NotImplementedError("format() not implemented")
    
class DSS_Pair_Formatter(Base_Pair_Formatter):

    def __init__(self, format_config):
        self.format_config = format_config
        self.parse_format_config()

    def parse_format_config(self):
        if self.format_config == {}:
            self.format_config = {
                "reference_page_sep": " "
            }
        else:
            if "reference_page_sep" not in self.format_config:
                self.format_config["reference_page_sep"] = " "
        return super().parse_format_config()
    
    def format(self, reference_page_pair: tuple):
        reference = reference_page_pair[0]
        page = reference_page_pair[1]
        formatted_reference = Bible_Reference_Formatter(self.format_config).format(reference)
        return f'{formatted_reference} {page}'
class Bible_Pair_Formatter(Base_Pair_Formatter):

    def parse_format_config(self):
        if self.format_config == {}:
            self.format_config = {
                "reference_page_sep": " "
            }
        else:
            if "reference_page_sep" not in self.format_config:
                self.format_config["reference_page_sep"] = " "
        return super().parse_format_config()
    
    def format(self, reference_page_pair: tuple):
        reference = reference_page_pair[0]
        page = reference_page_pair[1]
        formatted_reference = Bible_Reference_Formatter(self.format_config).format(reference)
        return f'{formatted_reference} {page}'