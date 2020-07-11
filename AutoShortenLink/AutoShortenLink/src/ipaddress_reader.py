import random

from constants import IP_ADDRESS_LIST_PATH

class IpAddressReader:
    def __init__(self):
        file = open(IP_ADDRESS_LIST_PATH, 'r', encoding='utf-8')
        self.lines = file.readlines()

    ''' Get random items from the list, without duplicate items
    '''
    def get_random(self):
        return random.sample(self.lines, len(self.lines)).strip().rstrip('\n')
