import os
import time

from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
from proxy_checker import ProxyChecker

# import pyautogui


# from selenium.webdriver.common.keys import Keys

from conf import Conf
from logger import Logger
from user_agent_reader import UserAgentReader
from proxy_reader import ProxyReader

class BrowserDriver:
    def __init__(self):
        self.driver = None
        self.conf = Conf()
        self.main_tab_handle = None
        self.logger = Logger.get_instance()

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

        # Set proxy
        proxy_reader = ProxyReader()
        proxy = proxy_reader.get_random()
        proxy_info = self.__validate_proxy(proxy)
        if proxy_info is False:
            self.logger.error('Invalid proxy: ' + proxy)
        else:
            options.add_argument('--proxy-server={}'.format(proxy))
            # Output to log
            self.logger.info(proxy_info)

        return options

    def start_browser(self):
        options = self.__set_browser_settings()
        self.driver = webdriver.Chrome(executable_path=self.conf.get_browser_driver_path(), options=options)
        self.__set_random_useragent()
        self.__delete_cookies()

    def get_webdriver(self):
        return self.driver

    def __validate_proxy(self, proxy):
        checker = ProxyChecker()
        return checker.check_proxy(proxy)

    ''' Use a different user agent each time the Chrome driver is started --> Prevent Selenium detection
    '''
    def __set_random_useragent(self):
        user_agent_reader = UserAgentReader()
        user_agent_dic = {}
        user_agent_dic["userAgent"] = user_agent_reader.get_random()
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', user_agent_dic)

        # Output to log
        self.logger.info(user_agent_dic)

    ''' Delete coockies
    '''
    def __delete_cookies(self, name=None):
        # print("Before cookies: " + str(self.driver.get_cookies()))
        # time.sleep(1)
        # if name:
        #     self.driver.delete_cookie(name)
        #     time.sleep(10)
        #     print("this case")
        # else:
        #     self.driver.delete_all_cookies()
        #     time.sleep(10)
        #     # self.driver.refresh()
        # print("After cookies: " + str(self.driver.get_cookies()))

        # self.driver.get('chrome://settings/siteData')
        # # self.driver.find_element_by_xpath('//*[@id="removeShowingSites"]').click()
        # # self.driver.find_element_by_xpath('//*[@id="confirmDeleteDialog"]/div[3]/cr-button[2]').click(0)

        # wait = WebDriverWait(self.driver, 10)
        # remove_cookies_btn = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'removeShowingSites')))
        # remove_cookies_btn.click()

        # confirm_btn = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="confirmDeleteDialog"]/div[3]/cr-button[2]')))
        # confirm_btn.click()

        # time.sleep(2)

        self.driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
        self.driver.execute_cdp_cmd('Network.deleteCookies', {})

        self.driver.execute_cdp_cmd('Network.clearBrowserCache', {})

        time.sleep(2)


    def set_main_tab_handle(self):
        self.main_tab_handle = self.driver.current_window_handle

    def is_on_main_tab(self):
        return True if self.main_tab_handle == self.driver.current_window_handle else False

    def open_url(self):
        url = self.conf.get_url()
        # self.driver.get(url)
        # self.__delete_cookies('1rx.io')

        # Output to log
        logger = Logger.get_instance()
        logger.info(url)

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