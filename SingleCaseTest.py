import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from selenium.webdriver.common.action_chains import ActionChains
import time
import cv2
import numpy as np
import HTMLTestRunner # type: ignore
import os
import configparser


class FactoryReset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        chrome_options = Options()
        chrome_options.add_argument('--log-level=3')  # SSL訊息和警告都不顯示

        # 在網站自動授予權限，可以用以下参数
        chrome_options.add_experimental_option(
        "prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,  # 允許麥克風
            "profile.default_content_setting_values.media_stream_camera": 1,  # 允許攝影機
            "profile.default_content_setting_values.geolocation": 1,  # 允許地理位置
            "profile.default_content_setting_values.notifications": 1,  # 允許通知
            "download.default_directory": "D:\\downloads"  # 更新為你的下載路徑
            }
        )
        
        # 使用該設定開啟chrome
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

        # 讀取配置文件
        config = configparser.ConfigParser()
        config.read(r'D:/selenium project/config.ini')

        URL = config['URL_Config']['URL']

        #開啟特定網址網頁
        cls.driver.get(URL)
        
        # 讀取配置文件
        config = configparser.ConfigParser()
        config.read(r'D:/selenium project/config.ini')
        username = config['Login_Config']['username']
        password = config['Login_Config']['password']

        # 輸入帳號密碼
        Username_button = cls.driver.find_element(By.ID, "div_SignIn_Username")
        Username_button.send_keys(username)
        Password_button = cls.driver.find_element(By.ID, "div_SignIn_Password")
        Password_button.send_keys(password)
        LoginIn_button = cls.driver.find_element(By.ID, "button_SignIn_OK")
        LoginIn_button.click()
        time.sleep(10)
        
    def setUp(self):

        time.sleep(2)

     #到image頁面，到頁面後要等待兩秒，等待所有元素就位
    def go_to_image_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        elem = self.driver.find_element(By.ID, "a_Image")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Image")))
        elem.click()
        time.sleep(4)

    #到advanced頁面
    def go_to_advanced_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_AdvancedSetting"))).click()
        time.sleep(4)

    def test_case033_Check_GainAuto(self):
        #到advance->exposure->Priority頁面檢查GainAuto
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        time.sleep(3) #等待切換完成
        #檢查GainAuto
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_GainAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_GainAuto")
        self.assertTrue(checkbox.is_selected(), "GainAuto is off")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case034_Check_MinGain(self):
        #到advance->exposure->Priority頁面檢查Min. Gain
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        time.sleep(3) #等待切換完成
        #檢查MinGain
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MinGain_div")))
        status = self.driver.find_element(By.ID, "select_AS_MinGain_div").get_attribute("data-text")
        self.assertEqual(status, "0%", f"Min. Gain is {status}, not 0%")
        time.sleep(2)
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case035_Check_MaxGain(self):
        #到advance->exposure->Priority頁面檢查Max. Gain
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        time.sleep(3) #等待切換完成
        #檢查MaxGain
        # 先定位可滾動的容器與目標元素
        container = self.driver.find_element(By.ID, "AS_div_Exposure_Main")
        target = self.driver.find_element(By.ID, "select_AS_MaxGain_div")
        # 執行 JavaScript 讓容器捲動，目標元素出現在可見範圍
        self.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", container, target)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MaxGain_div")))
        status = self.driver.find_element(By.ID, "select_AS_MaxGain_div").get_attribute("data-text")
        self.assertEqual(status, "100%", f"Max. Gain is {status}, not 100%")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case036_Check_Priority_EV_Value(self):
        #到advance->exposure->Priority頁面檢查EV Value
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        time.sleep(3) #等待切換完成
        #檢查EV value
        # 先定位可滾動的容器與目標元素
        container = self.driver.find_element(By.ID, "AS_div_Exposure_Main")
        target = self.driver.find_element(By.ID, "select_AS_EVValue_div")
        # 執行 JavaScript 讓容器捲動，目標元素出現在可見範圍
        self.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", container, target)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_EVValue_div")))
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        self.assertEqual(status, "0", f"EV Value is {status}, not 0")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
       

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/SeleniumProject/test_reports'))
