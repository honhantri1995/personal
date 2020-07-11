import random

from constants import USER_AGENT_LIST_PATH

class UserAgentReader:
    def __init__(self):
        file = open(USER_AGENT_LIST_PATH, 'r', encoding='utf-8')
        self.lines = file.readlines()

    ''' Get random item from the list, but might be duplicate items
    '''
    def get_random(self):
        return random.choice(self.lines).strip().rstrip('\n')
