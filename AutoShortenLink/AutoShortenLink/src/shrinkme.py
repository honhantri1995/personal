import time

import pyautogui

from constants import SHRINKME_IMAGE_PATH, MAX_COUNTDOWN_TIMER
from browser_driver import BrowserDriver

class ShrinkMe:
    def __init__(self, browser_driver):
        self.browser_driver = browser_driver

    def shorten_link(self):
        self.browser_driver.open_url()
        self.browser_driver.set_main_tab_handle()

        self.__solve_captcha_imnotarobot()
        self.__solve_captcha_choosingimages_using_bustercaptchasolver()
        self.__clickheretocontinue()
        self.__getlink()

    def __solve_captcha(self, retry_no, image):
        is_image_loaded = False
        retry = 0
        while retry < retry_no:
            retry += 1

            # In rare cases, still want to make sure we're on the right tab
            if not self.browser_driver.is_on_main_tab():
                self.browser_driver.close_other_tabs()
                continue

            # Note: Can use pyautogui.locateCenterOnScreen(), but it throws exception if image is not found.
            # By contrast, pyautogui.locateAllOnScreen() does not. So we can easily check whether image is loaded or not, and loaded how many times.1
            pos_list = list(pyautogui.locateAllOnScreen(image, confidence=0.8))
            # print(len(pos_list))
            # No captcha found
            if len(pos_list) == 0:
                # Image have not loaded and displayed --> will wait for it
                if not is_image_loaded:
                    print('Catcha have not loaded yet')
                    time.sleep(2)
                    continue
                # Already clicked on the image (making it disappeared) --> succeeded to solve the captcha
                if is_image_loaded and self.browser_driver.is_on_main_tab():
                    print('Passed captcha')
                    break
            # Captcha found --> will solve it
            else:
                is_image_loaded = True
                print('Position is ' + str(pos_list[0]))
                x, y = pyautogui.center(pos_list[0])
                pyautogui.click(x, y)
                self.browser_driver.close_other_tabs()

    def __solve_captcha_imnotarobot(self):
        print("Solving I'm not a robot")
        self.__solve_captcha(15, SHRINKME_IMAGE_PATH + 'ImNotARobot2.png')
        time.sleep(5)

    def __solve_captcha_choosingimages_using_bustercaptchasolver(self):
        print("Solving choosing images using Buster")
        self.__solve_captcha(5, SHRINKME_IMAGE_PATH + 'Buster_CaptchaSolver.png')
        time.sleep(10)

    def __clickheretocontinue(self):
        print("Solving ClickHereToContinue")
        self.__solve_captcha(15, SHRINKME_IMAGE_PATH + 'ClickHereToContinue.png')
        time.sleep(5)

    def __getlink(self):
        print("Solving GetLink")
        time.sleep(MAX_COUNTDOWN_TIMER)       # Wait for count-down timer
        self.__solve_captcha(10, SHRINKME_IMAGE_PATH + 'GetLink.png')
        time.sleep(5)