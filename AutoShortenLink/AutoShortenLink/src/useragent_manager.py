import random

from constants import USER_AGENT_LIST_PATH
from logger import Logger

class UserAgentManager:
    def __init__(self):
        self.lines = self.__read_file()
        self.logger = Logger.get_instance()

    def __read_file(self):
        file = open(USER_AGENT_LIST_PATH, 'r', encoding='utf-8')
        return file.readlines()

    ''' Get random item from the list, but might be duplicate items
    '''
    def get_random_useragent(self):
        return random.choice(self.lines).strip().rstrip('\n')
