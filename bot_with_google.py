import os
import time
import json
import random
import threading
import pandas as pd
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import warnings
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
import uuid
import os
import shutil

def generate_8_digit_uuid():
    uuid_str = str(uuid.uuid4())
    digit_uuid = ''.join(filter(str.isdigit, uuid_str))
    return digit_uuid[:8]  


class YouTubeBot:
    def __init__(self, max_duration, option, email, passw,r_email,ip,count,link,checker):
        self.max_duration = max_duration
        self.option = option
        self.email = email
        self.r_email=r_email
        self.passw = passw
        self.ip = ip
        self.driver = None
        self.count=count
        self.link=link
        self.checker=checker
        self.ss=None
    def setup_webdriver(self):
        chrome_driver_path = "chromedriver.exe"
        driver_path = "driver_folders"
        new_chrome_driver_name = f"chromedriver_{self.count}.exe"
        os.makedirs(driver_path, exist_ok=True)
        new_chrome_driver_path = os.path.join(driver_path, new_chrome_driver_name)
        if os.path.exists(new_chrome_driver_path):
            os.remove(new_chrome_driver_path)
        shutil.copyfile(chrome_driver_path, new_chrome_driver_path)

        chrome_binary_path = "Google\\Chrome\\Application\\chrome.exe"
        proxy_host = self.ip
        proxy_http_port = 50100
        proxy_socks5_port = 50101
        username = 'hatemeltorky10'
        password = 'ntaU6gaAet'
        
        # seleniumwire_options = {
        #     'proxy': {
        #         'http': f'http://{username}:{password}@{proxy_host}:{proxy_http_port}',
        #         'https': f'http://{username}:{password}@{proxy_host}:{proxy_http_port}',
        #         'socks5': f'socks5://{username}:{password}@{proxy_host}:{proxy_socks5_port}',
        #        'no_proxy': 'localhost,127.0.0.1',
        #         'verify_ssl': False,
        #         #'certs': 'ca.crt'  # Path to your certificate file
        #     },
        # }

        seleniumwire_options = {
            'proxy': {
                'no_proxy': 'localhost,127.0.0.1',  # Exclude localhost and 127.0.0.1 from proxy
                'verify_ssl': False,
                'use_system_proxy': True  # Use system proxy settings
            },
        }

        options = ChromeOptions()
        # options.add_experimental_option("excludeSwitches", ["disable-popup-blocking", "enable-automation"])
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")
        #options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-logging")

        options.binary_location = chrome_binary_path
        options.add_argument("--lang=en-US")
        #options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        service = Service(executable_path=new_chrome_driver_path)
        driver = Chrome(version_main=115,options=options,service=service, seleniumwire_options=seleniumwire_options)
        return driver

    
#https://www.youtube.com/watch?v=z15ftc_4XwY
    def save_cookies(self):
        cookies = self.driver.get_cookies()
        folder_name = 'cookies_folder'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_path = os.path.join(folder_name, f'cookies{self.count}.json')
        with open(file_path, 'w') as file:
            json.dump(cookies, file)
        print('New Cookies saved successfully')

