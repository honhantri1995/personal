import os
import time

from selenium import webdriver
# import pyautogui


# from selenium.webdriver.common.keys import Keys

from conf import Conf
from logger import Logger
from user_agent_reader import UserAgentReader

class BrowserDriver:
    def __init__(self):
        self.driver = None
        self.conf = Conf()
        self.logger = Logger()
        self.main_tab_handle = None

    def __set_browser_settings(self):
        options = webdriver.chrome.options.Options()

        # Set windows to full screen
        options.add_argument("start-maximized")
        # Disable all extensions
        # options.add_argument("--disable-extensions")
        # Load cookies from profile (for login)
        options.add_argument("user-data-dir=" + os.getenv('LOCALAPPDATA') + "\\Google\\Chrome\\User Data")
        # Keep openning the browser window after the script is completed
        options.add_experimental_option("detach", True)
        # Click Block on Show Notifications popup (1: Allow, 2: Block)
        options.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 2 })
        # Disable "Chrome is being controlled by automated test software"
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # Disable the driver to install other chrome extensions, such as CaptureScreenshot and others.
        options.add_experimental_option('useAutomationExtension', False)
        # Set "navigator.webdriver" in Chrome console to False  --> Prevent Selenium detection
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        return options

    def start_browser(self):
        options = self.__set_browser_settings()
        self.driver = webdriver.Chrome(executable_path=self.conf.get_browser_driver_path(), options=options)
        self.__delete_cookies()
        self.__set_random_useragent()

    ''' Use a different user agent each time the Chrome driver is started --> Prevent Selenium detection
    '''
    def __set_random_useragent(self):
        user_agent_reader = UserAgentReader()
        user_agent_dic = {}
        user_agent_dic["userAgent"] = user_agent_reader.get_random()
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', user_agent_dic)

        self.logger.info(user_agent_dic)

    ''' Delete coockies
    '''
    def __delete_cookies(self, user=None):
        if user:
            self.driver.delete_cookie(user)
        else:
            self.driver.delete_all_cookies()

    def set_main_tab_handle(self):
        self.main_tab_handle = self.driver.current_window_handle

    def is_on_main_tab(self):
        return True if self.main_tab_handle == self.driver.current_window_handle else False

    def open_url(self):
        url = self.conf.get_url()
        self.driver.get(url)

    def close_other_tabs(self):
        # Note: The time to open a new time might be longer than the code execution, so the following checking can lead to wrong behavior.
        # if self.is_on_main_tab():
        #     return
        count = 0
        while count < 2:
            count += 1
            time.sleep(1)       # Wait for all other tabs to be opened
            handle_list = self.driver.window_handles
            if len(handle_list) > 1:
                for handle in handle_list:
                    if handle != self.main_tab_handle:
                        print("Close other tabs")
                        self.driver.switch_to_window(handle)
                        self.driver.close()
                self.driver.switch_to_window(self.main_tab_handle)