import json 


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
    
    def load_alias_file(fname):
        try:
            with open(fname) as f:
                alias_dict = json.load(f)
        except FileNotFoundError:
            alias_dict = {}
            

class OT_Parser(Reference_Parser):

    def __init__(self, configurations: dict = None):
        super().__init__(configurations)
        self.configurations = configurations

    def parse(self, reference_string: str):
        """
        Parses a reference string for an Old Testament reference
        """
        return 'OT Reference'