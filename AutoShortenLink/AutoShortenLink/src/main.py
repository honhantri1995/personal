import time

from browser_driver import BrowserDriver
from shrinkme import ShrinkMe
from conf import Conf
from proxy_manager import ProxyManager
from useragent_manager import UserAgentManager

def main():
    useragent_mng = UserAgentManager()
    proxy_mng = ProxyManager()
    conf = Conf()

    # 51.222.12.136:8080
    proxies = proxy_mng.get_proxies(shuffled=True)
    for proxy in proxies:
        # if not proxy_mng.is_valid_proxy(proxy):
        #     print('Invalid proxy: ' + proxy)
        #     continue
        #     # break

        useragent = useragent_mng.get_random_useragent()
        print('Open browser')
        # driver = BrowserDriver()
        # driver = BrowserDriver(useragent=useragent)
        driver = BrowserDriver(proxy=proxy, useragent=useragent)
        driver.open_browser()

        shrinkme = ShrinkMe(driver)
        shrinkme.shorten_link(conf.get_url())

        driver.quit_browser()
        time.sleep(5)

if __name__ == "__main__":
    main()

    # You're not connected
    # This page isn't working right now
    # There is something wrong with the proxy server, or the address is incorrect.
