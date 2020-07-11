import os
import logging
from constants import LOG_PATH

class Logger():
    def __init__(self):
        self.logger = None
        self.__configure_logging()

    def __create_dir(self):
        relative_dir = os.path.dirname(LOG_PATH)                    # Get relative dir path from file path (eg: ../log/log.txt  --> ../log/)
        absolute_path = os.path.join(os.getcwd(), relative_dir)     # Append current dir + relative dir path

        if not os.path.isdir(absolute_path):                        # If no dir, create it
            os.mkdir(absolute_path)

    def __configure_logging(self):
        self.__create_dir()

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)         # Log level INFO or above will be outputted
        filehandler = logging.FileHandler(filename=LOG_PATH, mode='w+', encoding='utf-8')
        formatter = logging.Formatter('[%(asctime)s] [%(filename)s: %(lineno)s] [%(levelname)s] %(message)s')
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)

    def error(self, log):
        return self.logger.error(log)

    def info(self, log):
        return self.logger.info(log)