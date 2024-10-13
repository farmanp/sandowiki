from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# URL of the page to scrape
url = 'https://www.ichibansando.com/home'

# Open the page with Selenium
driver.get(url)

# Wait for the page to fully load
time.sleep(5)

# Close the popup (if needed)
try:
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'leadform-popup-close'))
    )
    close_button.click()
    print("Popup closed.")
except Exception as e:
    print("No popup or failed to close it:", e)

# Wait a bit to ensure the popup is closed
time.sleep(2)

# Now click on the "Order Online" link
try:
    order_online_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Order Online'))
    )
    order_online_link.click()
    print("Navigated to Order Online.")
    
    # Wait for the Order Online page to load
    time.sleep(5)
    
except Exception as e:
    print(f"Failed to navigate to Order Online: {e}")

# Capture the HTML source of the Order Online page
try:
    # Wait until the order online products section is present
    order_products_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'order-online-products'))
    )

    # Get the page source once the products are loaded
    html_source = driver.page_source

    # Print the HTML source of the "Order Online" page
    print(html_source)

    # Optionally, save the HTML source to a file for further inspection
    with open("ichiban_sando_order_online_page_source.html", "w", encoding="utf-8") as file:
        file.write(html_source)
    print("HTML source of the 'Order Online' page saved to 'order_online_page_source.html'.")

except Exception as e:
    print(f"Failed to capture the 'Order Online' page source: {e}")

# Close the WebDriver
driver.quit()
