from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Paths (can be moved to a config file later if needed)
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
chrome_driver_path = "D:\\Prog\\Chromium\\chromedriver-win64\\chromedriver.exe"
download_directory = "D:\\Prog\\Python\\Erik\\Hatóanyagok"

# Set up Chrome options
def get_chrome_options():
    chrome_options = Options()
    chrome_options.binary_location = brave_path
    chrome_options.add_argument("--headless=new")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")  # Simulate normal window size

    # Set preferences for downloads
    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    return chrome_options

# Function to start the browser
def start_browser():
    service = Service(chrome_driver_path)
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    time.sleep(1)
    return driver

# Function to stop the browser
def stop_browser(driver):
    driver.quit()
