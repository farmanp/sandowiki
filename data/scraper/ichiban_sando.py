from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
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

# Now scrape the products in the order online section
try:
    # Wait until the order online products section is present
    order_products_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'order-online-products'))
    )

    # Get the page source once the products are loaded
    html = driver.page_source

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all product items (children of class 'grid__item')
    product_items = soup.find_all('div', class_='item__card')

    # Extract information for each product
    for product in product_items:
        breakpoint()
        # Find the product name
        name_div = product.find('p', class_='text-component w-product-title')
        name = name_div.text.strip() if name_div else 'No name found'
        
        # Find the product description
        description_div = product.find('div', class_='item__description')
        description = description_div.text.strip() if description_div else 'No description found'

        # Find the price from the <span> element
        price_span = product.find('span', class_='text-component')
        price = price_span.text.strip() if price_span else 'No price found'

        # Print the product details
        print(f"Product: {name}\nDescription: {description}\nPrice: {price}\n")

except Exception as e:
    print(f"Failed to scrape products: {e}")

# Close the WebDriver
driver.quit()
