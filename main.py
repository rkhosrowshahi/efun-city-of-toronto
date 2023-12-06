import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver import Keys
from webdriver_manager.chrome import ChromeDriverManager
from getpass import getpass
from datetime import datetime
import pytz

def welcomeBanner():
    print("==========================================================================================")
    print("|                        Course Registration Bot in City of Toronto                      |")
    print("==========================================================================================")

def getDriver():
    print("\nInitializing/Checking webdriver....\n")
    # Initializes necessary Chrome driver for Selenium to use:
    global driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver.maximize_window
    driver.close()
        
def register(url, driver, courses, user_id):
    driver.get(url)
    
    barcode_search_btn = driver.find_element(By.ID, "barcode-search-icon")
    for c in courses:
        barcode_input = driver.find_element(By.ID, "cbarcode")
        barcode_input.clear()
        barcode_input = driver.find_element(By.ID, "cbarcode")
        barcode_input.send_keys(str(c))
        barcode_search_btn.click()
        add_to_cart_btn = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='course-details-course-info']//a[@title='Add To My Cart']"))
        )
        
        add_to_cart_btn.click()
        select_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='ClientID']"))
        )
        dropdown = Select(select_element)
        dropdown.select_by_index(user_id)

        WebDriverWait(driver, 50).until(
        EC.visibility_of_element_located(locator=(By.XPATH, "//span[@id='cart-subtotal']"))
        )   

        continue_btn = driver.find_element(By.XPATH, "//input[@id='cancel']")
        continue_btn.click()
        

    print("\nCourses registered successfully!\n")

    my_cart_btn = driver.find_element(By.XPATH, "//ul[@id='cart-preview']//a")
    my_cart_btn.click()
    
    checkout_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Go to Checkout']"))
    )
    checkout_btn.click()

    while(True):
        pass
    

def login(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver.maximize_window
    

    while True:
        driver.get(url)
        if EC.visibility_of_element_located((By.XPATH, '//div[@id="toolbar-login"]//a[@class="focus-parent ajax-request need-focus-pageobject"]')):
            break

    print("\nRegistering for courses...\n")
    logIn_btn = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="toolbar-login"]//a[@class="focus-parent ajax-request need-focus-pageobject"]'))
        )
    
    logIn_btn.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ClientBarcode")) #This is a dummy element
    )
    client_number_el = driver.find_element(By.ID, "ClientBarcode")
    client_number_el.send_keys(client_number)
    account_pin_el = driver.find_element(By.ID, "AccountPIN")
    account_pin_el.send_keys(PIN_number)
    submitButton = driver.find_element(By.XPATH, "//input[@value='Log in']")
    submitButton.click()

    return driver

def main():
    # Following urls are specified for the city of Toronto
    login_url = "https://efun.toronto.ca/torontofun/start/start.asp"
    register_url = "https://efun.toronto.ca/torontofun/Activities/ActivitiesAdvSearch.asp"

    welcomeBanner()
    getDriver()
    global courses, client_number, PIN_number, semester, PRN, num_of_courses

    # Defining courses barcode list:
    courses = [4318892, 4227049]
    # Getting user-inputed data that will be inserted into login:
    client_number=None
    PIN_number=None
    user_id = 1

    if client_number is None and PIN_number is None:
        print("\nPlease enter the necessary information to login...\n")
        client_number = input("What is your client number?: ").upper()[:9]
        PIN_number = getpass("What is your account pin?: ")
    else:
        print("\nCredentials look good!, Logging in...\n")

    # Change the timezone
    tz = pytz.timezone("US/Eastern")
    # Change the time to wait in the order of YYYY, MM, DD, HH, Min, Sec, MiliSec
    ts1 = datetime(2023, 12, 6, 7, 4, 1, 100, tzinfo=tz)
    while ts1.timestamp() >= datetime.now(tz).timestamp():
        print(ts1.timestamp() - datetime.now(tz).timestamp(), "is left")
    print("\nTime is reached...Program starting...\n")    
    driver = login(login_url)
    print("\nLogged in succesfully...\nRegistering courses...\n")
    register(url=register_url, driver=driver, courses=courses, user_id=user_id)
    print("Courses registered successfully!")

if __name__ == '__main__':
    main()