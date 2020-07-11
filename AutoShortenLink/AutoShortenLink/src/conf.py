from configparser import ConfigParser
from constants import CONFIG_PATH

class Conf:
    def __init__(self):
        # Note: By default, configparser automatically delete all comment marks (start with '#' or ';') when writing to the file.
        # A trick to avoid this is to set "comment_prefixes=" to empty so that no marks are consided as comment.
        # self.conf = ConfigParser(comment_prefixes=())
        self.conf = ConfigParser()
        self.conf.read(CONFIG_PATH)

    def get_browser_driver_path(self):
        return self.conf.get('PATH', 'CHROME_DRIVER')

    def get_url(self):
        return self.conf.get('SHRINKME', 'URL')

    # def get_xpath_of_clickheretocontinue(self):
    #     return self.conf.get('SHRINKME', 'XPATH_CLICKTOCONTINUE')

    # def get_xpath_of_imnotarobot(self):
    #     return self.conf.get('SHRINKME', 'XPATH_IMNOTAROBOT')