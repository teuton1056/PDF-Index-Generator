import PyPDF2
from index_loggers import intake_logger


class Intake_PDF:
    def __init__(self, base_number=0):
        self.base_number = base_number
        assert isinstance(self.base_number, int), "Base number must be an integer"

    def load_pdf_file(self, file_path: str) -> list:
        """
        Takes the path to a file and returns the text of each page in a list of dictionaries.
        a page has three keys, 'Raw_Number', 'Relative_Number' and 'Raw_Text'
        Of these, the first two are ints and the last is a string.
        """
        intake_logger.info(f"Loading file: {file_path}")
        pdfFileObj = open(file_path, "rb")
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        number_of_pages = len(pdfReader.pages)
        intake_logger.debug(f"Number of pages: {number_of_pages}")
        document = []
        for number in range(number_of_pages):
            pageObj = pdfReader.pages[number]
            # extracting text from page
            text = pageObj.extract_text()
            # log the amount of text extracted
            intake_logger.debug(
                f"Page {number} text length: {len(text)}"
            )  # the length is in chars
            if len(text) < 100:
                intake_logger.warning(
                    f"Page {number} text length is less than 100 chars. Text: {text}"
                )
            page = {
                "Raw_Number": int(number),
                "Relative_Number": int(number) + self.base_number,
                "Raw_Text": text,
            }
            document.append(page)  # each page is a dictionary
        # closing the pdf file object
        pdfFileObj.close()
        intake_logger.debug(f"Document loaded. Number of pages: {len(document)}")
        return document
