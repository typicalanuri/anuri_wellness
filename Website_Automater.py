from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # Go to Google
    driver.get("https://www.google.com")

    # Accept cookies / consent if the popup appears
    try:
        consent_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I agree') or contains(., 'Accept all')]"))
        )
        consent_btn.click()
    except:
        pass  # no consent popup

    # Locate the search box
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # Enter search query
    query = "GitHub Careers"
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load and show the link
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a/h3"))
    )

    # Click the first result (you can refine to click a specific domain)
    results[0].click()

    # Pause to see the new page
    time.sleep(5)

finally:
    driver.quit()