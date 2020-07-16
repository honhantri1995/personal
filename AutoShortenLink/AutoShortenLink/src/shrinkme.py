import time

from constants import IMAGE_PATH, SHRINKME_IMAGE_PATH, MAX_COUNTDOWN_TIMER
from browser_driver import BrowserDriver
from element_locator import ElementLocator
from logger import Logger

class ShrinkMe:
    def __init__(self, browser_driver):
        self.browser_driver = browser_driver
        self.logger = Logger.get_instance()
        self.element_locator = ElementLocator(self.browser_driver)

    def shorten_link(self, url):
        self.browser_driver.open_url(url)
        # if self.browser_driver.is_nointernet():
        if self.browser_driver.connect():
            return

        self.browser_driver.set_main_tab_handle()

        if self.__solve_captcha_imnotarobot():
            time.sleep(5)
        else:
            return

        if self.__solve_captcha_choosingimages():
            time.sleep(5)
        else:
            return

        if self.__click_clickheretocontinue():
            time.sleep(5)
            time.sleep(MAX_COUNTDOWN_TIMER)       # Wait for count-down timer
        else:
            return

        if self.__getlink():
            time.sleep(5)
        else:
            return

    def __solve_captcha_imnotarobot(self):
        print("Solving captcha_imnotarobot.")
        result = self.element_locator.locate_and_click_on_element(15, SHRINKME_IMAGE_PATH + 'ImNotARobot2.png', 2)

        if result:
            print('Passed captcha_imnotarobot.')
            self.logger.info('Succeeded to solve captcha IM NOT A ROBOT.')
        else:
            self.logger.error('Failed to solve captcha IM NOT A ROBOT.')
            self.logger.screenshot()
        return result

    def __solve_captcha_choosingimages(self):
        print("Solving captcha_choosingimages.")
        result = self.element_locator.locate_and_click_on_element(10, IMAGE_PATH + 'Buster_CaptchaSolver.png', 4)

        if result:
            print('Passed captcha_choosingimages.')
            self.logger.info('Succeeded to solve captcha CHOOSING IMAGES.')
        else:
            self.logger.error('Failed to solve captcha CHOOSING IMAGES.')
            self.logger.screenshot()
        return result

    def __click_clickheretocontinue(self):
        print("Solving ClickHereToContinue.")
        result = self.element_locator.locate_and_click_on_element(15, SHRINKME_IMAGE_PATH + 'ClickHereToContinue.png', 2)

        if result:
            print('Passed ClickHereToContinue.')
            self.logger.info('Succeeded to click on CLICK HERE TO CONTINUE.')
        else:
            self.logger.error('Failed to click on CLICK HERE TO CONTINUE.')
            self.logger.screenshot()
        return result

    def __getlink(self):
        print("Solving GetLink.")
        result = self.element_locator.locate_and_click_on_element(10, SHRINKME_IMAGE_PATH + 'GetLink.png', 2)

        if result:
            print('Passed GetLink.')
            self.logger.info('Succeeded to click on GET LINK.')
        else:
            self.logger.error('Failed to click on GET LINK.')
            self.logger.screenshot()
        return result
