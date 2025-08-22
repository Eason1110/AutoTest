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
import sys
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
        #service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

        # 讀取配置文件
        config = configparser.ConfigParser()
        config.read(r'D:/AutoTest/config.ini')

        URL = config['URL_Config']['URL']

        #開啟特定網址網頁
        cls.driver.get(URL)
        
        # 讀取配置文件
        config = configparser.ConfigParser()
        config.read(r'D:/AutoTest/config.ini')
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
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
    #到image_config頁面
    def go_to_image_config_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_ImageConfigs"))).click()
        time.sleep(2)

    #到advanced頁面
    def go_to_advanced_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_AdvancedSetting"))).click()
        time.sleep(4)
    
    #到system頁面->Device頁面
    def go_to_system_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_System")))
        elem = self.driver.find_element(By.ID, "a_System")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_System")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
    #到system頁面->Stream Configs頁面
    def go_to_stream_config_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_System")))
        elem = self.driver.find_element(By.ID, "a_System")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_System")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        StreamConfig = self.driver.find_element(By.ID, "a_Stream")
        StreamConfig.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))

    #到ALPR image頁面，等待所有元素就位
    def go_to_ALPR_image_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        elem = self.driver.find_element(By.ID, "a_Image")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Image")))
        elem.click()
        #切換到ALPR cam
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "span_CameraSwitch_Camera")))
        self.driver.find_element(By.ID, "span_CameraSwitch_Camera").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='ALPR_Camera']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
    #到ALPR image configs頁面，等待所有元素就位
    def go_to_ALPR_image_configs_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        elem = self.driver.find_element(By.ID, "a_Image")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Image")))
        elem.click()
        #切換到ALPR cam
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "span_CameraSwitch_Camera")))
        self.driver.find_element(By.ID, "span_CameraSwitch_Camera").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='ALPR_Camera']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #切換到Image configs頁面
        self.driver.find_element(By.ID, "a_ImageConfigs").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
    #到ALPR exposure Mode頁面，等待所有元素就位
    def go_to_ALPR_ExposureMode_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        elem = self.driver.find_element(By.ID, "a_Image")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Image")))
        elem.click()
        #切換到ALPR cam
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "span_CameraSwitch_Camera")))
        self.driver.find_element(By.ID, "span_CameraSwitch_Camera").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='ALPR_Camera']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #切換到Image configs頁面
        self.driver.find_element(By.ID, "a_ExposureMode").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))

    #到ALPR exposure Mode頁面，等待所有元素就位
    def go_to_ALPR_AdvancedSetting_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        elem = self.driver.find_element(By.ID, "a_Image")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Image")))
        elem.click()
        #切換到ALPR cam
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "span_CameraSwitch_Camera")))
        self.driver.find_element(By.ID, "span_CameraSwitch_Camera").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='ALPR_Camera']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #切換到Image configs頁面
        self.driver.find_element(By.ID, "a_AdvancedSetting").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
     #到System Overlay頁面，等待所有元素就位
    def go_to_Systme_Overlay_page(self):
        #切換到system頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_System")))
        elem = self.driver.find_element(By.ID, "a_System")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_System")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #再切換到overlay頁面
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Overlay")))
        self.driver.find_element(By.ID, "a_Overlay").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
    #到System Overlay頁面，等待所有元素就位
    def go_to_Systme_Audio_page(self):
        #切換到system頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_System")))
        elem = self.driver.find_element(By.ID, "a_System")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_System")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #再切換到audio頁面
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Audio")))
        self.driver.find_element(By.ID, "a_Audio").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
      #到Network Basic頁面，等待所有元素就位
    def go_to_Network_Basic_page(self):
        #切換到system頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Network")))
        elem = self.driver.find_element(By.ID, "a_Network")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Network")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
    # 到Network Advanced頁面，等待所有元素就位
    def go_to_Network_Advanced_page(self):
        #切換到system頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Network")))
        elem = self.driver.find_element(By.ID, "a_Network")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Network")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Advanced")))
        self.driver.find_element(By.ID, "a_Advanced").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
    # 到Notification頁面，等待所有元素就位
    def go_to_Notification_page(self):
        #切換到system頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Notification")))
        elem = self.driver.find_element(By.ID, "a_Notification")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Notification")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
    # 到Storage頁面，等待所有元素就位
    def go_to_Storage_page(self):
        #切換到Storage頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Storage")))
        elem = self.driver.find_element(By.ID, "a_Storage")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Storage")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
    
     # 到Administration頁面，等待所有元素就位
    def go_to_Administration_page(self):
        #切換到Administration頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Administration")))
        elem = self.driver.find_element(By.ID, "a_Administration")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Administration")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(5)
    
    def test_case0143_Check_Evidence_Priority_ExposureAuto_off_ExposureTime(self):
        self.errors = []  # 一開始先建立 list，用來暫存false
        #到advance->exposure->Priority頁面檢查
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查ExposureAuto並關閉它
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_ExposureAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_ExposureAuto")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#AS_input_ExposureAuto + .slider")
        if checkbox.is_selected():
            slider.click()
        #檢查Exposure Time
        ExposureTime = self.driver.find_element(By.ID, "select_AS_ExposureTime_div").get_attribute("data-text")
        try:
            self.assertEqual(ExposureTime,"1/60s",f"Exposure Time is {ExposureTime}, not 1/60s" )
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))

         #假設沒關閉，將exposure auto給開啟   
        if not checkbox.is_selected():
            slider.click()
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

        # 最後統一檢查是否有錯
        if self.errors:
         raise AssertionError("\n".join(self.errors))
    
    def test_case0144_Check_Evidence_Priority_GainAuto_off_GainValue(self):
        self.errors = []  # 一開始先建立 list，用來暫存false
        #到advance->exposure->Priority頁面檢查
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查ExposureAuto並關閉它
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_GainAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_GainAuto")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#AS_input_GainAuto + .slider")
        if checkbox.is_selected():
            slider.click()
        #檢查Gain Value
        GainValue = self.driver.find_element(By.ID, "select_AS_GainValue_div").get_attribute("data-text")
        try:
            self.assertEqual(GainValue,"50%",f"Gain Value is {GainValue}, not 50%" )
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))

         #假設沒關閉，將exposure auto給開啟   
        if not checkbox.is_selected():
            slider.click()
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

        # 最後統一檢查是否有錯
        if self.errors:
         raise AssertionError("\n".join(self.errors))
        
    def test_case0145_Check_ALPR_Priority_ExposureAuto_off_ExposureTime(self):
        self.errors = []  # 一開始先建立 list，用來暫存false
        #到advance->exposure->Priority頁面檢查
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查ExposureAuto並關閉它
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_ExposureAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_ExposureAuto")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#AS_input_ExposureAuto + .slider")
        if checkbox.is_selected():
            slider.click()
        #檢查Exposure Time
        ExposureTime = self.driver.find_element(By.ID, "select_AS_ExposureTime_div").get_attribute("data-text")
        try:
            self.assertEqual(ExposureTime,"1/60s",f"Exposure Time is {ExposureTime}, not 1/60s" )
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))

         #假設沒關閉，將exposure auto給開啟   
        if not checkbox.is_selected():
            slider.click()
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

        # 最後統一檢查是否有錯
        if self.errors:
         raise AssertionError("\n".join(self.errors))
    
    def test_case0146_Check_ALPR_Priority_GainAuto_off_GainValue(self):
        self.errors = []  # 一開始先建立 list，用來暫存false
        #到advance->exposure->Priority頁面檢查
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)

        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查ExposureAuto並關閉它
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_GainAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_GainAuto")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#AS_input_GainAuto + .slider")
        if checkbox.is_selected():
            slider.click()
        #檢查Gain Value
        GainValue = self.driver.find_element(By.ID, "select_AS_GainValue_div").get_attribute("data-text")
        try:
            self.assertEqual(GainValue,"50%",f"Gain Value is {GainValue}, not 50%" )
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))

         #假設沒關閉，將exposure auto給開啟   
        if not checkbox.is_selected():
            slider.click()
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

        # 最後統一檢查是否有錯
        if self.errors:
         raise AssertionError("\n".join(self.errors))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
       

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/AutoTest/test_reports'))
