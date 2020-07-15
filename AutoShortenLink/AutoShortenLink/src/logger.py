import os
import inspect
import logging
import time

import pyautogui

from constants import LOG_PATH, LOG_IMAGE_PATH

class Logger():
    __instance = None

    @staticmethod
    def get_instance():
        if not Logger.__instance:
            Logger()
        return Logger.__instance

    def __init__(self):
        ''' Virtually private constructor
        '''
        if Logger.__instance:
            raise Exception("Logger class is a singleton!")
        else:
            Logger.__instance = self

        self.logger = None

        self.__create_dir(LOG_PATH)
        self.__create_dir(LOG_IMAGE_PATH)

        self.__configure_logger()

        self.__create_separator()

    def __configure_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)         # Log level INFO or above will be outputted
        filehandler = logging.FileHandler(filename=LOG_PATH, mode='a', encoding='utf-8')
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)

    @staticmethod
    def __get_callstack_info():
        stack = inspect.stack()

        # stack[1] gives previous function ('info' or 'error' in our case)
        # stack[2] gives before previous function, and so on
        file = os.path.basename(stack[2][1])    # Only get file name from path
        func = stack[2][3]
        line = stack[2][2]

        return file, func, line

    def __create_dir(self, path):
        relative_dir = os.path.dirname(path)                        # Get relative dir path from file path (eg: ../log/log.txt  --> ../log/)
        absolute_path = os.path.join(os.getcwd(), relative_dir)     # Append current dir + relative dir path

        if not os.path.isdir(absolute_path):                        # If no dir is found, create it
            os.mkdir(absolute_path)

    ''' Each time the script is started, a separator is added for higher readability
    '''
    def __create_separator(self):
        self.logger.info('\n')
        self.logger.info('=====================================================================================================================')

    def error(self, msg):
        full_msg = "[{}] [{}() - {}]: {}".format(*self.__get_callstack_info(), msg)
        return self.logger.error(full_msg)

    def info(self, msg):
        full_msg = "[{}] [{}() - {}]: {}".format(*self.__get_callstack_info(), msg)
        return self.logger.info(full_msg)

    def screenshot(self):
        current_time = time.strftime("%m%d%Y_%H%M%S", time.localtime())
        shot_name = LOG_IMAGE_PATH + current_time + '.png'
        pyautogui.screenshot(shot_name)