# import time
# import logging
# from selenium import webdriver
# from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

# # Configure logging for better debugging and traceability
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# # Initialize WebDriver with a reusable function
# def init_driver():
#     # Adjust options if needed (e.g., headless mode)
#     driver = webdriver.Chrome()
#     return driver

# def close_popup(driver, popup_class, timeout=10):
#     """
#     Closes a popup if present.
#     """
#     try:
#         popup = WebDriverWait(driver, timeout).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, popup_class))
#         )
#         popup.click()
#         logging.info("Popup closed.")
#     except WebDriverException as e:
#         logging.error(f"Failed to close popup: {e}")

# def click_link(driver, link_text, timeout=10):
#     """
#     Clicks a link on the page.
#     """
#     try:
#         link = WebDriverWait(driver, timeout).until(
#             EC.element_to_be_clickable((By.LINK_TEXT, link_text))
#         )
#         link.click()
#         logging.info(f"Navigated to {link_text}.")
#         time.sleep(5)  # Wait for the new page to load
#     except WebDriverException as e:
#         logging.error(f"Failed to navigate to {link_text}: {e}")

# def capture_page_source(driver, file_name, target_identifier, identifier_type="class", timeout=10):
#     """
#     Captures HTML source of the current page.
#     """
#     for attempt in range(3):  # Retry mechanism for stale elements
#         try:
#             # Wait until the target section is present based on the identifier type (id or class)
#             if identifier_type == "id":
#                 WebDriverWait(driver, timeout).until(
#                     EC.presence_of_element_located((By.ID, target_identifier))
#                 )
#             elif identifier_type == "class":
#                 WebDriverWait(driver, timeout).until(
#                     EC.presence_of_element_located((By.CLASS_NAME, target_identifier))
#                 )

#             # Get the page source
#             html_source = driver.page_source

#             # Save the HTML source to a file
#             with open(file_name, "w", encoding="utf-8") as file:
#                 file.write(html_source)
#             logging.info(f"HTML source saved to {file_name}.")
#             return

#         except StaleElementReferenceException as e:
#             logging.warning("Stale element reference exception caught, retrying...")
#         except WebDriverException as e:
#             logging.error(f"Failed to capture the page source: {e}")
#             # Take a screenshot for further debugging
#             screenshot_file = "error_screenshot.png"
#             driver.save_screenshot(screenshot_file)
#             logging.info(f"Screenshot saved to {screenshot_file}")
#             break

#     logging.error("Failed to capture page source after retries.")

# def scrape_page(url, popup_class=None, link_text=None, target_identifier=None, identifier_type="class", file_name="page_source.html"):
#     """
#     Reusable function to scrape any page.
#     """
#     driver = init_driver()

#     try:
#         driver.get(url)
#         logging.info(f"Opened {url}.")

#         # Allow the page to load
#         time.sleep(5)
#         logging.info("Page loaded.")

#         # Close popup if popup class is provided
#         if popup_class:
#             close_popup(driver, popup_class)

#         # Click link if link text is provided
#         if link_text:
#             click_link(driver, link_text)

#         # Capture page source if target identifier is provided
#         if target_identifier:
#             capture_page_source(driver, file_name, target_identifier, identifier_type)

#     except WebDriverException as e:
#         logging.error(f"An error occurred: {e}")
#     finally:
#         driver.quit()
#         logging.info("WebDriver closed.")

# # Example Usage:
# scrape_page(
#     url="https://www.doordash.com/store/taku-sando-brooklyn-25320680/",      
#     target_identifier="order-online-products",
#     identifier_type="class",
#     file_name="taku_sando_order_online_page_source.html"
# ) 

from selenium import webdriver
import time

# Initialize WebDriver

def init_driver():
    driver = webdriver.Chrome()
    return driver

# Function to capture HTML source of the current page
def capture_page_source(driver, file_name):
    html_source = driver.page_source
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_source)
    print(f"HTML source saved to {file_name}.")

# Main function to open the page and save the HTML source
def scrape_page(url, file_name="page_source.html"):
    driver = init_driver()
    try:
        driver.get(url)
        print(f"Opened {url}.")
        time.sleep(5)  # Allow the page to load
        capture_page_source(driver, file_name)
    finally:
        driver.quit()
        print("WebDriver closed.")

# Example Usage
scrape_page(
    url="https://www.doordash.com/store/taku-sando-brooklyn-25320680/",
    file_name="doordash_taku_sando_order_online_page_source.html"
)