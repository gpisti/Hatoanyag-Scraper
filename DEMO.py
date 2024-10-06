from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
chrome_driver_path = "D:\\Prog\\Chromium\\chromedriver-win64\\chromedriver.exe"
download_directory = "D:\\Prog\\Python\\Erik\\Hatóanyagok"

chrome_options = Options()
chrome_options.binary_location = brave_path
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
    "safebrowsing.enabled": True,
}
chrome_options.add_experimental_option("prefs", prefs)


def start_browser(chrome_driver_path, chrome_options):
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()  # Ablak maximálisra állítása
    time.sleep(1)  # Várakozás, hogy biztosan maximálisan ki legyen terjesztve
    return driver


def enter_fullscreen(driver):
    driver.execute_script(
        "document.body.requestFullscreen();"
    )  # Kérje a teljes képernyős módot
    time.sleep(1)  # Várakozás, hogy a mód aktiválódjon


def stop_browser(driver):
    driver.quit()


def open_website(driver):
    driver.get("https://novenyvedoszer.nebih.gov.hu/engedelykereso/kereso")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (
                By.ID,
                "ContentPlaceHolder1_HatoanyagMultiSelectPopupControl_ShowPopupLinkButton",
            )
        )
    )
    print("Weboldal betöltve.")


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def select_active_ingredient(driver, index):
    try:
        dropdown_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "ContentPlaceHolder1_HatoanyagMultiSelectPopupControl_ShowPopupLinkButton",
                )
            )
        )
        dropdown_menu.click()

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "ContentPlaceHolder1_HatoanyagMultiSelectPopupControl_MultiSelectPopupUserControlPanelTable",
                )
            )
        )

        checkbox_id = f"ContentPlaceHolder1_HatoanyagMultiSelectPopupControl_MultiSelectPopupUserControlCheckBoxList_{index}"
        checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, checkbox_id))
        )

        # Görgessünk a checkboxhoz
        scroll_to_element(driver, checkbox)

        if not checkbox.is_selected():
            checkbox.click()
            print(f"Hatóanyag kiválasztva: {index}")
        else:
            print(f"Hatóanyag már kiválasztva: {index}")

        close_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.NAME,
                    "ctl00$ContentPlaceHolder1$HatoanyagMultiSelectPopupControl$CloseButton",
                )
            )
        )
        close_button.click()
        print("Rendben gombra kattintva.")
        time.sleep(1)

    except Exception as e:
        print(f"Hiba a hatóanyag kiválasztásakor: {str(e)}")


def get_number_of_results(driver):
    try:
        result_text = (
            WebDriverWait(driver, 20)
            .until(
                EC.visibility_of_element_located(
                    (By.ID, "ContentPlaceHolder1_talalatokDiv")
                )
            )
            .text
        )

        # A szám kinyerése a szövegből
        num_results = int(
            "".join(filter(str.isdigit, result_text))
        )  # Csak a számjegyeket tartja meg

        return num_results
    except Exception as e:
        print(f"Hiba a találatok számának lekérdezésekor: {str(e)}")
        return 0


def click_search_button(driver):
    try:
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.NAME, "ctl00$ContentPlaceHolder1$KeresesButton")
            )
        )
        search_button.click()
        print("Keresés gombra kattintva.")
        time.sleep(5)  # Megvárja, amíg az eredmények betöltődnek
    except Exception as e:
        print(f"Hiba a keresés végrehajtásakor: {str(e)}")


def process_search_results(driver):
    try:
        num_results = get_number_of_results(driver)
        if num_results == 0:
            print("Nincs találat.")
            return

        # Görgessünk le a táblázathoz
        table = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.ID, "ContentPlaceHolder1_NovszerGridView")
            )
        )
        scroll_to_element(driver, table)  # Görgessünk a táblázathoz
        rows = table.find_elements(By.XPATH, "//tr/td[1]/a")

        for i, row in enumerate(rows):
            # Görgessünk le a sorhoz
            scroll_to_element(driver, row)
            print(f"{i + 1}. sor feldolgozása...")
            row.click()
            time.sleep(3)
            download_pdfs(driver)
            close_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.NAME,
                        "ctl00$ContentPlaceHolder1$InfoNovszerControl$CloseButton",
                    )
                )
            )
            close_button.click()
            print("PDF információs ablak bezárva.")
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.ID, "ContentPlaceHolder1_NovszerGridView")
                )
            )

    except Exception as e:
        print(f"Hiba az eredmény táblázat kezelésekor: {str(e)}")


def download_pdfs(driver):
    try:
        pdf_links = driver.find_elements(
            By.XPATH,
            "//a[contains(@id, 'ContentPlaceHolder1_InfoNovszerControl_HyperLink_')]",
        )
        downloaded_files = set(os.listdir(download_directory))

        for i, link in enumerate(pdf_links):
            pdf_url = link.get_attribute("href")
            pdf_filename = os.path.basename(pdf_url)

            if pdf_filename in downloaded_files:
                print(f"PDF már letöltve: {pdf_filename}")
                continue

            print(f"PDF {i + 1} letöltve: {pdf_url}")
            link.click()
            wait_for_downloads(download_directory)

    except Exception as e:
        print(f"Hiba a PDF-ek letöltésekor: {str(e)}")


def wait_for_downloads(download_path, timeout=60):
    seconds = 0
    while seconds < timeout:
        if any(
            filename.endswith(".pdf") or filename.endswith(".crdownload")
            for filename in os.listdir(download_path)
        ):
            time.sleep(2)
            return True
        time.sleep(1)
        seconds += 1
    return False


def clear_filters(driver):
    try:
        clear_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.NAME, "ctl00$ContentPlaceHolder1$CancelButton")
            )
        )
        clear_button.click()
        print("Feltételek törölve.")
        time.sleep(3)
        driver.refresh()
        time.sleep(5)

    except Exception as e:
        print(f"Hiba a feltételek törlésekor: {str(e)}")


def restart_browser(driver, chrome_driver_path, chrome_options):
    stop_browser(driver)
    new_driver = start_browser(chrome_driver_path, chrome_options)
    open_website(new_driver)
    time.sleep(5)
    return new_driver


driver = start_browser(chrome_driver_path, chrome_options)
enter_fullscreen(driver)  # Itt belépünk a teljes képernyős módba
open_website(driver)

for index in range(630):
    print(f"Feldolgozás: {index + 1}. hatóanyag")
    select_active_ingredient(driver, index)
    click_search_button(driver)
    process_search_results(driver)
    clear_filters(driver)
    print(f"{index + 1}. hatóanyag feldolgozva.")

    if (index + 1) % 10 == 0:
        print("WebDriver újraindítása...")
        driver = restart_browser(driver, chrome_driver_path, chrome_options)

stop_browser(driver)
