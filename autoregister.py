# TODO: Create functions for each step and allow disabling of certain steps
# TODO: Clean up code comments
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sys import platform
import time
import pyautogui

from selenium.webdriver.chrome.service import Service

chromeoptions = webdriver.ChromeOptions()

# TODO: Add support for Windows
# TODO: Add support for other browsers
if platform == "linux" or platform == "linux2":
    # Linux
    print('Linux')
    chromedriver = "/usr/bin/chromedriver"
    chromeoptions.binary_location = '/usr/lib/brave-bin/brave'
    chromeoptions.add_argument("--enable-features=VaapiVideoEncoder,VaapiVideoDecoder")
    chromeoptions.add_argument("--enable-gpu-rasterization")
    # chromeoptions.add_argument("--user-data-dir=/home/dylank/.config/BraveSoftware/Brave-Browser")
elif platform == "darwin":
    # MacOS
    print('macOS')
    chromedriver = "/opt/homebrew/bin/chromedriver"
    chromeoptions.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    # chromeoptions.add_argument("--user-data-dir=/Users/dylank/Library/Application Support/BraveSoftware/Brave-Browser")
else:
    print('Unsupported operating system')


driver = webdriver.Chrome(service=Service(chromedriver), options=chromeoptions)
lionpath = "https://lionpath.psu.edu/"
driver.get(lionpath)

# grab username from file
usernameFile = open('username.txt', 'r')
username = usernameFile.read()
usernameFile.close()

# get password from file lmao
passwordFile = open('password.txt', 'r')
password = passwordFile.read()
passwordFile.close()

# Login

# Wait for login page
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))

# Type username
driver.find_element(By.NAME, 'loginfmt').send_keys(username)

# Click next
driver.find_element(By.ID, 'idSIButton9').click

# Wait
time.sleep(1)

# Type password
driver.find_element(By.NAME, 'passwd').send_keys(password)

# Wait for duo auth to show up
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'device')))

# Select iOS
duoSelect = Select(driver.find_element(By.NAME, 'device'))
duoSelect.select_by_visible_text('iOS')

# Send push
duoPush = driver.find_element(By.XPATH, '//*[@id="auth_methods"]/fieldset[1]/div[1]/button')
ActionChains(driver).click(duoPush).perform()
# duoPush.click

enrollmentBtnFound = False
while not enrollmentBtnFound:
    # If duo detects browser is out of date, click the skip button
    # this code doesn't fully work yet, since the skip button is not always there
    # if driver.find_elements(By.NAME, 'Skip'):
    if driver.find_elements(By.CSS_SELECTOR, 'body > div > div > div.base-main > div > div > div.navigation > div.nav-button.next.clickable > span'):
        skipButton = driver.find_element(By.CSS_SELECTOR, 'body > div > div > div.base-main > div > div > div.navigation > div.nav-button.next.clickable > span')
        ActionChains(driver).click(skipButton).perform()
        # driver.execute_script(document.querySelector("body > div > div > div.base-main > div > div > div.navigation > div.nav-button.next.clickable"))
    # else find the enrollment button
    elif driver.find_elements(By.ID, 'PE_UI020_BTNS_PE_GRID_BUTTON$1'):
        enrollmentBtnFound = True


# Wait until push accepted lionpath is loaded, we are waiting for the enrollment button
# WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.ID, 'PE_UI020_BTNS_PE_GRID_BUTTON$1')))


# input('Press enter to continue after logging in')

# driver.find_element(By.ID, "win0divPE_UI020_BTNS_PE_GRID_BUTTON$1")
# enrollment_button = driver.find_element(By.ID, "PE_UI020_BTNS_PE_GRID_BUTTON$span$1")
# enrollment_button = driver.find_element(By.NAME, "Enrollment")
# print(enrollment_button)
# enrollment_button.click
# enrollment_button.click

# hit the enrollment button

driver.execute_script("submitAction_win0(document.win0,'PE_UI020_BTNS_PE_GRID_BUTTON$1')")

# Wait until next page is loaded, specifically the shopping cart button
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="win1divPTGP_STEP_DVW_PTGP_STEP_BTN_GB$4"]')))



# Trying to hit shopping cart button
# driver.execute_script("cancelBubble(event);if (!top.ptgpPage.openCustomStepButton('PE_S201901181129161770441332')) top.ptgpPage.openUrlWithWarning(this.getAttribute('href'), 'top.ptgpPage.selectStep(\'PE_S201901181129161770441332\');', true);return false;)")
# driver.sleep fix this pls

time.sleep(4)
shoppingCartButton = driver.find_element(By.XPATH, '//*[@id="win1divPTGP_STEP_DVW_PTGP_STEP_BTN_GB$4"]')
ActionChains(driver).click(shoppingCartButton).perform()

time.sleep(3)

# TODO: add fall2023 support
# Semesters
spring2023 = driver.find_element(By.XPATH, '//*[@id="GRID_TERM_SRC5$0_row_1"]/td')

# Click current semester
semester = spring2023
ActionChains(driver).click(semester).perform()

time.sleep(1)

# Trying to hit shopping cart button
# driver.execute_script("cancelBubble(event);if (!top.ptgpPage.openCustomStepButton('PE_S201901181129161770441332')) top.ptgpPage.openUrlWithWarning(this.getAttribute('href'), 'top.ptgpPage.selectStep(\'PE_S201901181129161770441332\');', true);return false;)")
# driver.sleep fix this pls
# shoppingCartButton = driver.find_element(By.XPATH, '//*[@id="win2divPTGP_STEP_DVW_PTGP_STEP_BTN_GB$4"]')
ActionChains(driver).click(shoppingCartButton).perform()

input('Press enter to continue after going to enroll key')
time.sleep(1)

# Hit the enroll button

time.sleep(1)

driver.close
