from browser_driver import BrowserDriver
from shrinkme import ShrinkMe

def main():
    driver = BrowserDriver()
    driver.start_browser()

    shrinkme = ShrinkMe(driver)
    shrinkme.shorten_link()

if __name__ == "__main__":
    main()