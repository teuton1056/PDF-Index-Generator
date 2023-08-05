import intake
import reference_parser
from index_loggers import main_logger 

def main():
    main_logger.info("Starting program")
    intake_obj = intake.Intake_PDF()
    document = intake_obj.load_pdf_file("test.pdf")
    parser = reference_parser.Main_Parser()
    refs = parser.parse_lines(document)
    # ... do stuff with refs
    main_logger.info("Program complete")