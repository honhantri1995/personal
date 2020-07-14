import random

from constants import PROXY_LIST_PATH

class ProxyReader:
    def __init__(self):
        file = open(PROXY_LIST_PATH, 'r', encoding='utf-8')
        self.lines = file.readlines()

    ''' Get random items from the list, without duplicate items
    '''
    def get_random(self):
        proxies = random.sample(self.lines, len(self.lines))
        return str(proxies).strip().rstrip('\n')
