import logging 



# create the formatter 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create the console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# Create the file handler
fh = logging.FileHandler('Index Generation.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# Create the reference logger
ref_logger = logging.getLogger("Reference_Parser")
ref_logger.setLevel(logging.DEBUG)
ref_logger.addHandler(ch)
ref_logger.addHandler(fh)

