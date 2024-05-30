import logging

def setup_logger():
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler("scraper.log")
    console_handler = logging.StreamHandler()

    # Set the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Example usage:
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Logger setup complete.")