#https://accounts.google.com/v3/signin/identifier?hl=en-gb&ifkv=ARZ0qKLhxlhs7w3QzfwM0Erx6kJrcIos3Yw8rKaHVK34Nyay5T7N1-KcfikBkEghvJZ-rZuD6mz8xA&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1710882900%3A1711315508393122&theme=mn&ddm=0
    def load_cookies(self):
        folder_name = 'cookies_folder'
        if not os.path.exists(folder_name):
            print('No cookies folder found')
            return

        cookies_file = f'cookies{self.count}.json'
        file_path = os.path.join(folder_name, cookies_file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                cookies = json.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        else:
            print('No cookies file found')

    def sign_in(self):
        time.sleep(10)
        try:
            print("Entering in signing in phase")
            self.driver.get("https://accounts.google.com/servicelogin?hl=en-gb")
            
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            
            enter_email = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
            enter_email.send_keys(self.email)
            
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            time.sleep(3)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='Next']"))).click()
            
            enter_pass = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
            enter_pass.send_keys(self.passw)
            time.sleep(3)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='Next']"))).click()
            
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            time.sleep(3)
        except:
            print("Already signed in")
            
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[normalize-space(.)='Confirm your recovery email']"))).click()
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            time.sleep(4)
            enter_remail = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
            enter_remail.send_keys(self.r_email)
            
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='Next']"))).click()
            
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            time.sleep(2)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[normalize-space(.)='Not now']"))).click()
            
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            time.sleep(2)
        except:
            print("Signed in")
            
        print("Signed in Complete")
    def convert_time(self, ad_duration):
        time_obj = datetime.strptime(ad_duration, '%M:%S')
        total_seconds = time_obj.minute * 60 + time_obj.second
        return total_seconds

    def check_add(self):
        def scroll_down(driver):
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
        try:
            but = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='ytp-large-play-button ytp-button']")))
            but.click()
            time.sleep(3)
        except:
            pass
        
        try:
            #current_window_handle = self.driver.current_window_handle
            print("Enter to check add")
            # ad_duration = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//span[@class='ytp-ad-duration-remaining']"))).text
            self.driver.find_element(By.XPATH,'//*[@id="movie_player"]/div[1]/video').click()
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            time.sleep(2)
            l=False
            try:
                self.driver.find_element(By.XPATH,"//button[contains(@class, 'ytp-ad-button') and contains(@aria-label, 'link')]").click()
                l=True
            except:
                print("First try failed")
            if l is not True:
                try:
                    self.driver.find_element(By.XPATH,"//span[@class='ytp-ad-button-text']").click()
                except:
                    print("second try failed")
                

            try:
                # WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
                # for window_handle in self.driver.window_handles:
                #     if window_handle != current_window_handle:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                print("opening add in new tab")
                time.sleep(5)
                file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
                self.driver.get_screenshot_as_file(file_path)
                for _ in range(10):
                    scroll_down(self.driver)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                # time.sleep(4)
                # self.driver.quit()
                # sys.exit()
                #break
            except:
                print("New window did not open within the timeout period.")
        except:
            print("No add for now")
        
        try:
            skip_add = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ytp-ad-skip-button-modern')]")))
            skip_add.click()
            time.sleep(1)
        except:
            print("No skip Button")



    def sub_like(self):
        try:
            if "S" in self.option:
                sub=self.driver.find_element(By.XPATH,"//button[contains(@class, 'yt-spec-button-shape-next') and contains(@aria-label, 'Subscribe')]")
                sub.click()
                print("subscribed")
                file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
                self.driver.get_screenshot_as_file(file_path)
                time.sleep(2)
        except:
            print("Already Subscribed")

        try:
            if "L" in self.option:
                like=self.driver.find_element(By.XPATH,"//button[contains(@class, 'yt-spec-button-shape-next') and @title='I like this']")
                like.click()
                file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
                self.driver.get_screenshot_as_file(file_path)
                print("Liked")
                time.sleep(2)
        except:
            print("Already Liked")

    def play_video(self):
        start_time = time.time()  # Record the start time
        elapsed_time = 0
        like_called = False
        while elapsed_time < self.max_duration:
            self.check_add()
            elapsed_time = time.time() - start_time
            time.sleep(5)
            if not like_called and elapsed_time >= 10:
                self.sub_like()
                like_called = True 
        if not like_called:
            self.sub_like()
            like_called = True 
        self.driver.quit()



    def create_directory(self):
        if os.path.exists(self.ss):
            shutil.rmtree(self.ss)
        os.makedirs(self.ss)


    def text_search(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//form[@id="search-form"]//input[@id="search"]')))
            time.sleep(3)
            element.send_keys(self.link)
            time.sleep(3)
            element.send_keys(Keys.ENTER)
        except:
            print("Unable to find the element")

        time.sleep(6)
        try:
            a = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@id='contents']//ytd-video-renderer//div[@id='title-wrapper']")))
            a[0].click()
            time.sleep(4)
        except:
            print("Unable to find video")


    def check_sign_in(self):
        self.driver.get("https://www.google.com/")
        time.sleep(5)
        try:
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[normalize-space(.)='Sign in']"))
            )
            print("Not signed in")
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            self.sign_in()
        except:
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            print("Already Signed")
            pass
        #self.driver.get("https://www.youtube.com/")
        time.sleep(4)
        #self.save_cookies()

    def run_bot(self):
        print(f'Bot{self.count} running')
        self.ss = f'Bots_screenshots//Bot_{self.count}'
        self.create_directory()
        self.check_sign_in()
        if self.checker =="T":
            self.driver.get('https://www.youtube.com?hl=en-gb')
            print("Opening Text search")
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            time.sleep(5)
            try:
                self.driver.find_element(By.XPATH,"//button[normalize-space(.)='Accept all']").click()
                print("Accept cookies")
                time.sleep(3)
            except:
                print("No cookies")
            self.text_search()
            self.play_video()
        elif self.checker =="L":
            print("Opening Link search")
            self.driver.get(self.link)
            time.sleep(5)
            file_path = os.path.join(self.ss,f'SS_{str(generate_8_digit_uuid())}.png')
            self.driver.get_screenshot_as_file(file_path)
            try:
                self.driver.find_element(By.XPATH,"//button[normalize-space(.)='Accept all']").click()
                print("Accept cookies")
                time.sleep(3)
            except:
                print("No cookies")
            self.play_video()


