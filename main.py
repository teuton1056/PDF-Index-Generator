import intake
import reference_parser
from index_loggers import main_logger 
from Index import Index, Index_Entry, create_index_entries
import time 
import sys

def main(fname="sample_pdfs/test_1.pdf", base_number=1):
    t = time.time()
    main_logger.info("Starting program")
    intake_obj = intake.Intake_PDF(base_number=1)
    document = intake_obj.load_pdf_file(fname)
    parser = reference_parser.Main_Parser(["OT", "NT", "AP", "DSS"])
    index = Index()
    parsed_pages = parser.parse_document(document)
    for page in parsed_pages:
        index_entries = create_index_entries(parsed_pages[page], page)
        index.add_entries(index_entries)
    str_index = index.format_index('txt')
    with open("index.txt", "w") as f:
        f.write(str_index)
    # ... do stuff with refs
    main_logger.info("Program complete")
    main_logger.info("Time elapsed: " + str(time.time() - t))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Running with default values")
        main()
    elif len(sys.argv) == 2:
        print("Running without a base number")
        main(fname=sys.argv[1])   
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Too many arguments")
        sys.exit(1)