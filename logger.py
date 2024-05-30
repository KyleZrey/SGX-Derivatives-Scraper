import logging

def setup_logger(file_name):
    # Create logger
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(file_name)
    console_handler = logging.StreamHandler()

    # Set the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def setup_logger_file(file_name):
    # Create logger
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(file_name)

    # Set the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)

    return logger
