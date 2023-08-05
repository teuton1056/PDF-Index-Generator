import PyPDF2
from index_loggers import intake_logger

class Intake_PDF:

    def __init__(self, base_number=0):
        self.base_number = base_number

    def load_pdf_file(self, file_path):
        intake_logger.info(f"Loading file: {file_path}")
        pdfFileObj = open(file_path, 'rb')  
        pdfReader = PyPDF2.PdfReader(pdfFileObj)  
        number_of_pages = len(pdfReader.pages)
        intake_logger.debug(f"Number of pages: {number_of_pages}")
        document = []
        for number in range(number_of_pages):
            pageObj = pdfReader.pages[number]
            # extracting text from page  
            text = pageObj.extract_text()
            page = {'Raw_Number':int(number), 'Relative_Number':int(number) + self.base_number,'Raw_Text':text}
            document.append(page)
        # closing the pdf file object  
        pdfFileObj.close()
        intake_logger.debug(f"Document loaded. Number of pages: {len(document)}")
        return document