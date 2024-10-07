from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

brave_path = "ADD MEG A BRAVE BÖNGÉSZŐ ELÉRÉSI ÚTVONALÁT"
chrome_driver_path = "ADD MEG A CHROME DRIVER ELÉRÉSI ÚTVONALÁT"
download_directory = "ADD MEG HOVA SZERETNÉD LETÖLTENI A PDF DOKUMENTUMOKAT"

def get_chrome_options():
    chrome_options = Options()
    chrome_options.binary_location = brave_path
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    return chrome_options

def start_browser():
    service = Service(chrome_driver_path)
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    time.sleep(1)
    return driver

def stop_browser(driver):
    driver.quit()
