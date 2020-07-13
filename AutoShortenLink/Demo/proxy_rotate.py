from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

def get_proxy_from_sslproxies():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=options, executable_path=r'E:\\PROJECTS\\MYPROJECT\\Personal\\AutoShortenLink\\AutoShortenLink\\chromedriver_win32\\chromedriver.exe')
    driver.get("https://sslproxies.org/")

    # IP Address Column name
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
    # Ip Address
    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
    print("=========== IP: ")
    print(ips)
    # Port
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
    print("=========== Port: ")
    print(ports)

    driver.quit()

    proxies = []
    for i in range(0, len(ips)):
        proxies.append(ips[i]+':'+ports[i])
    print("=========== Proxies: ")
    print(proxies)

    return proxies

def check_proxies_after_changed():
    proxies = get_proxy_from_sslproxies()

    for i in range(0, len(proxies)):
        print("Proxy selected: {}".format(proxies[i]))
        options = webdriver.ChromeOptions()
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

        options.add_argument('--proxy-server={}'.format(proxies[i]))
        driver = webdriver.Chrome(options=options, executable_path=r'E:\\PROJECTS\\MYPROJECT\\Personal\\AutoShortenLink\\AutoShortenLink\\chromedriver_win32\\chromedriver.exe')
        # driver.get("https://www.whatismyip.com/proxy-check/?iref=home")
        # if "Proxy Type" in WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.card-text"))):
        #     print("Proxy detected: ")
        #     break

        # driver.get("https://www.whatismyip.com/ip-address-lookup/?iref=navbar")
        # ip_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="post-5236"]/div[1]/div[1]/form/div/input')))
        # ip_input.clear()
        # ip_input.send_keys()

        driver.get("https://www.whatismyip.com/")
        ip_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="post-7"]/div[1]/div/div[1]/div/div/ul/li[1]/a/text()')))
        print("========== Result: ")
        print(ip_result)

        location_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="post-7"]/div[1]/div/div[1]/div/div/ul/li[3]/text()')))
        print(location_result)

        time.sleep(30)

def check_proxy_after_changed():
    proxy = '203.204.200.107:80'
    print("Proxy selected: {}".format(proxy))

    options = webdriver.ChromeOptions()
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

    options.add_argument('--proxy-server={}'.format(proxy))
    driver = webdriver.Chrome(options=options, executable_path=r'E:\\PROJECTS\\MYPROJECT\\Personal\\AutoShortenLink\\AutoShortenLink\\chromedriver_win32\\chromedriver.exe')

    # driver.get("https://www.whatismyip.com/")
    # ip_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="post-7"]/div[1]/div/div[1]/div/div/ul/li[1]/a/text()')))
    # print("========== Result: ")
    # print(ip_result)

    # location_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="post-7"]/div[1]/div/div[1]/div/div/ul/li[3]/text()')))
    # print(location_result)

    driver.get("https://www.zing.vn")

    time.sleep(30)

check_proxy_after_changed()
# check_proxies_after_changed()