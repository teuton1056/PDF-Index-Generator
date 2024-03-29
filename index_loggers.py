import logging 
import sys 


# create the formatter 
formatter = logging.Formatter(u"%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s @ %(module)s -> %(lineno)d")

# Create the console handler
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
ch.setFormatter(formatter)

# Create the file handler
fh = logging.FileHandler('Index Generation.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# Create the reference logger
ref_logger = logging.getLogger("Reference_Parser")
ref_logger.setLevel(logging.DEBUG)
ref_logger.addHandler(ch)
ref_logger.addHandler(fh)

# creat the intake logger
intake_logger = logging.getLogger("Intake")
intake_logger.setLevel(logging.DEBUG)
intake_logger.addHandler(ch)
intake_logger.addHandler(fh)

# create the formatting logger 
format_logger = logging.getLogger("Formatting")
format_logger.setLevel(logging.DEBUG)
format_logger.addHandler(ch)
format_logger.addHandler(fh)

# create the main logger
main_logger = logging.getLogger("Main")
main_logger.setLevel(logging.DEBUG)
main_logger.addHandler(ch)
main_logger.addHandler(fh)

# create the index logger
index_logger = logging.getLogger("Index")
index_logger.setLevel(logging.DEBUG)
index_logger.addHandler(ch)
index_logger.addHandler(fh)
