# coding=utf-8
import config
import logging
from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class TrendyolTest:
    def __init__(self):
        self.userName = config.userData['mail']
        self.password = config.userData['pass']
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    def runWebDriver(self, driver):
        self.driver = driver
        if self.driver == config.chromeDriver:
            self.driver = webdriver.Chrome(executable_path=config.chromeExecutablePath)
            self.wait = WebDriverWait(self.driver, 20)

        elif self.driver == config.firefoxDriver:
            self.driver = webdriver.Firefox(executable_path=config.firefoxExecutablePath)
            self.wait = WebDriverWait(self.driver, 20)
            self.driver.maximize_window()


        else:
            logging.info("Config value error, no browser selected to be run.")

        return driver

    # As default base url in config file
    def goUrl(self, url):
        try:
            # Go base url and close the starting page popup.
            self.driver.get(url)
            self.checkCurrentUrl(url + '/')
            logging.info('Gone Url')
        except:
            logging.warning('Fail Gone')
            self.finishCase()

    def closePopUp(self):
        popupClose = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.fancybox-close')))
        popupClose.click()

    # Wait for loading last element
    def waitForLoadPage(self):
        time.sleep(2)
        self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'KVK ve Gizlilik Politikası')))

    # Checking current url equality
    def checkCurrentUrl(self, currentUrl):
        self.currentUrl = currentUrl
        if str(self.currentUrl) == str(self.driver.current_url):
            return True
        else:
            logging.warning('Url equality is not provided')
            return False

    # Login step
    def loginCase(self):

        loginContainer = self.wait.until(EC.visibility_of_element_located((By.ID, 'not-logged-in-container')))

        loginHover = ActionChains(self.driver).move_to_element(loginContainer)
        loginHover.perform()

        loginButton = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.account-button.login')))
        loginButton.click()

        loginMail = self.wait.until(EC.visibility_of_element_located((By.ID, 'email')))
        loginMail.send_keys(config.userData['mail'])

        loginPass = self.wait.until(EC.visibility_of_element_located((By.ID, 'password')))
        loginPass.send_keys(config.userData['pass'])

        loginSubmit = self.wait.until(EC.visibility_of_element_located((By.ID, 'loginSubmit')))
        loginSubmit.click()

    # Checking status code for images
    def checkStatusImageBoutique(self, cssSelector):
        self.waitForLoadPage()

        boutiqueElements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, cssSelector)))

        for i in boutiqueElements:
            self.requestImage = requests.get(i.get_attribute('src'))
            try:
                assert self.requestImage.status_code == 200
            except:
                logging.warning('FAIL - Status Code : {}'.format(self.requestImage.status_code))

    # Checking all tabs and image load status
    def checkAllTabs(self):
        self.waitForLoadPage()

        tabLength = int(len(self.driver.find_elements_by_css_selector('#main-menu > ul > li')))

        for i in range(tabLength):
            elems = self.driver.find_elements_by_css_selector('#main-menu > ul > li')[i]
            elems.click()

            # Checking page loads for all tabs
            self.waitForLoadPage()

            # Checking status and url equalities
            self.checkStatusImageBoutique('img.bigBoutiqueImage')
            self.checkCurrentUrl(config.baseUrl + config.tabPaths[0])
            config.tabPaths.pop(0)

    #Take the url in element
    def takeUrl(self, cssSelector):
        randomBoutique = self.driver.find_element_by_css_selector(cssSelector)
        self.urlPathBoutique = str(randomBoutique.get_attribute('href'))
        randomBoutique.click()
        self.checkCurrentUrl(self.urlPathBoutique)

    def checkRandomBoutiqueImages(self):
        self.waitForLoadPage()
        self.takeUrl('.boutique-large-list-tmpl-result.row > div:first-child > div.butik-large-image > a')
        self.checkStatusImageBoutique('.prc-picture')

    # Adding product in basket
    def addProductInBasket(self):
        self.waitForLoadPage()
        self.takeUrl('#root > div > ul > li:nth-child(1) > div > a')
        self.waitForLoadPage()
        self.driver.find_element_by_id('addToBasketButton').click()
        # Choose variant

        if self.driver.find_element_by_css_selector('.product-detail-overlay').is_displayed():
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-original-index="1"]'))).click()

    # Quit driver
    def finishCase(self):
        try:
            self.driver.quit()
            logging.info('Success for all tests')
        except:
            logging.warning('Webdriver could not be closed')
