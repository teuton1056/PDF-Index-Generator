import reference_formatter
import Index_Models
import json
from index_loggers import index_logger

class Index_Entry:

    def __init__(self, reference, page):
        self.reference = reference
        self.page = page
        self.formatted_reference = None
        self.formatted_entry = None

    def __str__(self):
        return self.reference + " " + str(self.page)

class Index:

    """
    The Index class is a top-level class which contains all the index entries (Index_Entry objects).
    """

    def __init__(self, index_entries):
        self.entries = index_entries
        self.formatters = {
            Index_Models.Bible_Reference: reference_formatter.Bible_Reference_Formatter({}),
            Index_Models.DSS_Reference: reference_formatter.DSS_Reference_Formatter({})
        }
    
    def group_entries(self):
        """
        Groups entries by reference type.
        """
        groups = {}
        for entry in self.entries:
            if type(entry.reference) not in groups:
                groups[type(entry.reference)] = []
            groups[type(entry.reference)].append(entry)
        return groups
    
    def format_group(self, group):
        for entry in group:
            entry.formatted_reference = self.formatters[type(entry.reference)].format(entry.reference)
            entry.formatted_entry = entry.formatted_reference + ", " + str(entry.page)

    def sub_group_entries(self, group, tag):
        """
        Sub-groups entries by tag.
        """
        pass # TODO

    def sort_entries(self, group):
        """
        Sorts entries by reference.
        """
        pass # TODO

    def load_sort_order(self, sorting):
        index_logger.debug(f"Loading sort order for {sorting}")
        if sorting == 'NT':
            order = self.load_sort_order_from_file('NT')
            return order
        elif sorting == 'OT':
            order = self.load_sort_order_from_file('OT')
            return order
        elif sorting == 'Bible_Reference':
            ot_order = self.load_sort_order_from_file('OT')
            nt_order = self.load_sort_order_from_file('NT')
            nt_order = {k: str(int(v)+len(ot_order)) for k, v in nt_order.items()}
            order = {**ot_order, **nt_order}
            return order
        else:
            return {}
    
    def load_sort_order_from_file(self, name):
        with open(f"sort_order/{name}.json", 'r') as f:
            sort_order = json.load(f) 
        return sort_order
    
    def sort_entries_by_order(self, group: list, order: str) -> list:
        """
        Sorts entries by reference.
        """
        group.sort(key=lambda x: x.formatted_reference)
        group.sort(key=lambda x: order[x.reference.book])
        return group

    def _txt_format(self):
        """
        Formats index for .txt file.
        """
        output = ""
        groups = self.group_entries()
        for group in groups:
            self.format_group(groups[group])
            order = self.load_sort_order(group.__name__)
            if order != {}:
                groups[group] = self.sort_entries_by_order(groups[group], order)
            else:
                groups[group].sort(key=lambda x: x.formatted_reference)
            for entry in groups[group]:
                output += entry.formatted_entry + "\n"
        return output
    
    def format_index(self, format_type):
        """
        Formats index.
        """
        if format_type == "txt":
            return self._txt_format()
        else:
            raise Exception("Invalid format type: " + format_type)

    def __str__(self):
        return str(self.entries)
    