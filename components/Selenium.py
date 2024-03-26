from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


def selenium_scraping(url: str) -> str:
    webdriver_path = "..\RAG_bot\geckodriver.exe"

    # binary_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    firefox_options = Options()
    # firefox_options.binary_location = binary_path
    firefox_options.headless = True

    service = Service(executable_path=webdriver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.get(url)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))

    visible_text = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()
    return visible_text
