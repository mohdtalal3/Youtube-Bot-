# main_driver.switch_to.window(main_driver.window_handles[-1])
#                 main_driver.close()
#                 main_driver.switch_to.window(main_driver.window_handles[-1])
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
import bot_with_google
import bot_without_google
from concurrent.futures import ThreadPoolExecutor
import threading
import number_of_bots_to_run
semaphore = threading.Semaphore(number_of_bots_to_run.a)
class YouTubeBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Bot GUI')
        self.setGeometry(100, 100, 600, 400)  # Larger window size

        layout = QVBoxLayout()

        # Add image
        image_label = QLabel(self)
        pixmap = QPixmap('y.png')  
        pixmap = pixmap.scaledToWidth(600)  # Scale the image width to fit the window
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        self.max_time_label = QLabel('Enter Max Time in seconds:')
        self.max_time_input = QLineEdit()
        layout.addWidget(self.max_time_label)
        layout.addWidget(self.max_time_input)


        self.link_label = QLabel('Enter youtube Text or link:')
    
        self.link_input = QLineEdit()
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_input)
        

        self.subscribe_checkbox = QCheckBox('Subscribe')
        layout.addWidget(self.subscribe_checkbox)

        self.like_checkbox = QCheckBox('Like')
        layout.addWidget(self.like_checkbox)

        self.WO_G_checkbox = QCheckBox('Run without Accounts')
        layout.addWidget(self.WO_G_checkbox)

        self.W_G_checkbox = QCheckBox('Run with google accounts')
        layout.addWidget(self.W_G_checkbox )

        self.using_text_checkbox = QCheckBox('Text to search')
        layout.addWidget(self.using_text_checkbox)

        self.link_checkbox = QCheckBox('Link to search')
        layout.addWidget(self.link_checkbox )

        self.start_button = QPushButton('Start Bot')
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)

        self.setLayout(layout)


    def run_with_google(self):
        max_time = int(self.max_time_input.text())
        print(max_time)
        link = self.link_input.text()
        option = []
        if self.subscribe_checkbox.isChecked():
            option.append('S')
        if self.like_checkbox.isChecked():
            option.append('L')

        if self.using_text_checkbox.isChecked():
            print("Text search")
            checker = "T"
        if self.link_checkbox.isChecked():
            print("Print link search")
            checker = "L"

        csv_file = "bot_data.csv"
        bots = create_bot_from_csv(csv_file, max_time, option, link, checker)
        threads = []
        for bot in bots:
            try:
                bot.driver = bot.setup_webdriver()
                semaphore.acquire()
                thread = threading.Thread(target=run_with_semaphore, args=(bot,))
                threads.append(thread)
                thread.start()
                #time.sleep(2)
            except:
                continue

        for thread in threads:
            thread.join()
        print("All bots completed")
        return
    


    def run_without_google(self):
        max_time = int(self.max_time_input.text())
        print(max_time)
        link = self.link_input.text()
        if self.using_text_checkbox.isChecked():
            print("Text search")
            checker = "T"
        if self.link_checkbox.isChecked():
            print("Print link search")
            checker = "L"
        csv_file = "bot_data_without_google.csv"
        bots = create_bot_from_csv_without_google(csv_file, max_time, link, checker)
        threads = []
        for bot in bots:
            try:
                bot.driver = bot.setup_webdriver()
                # Acquire a permit from the semaphore
                semaphore.acquire()
                thread = threading.Thread(target=run_with_semaphore, args=(bot,))
                threads.append(thread)
                thread.start()
                #time.sleep(2)
            except:
                continue

        for thread in threads:
            thread.join()
        print("All bots completes")
        return




    def start_bot(self):
        if self.WO_G_checkbox.isChecked():
            print("Running without google")
            self.run_without_google()
        if self.W_G_checkbox.isChecked():
            print("Running with google accounts")
            self.run_with_google()

        
        
def run_with_semaphore(bot):
    try:
        bot.run_bot()
    finally:
        # Release the permit back to the semaphore
        semaphore.release()
def create_bot_from_csv_without_google(csv_file, max_time,link,checker):
    bots = []
    data = pd.read_csv(csv_file)
    count=1
    for _, row in data.iterrows():
        bot = bot_without_google.YouTubeBot(
            max_time,
            row['ip'],
            count,
            link,
            checker
        )
        bots.append(bot)
        count=count+1
    return bots


def create_bot_from_csv(csv_file, max_time, option,link,checker):
    bots = []
    data = pd.read_csv(csv_file)
    count=1
    for _, row in data.iterrows():
        bot = bot_with_google.YouTubeBot(
            max_time,
            option,
            row['email'],
            row['password'],
            row["recovery_email"],
            row['ip'],
            count,
            link,
            checker
        )
        bots.append(bot)
        count=count+1
    return bots

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    app = QApplication(sys.argv)
    gui = YouTubeBotGUI()
    gui.show()
    sys.exit(app.exec_())

