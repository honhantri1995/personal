import random

from proxy_checker import ProxyChecker

from constants import PROXY_LIST_PATH
from logger import Logger

class ProxyManager:
    def __init__(self):
        self.lines = self.__read_file()
        self.proxy_checker = ProxyChecker()
        self.logger = Logger.get_instance()

    def __read_file(self):
        file = open(PROXY_LIST_PATH, 'r', encoding='utf-8')
        return file.readlines()

    ''' Get random items from the list, without duplicates
    '''
    def get_proxies(self, shuffled=False):
        proxies = []

        for proxy in self.lines:
            proxies.append(proxy.strip().rstrip('\n'))

        if shuffled:
            random.shuffle(proxies)
        return proxies

    def is_valid_proxy(self, proxy):
        proxy_info = self.proxy_checker.check_proxy(proxy)
        if proxy_info == False:
            self.logger.error('Invalid proxy: ' + proxy)
            return False
        else:
            self.logger.info('Valid proxy: ' + str(proxy_info))
            return True