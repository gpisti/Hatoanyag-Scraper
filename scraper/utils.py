import time
import os


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


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
