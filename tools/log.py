import logging
import setting

def log(name):
    logger = logging.getLogger(name)
    if setting.log_grade:
        if setting.log_grade == "error":
            logger.setLevel(logging.ERROR)
        elif setting.log_grade == "debug":
            logger.setLevel(logging.DEBUG)
        elif setting.log_grade == "info":
            logger.setLevel(logging.INFO)
        elif setting.log_grade == "warning":
            logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.ERROR)
    # create console handler and set level to debug

    ch = logging.StreamHandler()
    # create formatter for console handler

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to console handler
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger