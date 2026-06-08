import reference_formatter
import Index_Models
import json
from index_loggers import index_logger

def create_index_entries(refs: list, page: int) -> list:
    """
    Creates a list of index entries from a list of references.
    """
    index_logger.debug(f"Creating {len(refs)} index entries for page {page}")
    entries = []
    for ref in refs:
        entries.append(Index_Entry(ref, page))
    return entries

class Index_Entry:

    def __init__(self, reference, page):
        self.reference = reference
        self.page = page
        self.formatted_reference = None
        self.formatted_entry = None

    def __str__(self):
        return str(self.reference) + " " + str(self.page)
    
    def __repr__(self):
        return str(self.reference) + " " + str(self.page)

class Index:

    """
    The Index class is a top-level class which contains all the index entries (Index_Entry objects).
    """

    def __init__(self, index_entries = []):
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

    def add_entries(self, entries: list):
        """
        Adds entries to index.
        """
        self.entries.extend(entries)

    def sub_group_entries(self, group, tag):
        """
        Sub-groups entries by tag.
        """
        pass # TODO

    def load_sort_order(self, sorting: str) -> dict:
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
    
    def load_sort_order_from_file(self, name: str) -> dict:
        with open(f"sort_order/{name}.json", 'r') as f:
            sort_order = json.load(f) 
        return sort_order
    
    def sort_entries_by_order(self, group: list, order: dict) -> list:
        """
        Sorts entries by reference.
        """
        index_logger.debug("Sorting entries by order")
        index_logger.debug(f"Order: {order}")
        index_logger.debug(f"Group Before Any Sorting: {group}")
        group.sort(key=lambda x: x.formatted_reference)
        index_logger.debug(f"Group After Initial Alphabetical Sort: {group}")
        group.sort(key=lambda x: int(order[x.reference.book]))
        index_logger.debug(f"Group After Book Sort: {group}")
        return group

    def _txt_format(self) -> str:
        """
        Formats index for .txt file.
        """
        index_logger.debug("Formatting index for .txt file")
        output = ""
        groups = self.group_entries()
        for group in groups:
            if output != "":
                output += "" # TODO: provide a way to separate groups
            self.format_group(groups[group])
            order = self.load_sort_order(group.__name__)
            if order != {}:
                groups[group] = self.sort_entries_by_order(groups[group], order)
            else:
                groups[group].sort(key=lambda x: x.formatted_reference)
            for entry in groups[group]:
                output += entry.formatted_entry + "\n"
        return output

    def _html_format(self) -> str:
        """
        Formats index as an HTML document.
        """
        index_logger.debug("Formatting index for .html file")
        groups = self.group_entries()
        sections_html = ""
        for group in groups:
            self.format_group(groups[group])
            order = self.load_sort_order(group.__name__)
            if order != {}:
                groups[group] = self.sort_entries_by_order(groups[group], order)
            else:
                groups[group].sort(key=lambda x: x.formatted_reference)
            rows = ""
            for entry in groups[group]:
                ref = entry.formatted_reference.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                rows += f"        <tr><td class=\"ref\">{ref}</td><td class=\"page\">{entry.page}</td></tr>\n"
            section_title = group.__name__.replace("_", " ")
            sections_html += (
                f"    <section>\n"
                f"      <h2>{section_title}</h2>\n"
                f"      <table>\n"
                f"        <thead><tr><th>Reference</th><th>Page</th></tr></thead>\n"
                f"        <tbody>\n"
                f"{rows}"
                f"        </tbody>\n"
                f"      </table>\n"
                f"    </section>\n"
            )
        return (
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"UTF-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            "  <title>Index</title>\n"
            "  <style>\n"
            "    body { font-family: serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }\n"
            "    h1 { font-size: 1.8rem; border-bottom: 2px solid #333; padding-bottom: 0.5rem; }\n"
            "    h2 { font-size: 1.2rem; margin-top: 2rem; color: #444; }\n"
            "    table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }\n"
            "    th { text-align: left; border-bottom: 1px solid #999; padding: 0.3rem 0.5rem; }\n"
            "    td { padding: 0.2rem 0.5rem; }\n"
            "    tr:nth-child(even) { background: #f5f5f5; }\n"
            "    td.page { color: #555; width: 4rem; text-align: right; }\n"
            "  </style>\n"
            "</head>\n"
            "<body>\n"
            "  <h1>Index</h1>\n"
            f"{sections_html}"
            "</body>\n"
            "</html>\n"
        )

    def format_index(self, format_type: str) -> str:
        """
        Formats index.
        """
        if format_type == "txt":
            return self._txt_format()
        elif format_type == "html":
            return self._html_format()
        else:
            raise Exception("Invalid format type: " + format_type)

    def __str__(self):
        return str(self.entries)
    