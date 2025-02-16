from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ChromeOptions, Chrome
import time
import os
from webdriver_manager.chrome import ChromeDriverManager
default_path = "http://localhost"
#default_path = "https://demo.docassemble.org"
default_wait_seconds = 0
use_firefox = False
use_phantomjs = False
use_headless_chrome = True

class MyFirefox(webdriver.Firefox):
    def loaded(self):
        try:
            return 0 == self.execute_script("return jQuery.active")
        except WebDriverException:
            pass

    def wait_for_it(self):
        WebDriverWait(self, 20).until(MyFirefox.loaded, "Timeout waiting for page to load")

    def text_present(self, text):
        try:
            body = self.find_element_by_tag_name("body")
        except NoSuchElementException:
            return False
        return text in body.text

class MyPhantomJS(webdriver.PhantomJS):
    def loaded(self):
        try:
            return 0 == self.execute_script("return jQuery.active")
        except WebDriverException:
            pass

    def wait_for_it(self):
        WebDriverWait(self, 20).until(MyPhantomJS.loaded, "Timeout waiting for page to load")

    def text_present(self, text):
        try:
            body = self.find_element_by_tag_name("body")
        except NoSuchElementException:
            return False
        return text in body.text

class MyChrome(Chrome):
    def loaded(self):
        try:
            return 0 == self.execute_script("return jQuery.active")
        except WebDriverException:
            pass

    def wait_for_it(self):
        WebDriverWait(self, 20).until(MyChrome.loaded, "Timeout waiting for page to load")

    def text_present(self, text):
        try:
            body = self.find_element_by_tag_name("body")
        except NoSuchElementException:
            return False
        return text in body.text

def before_all(context):
    context.screenshot_number = 0
    context.screenshot_folder = None
    context.headless = False
    if use_firefox:
        context.browser = MyFirefox()
        context.browser.set_window_size(450, 1200)
        context.browser.set_window_position(0, 0)
        #context.browser.maximize_window()
    elif use_phantomjs:
        context.browser = MyPhantomJS()
    elif use_headless_chrome:
        context.headless = True
        options = ChromeOptions()
        options.add_argument("--window-size=1005,9999")
        options.add_argument("--headless");
        context.browser = MyChrome(ChromeDriverManager().install(), chrome_options=options)
    else:
        options = ChromeOptions()
        options.add_argument("--start-maximized");
        context.browser = MyChrome(ChromeDriverManager().install(), chrome_options=options)
    context.da_path = default_path
    context.wait_seconds = default_wait_seconds

def after_all(context):
    time.sleep(2)
    #print("Total %d of %d scenarios passed!" % ( total.scenarios_ran, total.scenarios_passed ))
    context.browser.quit()
