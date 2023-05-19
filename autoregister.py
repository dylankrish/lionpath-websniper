# Enable Raised Exceptions in vscode for debugging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sys import platform
import os
import time
import datetime
import hashlib
import pyotp
from selenium.webdriver.chrome.service import Service
from config import *

def autoregister():
    try:
        if platform == "linux":
            # Linux
            print('Running on Linux ' + os.uname().machine)
            chromeoptions = webdriver.ChromeOptions()
            if useBrave:
                chromeoptions.binary_location = '/usr/bin/brave'
            if darkMode:
                chromeoptions.add_argument("--force-dark-mode")
                chromeoptions.add_argument("--enable-features=WebContentsForceDark")
            # enable hardware acceleration on linux
            chromeoptions.add_argument("--enable-features=VaapiVideoEncoder,VaapiVideoDecoder")
            chromeoptions.add_argument("--enable-gpu-rasterization")
            driver = webdriver.Chrome(options=chromeoptions)
        elif platform == "darwin":
            # MacOS
            print('Running on macOS ' + os.uname().machine)
            chromeoptions = webdriver.ChromeOptions()
            if useBrave:
                chromeoptions.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            if darkMode:
                chromeoptions.add_argument("--force-dark-mode")
                chromeoptions.add_argument("--enable-features=WebContentsForceDark")    
            driver = webdriver.Chrome(options=chromeoptions)
        elif platform == "win32":
            # Windows
            print('Running on Windows ' + os.uname().machine)
            chromeoptions = webdriver.ChromeOptions()
            if darkMode:
                chromeoptions.add_argument("--force-dark-mode")
                chromeoptions.add_argument("--enable-features=WebContentsForceDark")
            if useBrave:
                chromeoptions.binary_location = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                driver = webdriver.Chrome(options=chromeoptions)
            elif useEdge:
                driver = webdriver.Edge(options=chromeoptions)
            else:
                driver = webdriver.Chrome(options=chromeoptions)
        else:
            # may add BSD support in the future
            print(platform + ' is not supported.')

        # we need to maximize the window so that all elements are visible
        driver.maximize_window()
        lionpath = "https://lionpath.psu.edu/"
        enrollmentPage = "https://www.lionpath.psu.edu/psc/CSPRD/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID%3aPTPPNAVCOL&scname=PE_PT_NVF_ENROLLMENT&PanelCollapsible=Y&PTPPB_GROUPLET_ID=PE_PT_NVI_ENROLLMENT&CRefName=PE_PT_NVI_ENROLLMENT&AJAXTransfer=y"
        driver.get(enrollmentPage)

        # TODO: Encrypt username, password and totp secret
        # grab username from file
        usernameFile = open('username.txt', 'r')
        username = usernameFile.read()
        usernameFile.close()

        # get password from file
        passwordFile = open('password.txt', 'r')
        password = passwordFile.read()
        passwordFile.close()

        if useTOTP:
            # get totp token from file
            totpfile = open('totpsecret.txt', 'r')
            totpsecret = totpfile.read()
            totpfile.close()

        # Login

        # Wait for login page
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))

        # Type username
        driver.find_element(By.NAME, 'loginfmt').send_keys(username)

        # Wait for password page
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'passwd')))

        # Type password
        driver.find_element(By.NAME, 'passwd').send_keys(password)
        time.sleep(1)

        # Send enter key
        driver.find_element(By.NAME, 'passwd').send_keys(u'\ue007')

        if useTOTP:
            # Wait for totp page
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'otc')))

            # Create a TOTP object with the given secret
            totp = pyotp.TOTP(totpsecret, digits=6, digest=hashlib.sha1)

            # Get the current TOTP code
            totpcode = totp.now()

            # Type totp code
            driver.find_element(By.NAME, 'otc').send_keys(totpcode)
            # Send enter key
            driver.find_element(By.NAME, 'otc').send_keys(u'\ue007')

            # If the expected verification code is not entered, we need to try a different one
            # check for id 'ViewDetails' or the login page
            while True:
                # if the view details button is visible, we are on the login page
                if driver.find_elements(By.ID, 'ViewDetails'):
                    raise Exception('You didn\'t enter an expected verification code. Please try again.')
                # if the view details button is not visible, we are on the enrollment page
                elif driver.find_elements(By.ID, 'main_target_win0'):
                    break

        # Wait for the iframe to become visible
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'main_target_win0')))

        # Switch to the iframe
        driver.switch_to.frame(driver.find_element(By.ID, 'main_target_win0'))

        # TODO: automatically detect each button
        # we can automatically detect the buttons by using the id's and x
        # we can create a list of buttons and iterate through them
        radioList = []
        while True:
            try:
                radioList.append(driver.find_element(By.ID, 'SSR_DUMMY_RECV1$sels$' + str(len(radioList)) + '$$0'))
            except:
                break
        # pick the radio button using the enrollnum
        ActionChains(driver).click(radioList[radnum - 1]).perform()
        # Radio buttons for each semester
        # radio1 = driver.find_element(By.ID, 'SSR_DUMMY_RECV1$sels$0$$0')
        # radio2 = driver.find_element(By.ID, 'SSR_DUMMY_RECV1$sels$1$$0')
        # radio3 = driver.find_element(By.ID, 'SSR_DUMMY_RECV1$sels$2$$0')

        # pick the radio button using the enrollnum
        # if radnum == 1:
        #     radiobtn = radio1
        # elif radnum == 2:
        #     radiobtn = radio2
        # elif radnum == 3:
        #     radiobtn = radio3

        # Select the radio button by clicking on it with actionchains
        # ActionChains(driver).click(radiobtn).perform()


        # Click continue
        continueButton = driver.find_element(By.ID, 'DERIVED_SSS_SCT_SSR_PB_GO')
        continueButton.click()

        # Wait for the loading screen to go away
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))

        # get out of the iframe
        driver.switch_to.default_content()

        # Go to the shopping cart
        # Method 1: Click the shopping cart button
        # shoppingCartButton = driver.find_element(By.XPATH, '//*[@id="win1divPTGP_STEP_DVW_PTGP_STEP_BTN_GB$4"]')
        # ActionChains(driver).click(shoppingCartButton).perform()
        # Method 2: Go directly to the shopping cart url
        driver.get('https://www.lionpath.psu.edu/psc/CSPRD_newwin/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true')

        # wait for the loading screen to go away
        # (only needed if we use method 1)
        # WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))

        # Method 1: click the enroll button to unglitch the page
        # enrollButton = driver.find_element(By.ID, 'DERIVED_SSR_FL_SSR_ENROLL_FL')
        # ActionChains(driver).click(enrollButton).perform()
        # WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
        # time.sleep(0.1)

        # Method 2: refresh to unglitch the page
        # refresh the page
        driver.refresh()

        if datetime.datetime.now().hour != 0 and waitUntil12AM:
            print('Waiting for 12AM')
            # Wait until 12AM
            while datetime.datetime.now().hour != 0:
                # check if the "Your session is about to expire" popup is visible
                # id="#ICOK"
                # if it is, run javascript:pingServer("https://www.lionpath.psu.edu/psc/CSPRD_2/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true");setupTimeout2();closeLastModal();
                try: 
                    driver.find_element(By.ID, '#ICOK').is_displayed()
                    driver.execute_script('pingServer("https://www.lionpath.psu.edu/psc/CSPRD_2/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true");setupTimeout2();closeLastModal();')
                except:
                    pass
                # check if the "Your session has expired" popup is visible
                # id="ps_loginmessagelarge"
                # if it is, raise an exception
                try:
                    driver.find_element(By.XPATH, '//*[@id="login"]/div/div/div/p[4]/a').is_displayed()
                    raise Exception('Your session has expired. Please log in again.')
                except:
                    pass
                # wait 1 second
                time.sleep(0.1)
                # refresh the page

        # refresh the page to reveal the enroll button
        driver.refresh()

        # TODO: attempt to check if the enroll button is visible, otherwise refresh the page
        while not driver.find_element(By.XPATH, '//*[@id="DERIVED_SSR_FL_SSR_ENROLL_FL"]').is_displayed():
            # refresh the page
            print('Waiting for enroll button to appear')
            driver.refresh()

        # see how many checkboxes there are
        # checkboxes are in the format DERIVED_REGFRM1_SSR_SELECT$x where x is the number of the checkbox starting from 0
        checkboxList = []
        while True:
            try:
                checkboxList.append(driver.find_element(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(len(checkboxList))))
            except:
                break
        # checkboxes are in the format DERIVED_REGFRM1_SSR_SELECT$x where x is the number of the checkbox starting from 0 and going to enrollnum - 1
        # for i in range(enrollnum):
        #     # checkbox = driver.find_element(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(i))
        #     # test using xpath rather than id
        #     checkbox = driver.find_element(By.XPATH, '//*[@id="DERIVED_REGFRM1_SSR_SELECT$' + str(i) + '"]')
        #     ActionChains(driver).click(checkbox).perform()
        print(checkboxList)
        # click all the checkboxes in the list
        for i in range(len(checkboxList)):
            ActionChains(driver).click(checkboxList[i - 1]).perform()

        # Hit the enroll button
        # enrollButton = driver.find_element(By.ID, 'DERIVED_SSR_FL_SSR_ENROLL_FL')
        # ActionChains(driver).click(enrollButton).perform()
        # Run the javascript to click the enroll button
        driver.execute_script("javascript:submitAction_win2(document.win2,'DERIVED_SSR_FL_SSR_ENROLL_FL');")

        # Wait for yes button to appear
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="#ICYes"]')))

        # Run the javascript to click the yes button
        driver.execute_script("oParentWin.submitAction_win2(oParentWin.document.win2, '#ICYes');closeMsg(null,modId);")

        # Check if any classes failed to enroll
        # success = win0divDERIVED_REGFRM1_DESCRLONG$x where x is a number
        # fail = win2divDERIVED_REGFRM1_DESCRLONG$x where x is a number

        # Wait for the loading screen to go away
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win2')))

        # Experimental: check if the fail ID is displayed
        for i in range(enrollnum):
            classObj = driver.find_element(By.ID, 'DERIVED_REGFRM1_DESCRLONG$' + str(i))
            className = classObj.text
            # check to see if the class was fail or success
            # if the fail element exists
            if driver.find_elements(By.ID, 'win2divDERIVED_REGFRM1_DESCRLONG$' + str(i)):
                # we also need to get the ps-htmlarea div contained within id win2divDERIVED_REGFRM1_SS_MESSAGE_LONG$1
                divHTML = driver.find_element(By.ID, 'win2divDERIVED_REGFRM1_SS_MESSAGE_LONG$' + str(i)).get_attribute("innerHTML")
                # for the fail message, we need to get rid of the top 2 lines and the last 2 lines, and convert the index 0 to a string
                failMessage = divHTML.splitlines()[2:-2][0]
                # print the class that failed to enroll by checking the text of the element
                print("\"" + className + "\" failed to enroll")
                if sendDiscordNotification:
                    import requests
                    # timestamp
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                    # send a discord notification
                    data = {
                        "username" : "LionPath Sniper",
                    }
                    data["embeds"] = [
                        {
                            "title" : ":x: **" + className + "**",
                            "description" : "**" + failMessage + "**\n\n" + str(timestamp),
                            "color" : 0xff0000
                        }
                    ]
                    requests.post(discordWebhookURL, json = data)
            # else if the success element exists
            elif driver.find_elements(By.ID, 'win0divDERIVED_REGFRM1_DESCRLONG$' + str(i)):
                divHTML = driver.find_element(By.ID, 'win0divDERIVED_REGFRM1_SS_MESSAGE_LONG$' + str(i)).get_attribute("innerHTML")
                # for the success message, we need to get rid of the top 2 lines and the last 2 lines, and convert the index 0 to a string
                successMessage = divHTML.splitlines()[2:-2][0]
                print("\"" + className + "\" enrolled successfully")
                if sendDiscordNotification:
                    import requests
                    # timestamp
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                    # send a discord notification
                    data = {
                        "username" : "LionPath Sniper",
                    }
                    data["embeds"] = [
                        {
                            "title" : ":heavy_check_mark: **" + className + "**",
                            "description" : "**" + successMessage + "**\n\n" + str(timestamp),
                            "color" : 0x00ff00
                        }
                    ]
                    requests.post(discordWebhookURL, json = data)

        driver.close

        input('Finished. Press enter to close the program.')
    except Exception as e:
        print(e)
        driver.close()
        autoregister()

# function to run the autoregister() function at 11:57 PM
def waitTimer():
    while True:
        time.sleep(1)
        if datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 57:
            autoregister()
                

if __name__ == '__main__':
    if waitTimerEnable:
        waitTimer()
    else:
        autoregister()