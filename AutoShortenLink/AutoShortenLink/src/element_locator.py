import time

import pyautogui

# from constants import RESULT_ENUM
from browser_driver import BrowserDriver
from humanlike_mouse import HumanlikeMouse
from logger import Logger

class ElementLocator:
    def __init__(self, browser_driver):
        self.browser_driver = browser_driver
        self.logger = Logger.get_instance()

    def locate_and_click_on_element(self, retry_no, element_image, wait_time):
        is_element_loaded = False
        retry = 0
        while retry < retry_no:
            retry += 1

            # In rare cases, still want to make sure we're on the right tab
            if not self.browser_driver.is_on_main_tab():
                self.browser_driver.close_other_tabs()
                continue

            if self.__is_bot_detected():
                return False

            # Note: Can use pyautogui.locateCenterOnScreen(), but it throws exception if element is not found.
            # By contrast, pyautogui.locateAllOnScreen() does not. So we can easily check whether element is loaded or not, and loaded how many times.1
            pos_list = list(pyautogui.locateAllOnScreen(element_image, confidence=0.8))
            # print(len(pos_list))
            # No element found
            if len(pos_list) == 0:
                # Element have not loaded and displayed --> will wait for it
                if not is_element_loaded:
                    print('Element have not loaded yet')
                    time.sleep(2)
                    continue
                # Element is clicked and no longer appears
                elif is_element_loaded and self.browser_driver.is_on_main_tab():
                    return True     # Suceess
            # Element is found --> will click on it
            else:
                is_element_loaded = True
                print('Element position is ' + str(pos_list[0]) + '\n')
                x, y = pyautogui.center(pos_list[0])
                mouse = HumanlikeMouse()
                mouse.move_and_click(x, y)
                self.browser_driver.close_other_tabs()
                time.sleep(wait_time)

        return False    # Fail

    def __is_bot_detected(self):
        web_msg_list = ['Please upgrade to a supported browser to get a reCAPTCHA challenge.',
                        'Your computer or network may be sending automated queries.'
        ]

        for web_msg in web_msg_list:
            if str(web_msg) in self.browser_driver.get_webdriver().page_source.encode("utf-8"):
                self.logger.error('Bot is DETECTED! ' + '({})'.format(web_msg))
                self.logger.screenshot()
                return True

        return False