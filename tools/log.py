import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# create console handler and set level to debug

ch = logging.StreamHandler()
# create formatter for console handler

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to console handler
ch.setFormatter(formatter)
logger.addHandler(ch)