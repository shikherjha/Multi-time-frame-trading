import logging
import os

def Setup_logger(name="Tading bot", file_name = "log_file.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if logger.handlers:
        return logger
    
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(formatter)

    f_handler = logging.FileHandler(file_name)
    f_handler.setLevel(logging.INFO)
    f_handler.setFormatter(formatter)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

