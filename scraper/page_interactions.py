from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import scroll_to_element, wait_for_downloads
import time

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

def select_active_ingredient(driver, index, max_retries=3):
    for attempt in range(max_retries):
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
            return

        except Exception as e:
            print(f"Hiba a hatóanyag kiválasztásakor (Attempt {attempt + 1}): {str(e)}")
            if attempt == max_retries - 1:
                print("Max retries reached. Skipping ingredient selection.")
                return

        time.sleep(3)

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
        num_results = int("".join(filter(str.isdigit, result_text)))

        return num_results
    except Exception as e:
        print(f"Hiba a találatok számának lekérdezésekor: {str(e)}")
        return 0

def click_search_button(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located(
                (
                    By.ID,
                    "ContentPlaceHolder1_HatoanyagMultiSelectPopupControl_MultiSelectPopupUserControlPanelTable",
                )
            )
        )

        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.NAME, "ctl00$ContentPlaceHolder1$KeresesButton")
            )
        )
        search_button.click()
        print("Keresés gombra kattintva.")
        time.sleep(5)
    except Exception as e:
        print(f"Hiba a keresés végrehajtásakor: {str(e)}")

def clear_filters(driver, max_retries=3):
    for attempt in range(max_retries):
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
            return
        except Exception as e:
            print(f"Hiba a szűrők törlésekor (Attempt {attempt + 1}): {str(e)}")
            if attempt == max_retries - 1:
                print("Max retries reached. Skipping filter clearing.")
                return
