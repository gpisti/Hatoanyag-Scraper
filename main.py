from scraper.browser_setup import start_browser, stop_browser
from scraper.page_interactions import (
    open_website,
    select_active_ingredient,
    click_search_button,
    clear_filters,
)
from scraper.scraper import process_search_results

if __name__ == "__main__":
    driver = start_browser()

    try:
        open_website(driver)
        for index in range(630):
            select_active_ingredient(driver, index)
            click_search_button(driver)
            process_search_results(driver)
            clear_filters(driver)
    finally:
        stop_browser(driver)
