from .page_interactions import (
    open_website,
    select_active_ingredient,
    click_search_button,
    clear_filters,
    get_number_of_results,
)
from .browser_setup import start_browser, stop_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import scroll_to_element, wait_for_downloads
import time
import os


DOWNLOAD_DICTIONARY = "D:\\Prog\\Python\\Erik\\Hatóanyagok"


def get_number_of_rows(driver):
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

        num_rows = int("".join(filter(str.isdigit, result_text)))

        print(f"Találatok száma: {num_rows}")
        return num_rows

    except Exception as e:
        print(f"Hiba a találatok számának lekérdezésekor: {str(e)}")
        return 0


def process_search_results(driver):
    try:
        num_rows = get_number_of_rows(driver)
        if num_rows == 0:
            print("Nincs találat.")
            return

        for i in range(num_rows):
            row_selector = f"Select${i}"
            row_link_xpath = f'//a[contains(@href, "{row_selector}")]'

            row_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, row_link_xpath))
            )

            scroll_to_element(driver, row_link)
            print(f"{i + 1}. sor feldolgozása...")
            row_link.click()
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
        downloaded_files = set(os.listdir(DOWNLOAD_DICTIONARY))

        for i, link in enumerate(pdf_links):
            pdf_url = link.get_attribute("href")
            pdf_filename = os.path.basename(pdf_url)

            if pdf_filename in downloaded_files:
                print(f"PDF már letöltve: {pdf_filename}")
                continue

            print(f"PDF {i + 1} letöltve: {pdf_url}")
            link.click()
            wait_for_downloads(DOWNLOAD_DICTIONARY)

    except Exception as e:
        print(f"Hiba a PDF-ek letöltésekor: {str(e)}")
