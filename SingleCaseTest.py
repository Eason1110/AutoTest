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
    
    #到exposure_mode頁面
    def go_to_exposure_mode_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_ExposureMode"))).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))#等待loading消失
        time.sleep(0.5)
    
     # 到Administration頁面，等待所有元素就位
    def go_to_Administration_page(self):
        #切換到Administration頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Administration")))
        elem = self.driver.find_element(By.ID, "a_Administration")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Administration")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(5)
    
    #確認ALPR stream開關
    def test_case096_Check_ALPR_Stream_Switch(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        ALPR_Stream_Switch= self.driver.find_element(By.ID, "switch_StreamSwitch")
        self.assertFalse(ALPR_Stream_Switch.is_selected(),"Switch is on")

    #確認ALPR的Resolution
    def test_case097_Check_ALPR_Resolution(self):
        self.errors = []  # 一開始先建立 list，用來暫存false
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
        #開啟ALPR stream，預設是關閉
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位   
        #定位resolution
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainResolution_div")))
        resolution= self.driver.find_element(By.ID, "select_Stream_MainResolution_div").get_attribute("data-text")

        #檢查解析度，若false，則蒐集錯誤，後續程式碼會繼續執行
        try:
            self.assertEqual(resolution,"1920x1080(16:9)",f"Resolution is {resolution}, not 1920x1080(16:9)")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))
        
        #關閉ALPR stream並save
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if checkbox.is_selected():
                slider.click()
        #點擊儲存按鈕
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "SaveButton")))
        self.driver.find_element(By.CLASS_NAME, "SaveButton").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))

        # 最後統一檢查是否有錯
        if self.errors:
         raise AssertionError("\n".join(self.errors))
    
    #確認ALPR的Stream format
    def test_case098_Check_ALPR_StreamFormat(self):

        self.errors = []  # 一開始先建立 list
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
        #開啟ALPR stream，預設是關閉
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位   
        #定位StreamFormat並判斷
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainStreamFormat_div")))
        StreamFormat= self.driver.find_element(By.ID, "select_Stream_MainStreamFormat_div").get_attribute("data-text")
       
       #檢查stream format，若false，則蒐集錯誤，程式碼會繼續執行
        try:
            self.assertEqual(StreamFormat,"H.265",f"StreamFormat is {StreamFormat}, not H.265")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))

        #關閉ALPR stream並save
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if checkbox.is_selected():
             slider.click()
         # 點擊儲存按鈕
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "SaveButton")))
        self.driver.find_element(By.CLASS_NAME, "SaveButton").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))

         # 最後統一檢查是否有錯
        if self.errors:
            raise AssertionError("\n".join(self.errors))
    
    
    #確認ALPR的FrameRate
    def test_case099_Check_ALPR_FrameRate(self):
        self.errors = []  # 一開始先建立 list
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
        #開啟ALPR stream，預設是關閉
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位   
        #定位Frame Rate並判斷
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainFrameRate_div")))
        FrameRate= self.driver.find_element(By.ID, "select_Stream_MainFrameRate_div").get_attribute("data-text")
       
       #檢查Frame Rate，若false，則蒐集錯誤，程式碼會繼續執行
        try:
            self.assertEqual(FrameRate,"20",f"FrameRate is {FrameRate}, not 20")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))

        #關閉ALPR stream並save
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if checkbox.is_selected():
             slider.click()
         # 點擊儲存按鈕
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "SaveButton")))
        self.driver.find_element(By.CLASS_NAME, "SaveButton").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))

         # 最後統一檢查是否有錯
        if self.errors:
            raise AssertionError("\n".join(self.errors))
    
    #確認ALPR的URL String
    def test_case100_Check_ALPR_URL_String(self):
        self.errors = []  # 一開始先建立 list
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
        #開啟ALPR stream，預設是關閉
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位   
        #定位URL String
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Stream_URLString")))
        URL_String= self.driver.find_element(By.ID, "input_Stream_URLString").get_attribute("value")

        #判斷是否為alpr，有false就蒐集
        try:
         self.assertEqual(URL_String, "alpr333", f"URL Stream is {URL_String}, not alpr333")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))
        
        #關閉ALPR stream並save
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if checkbox.is_selected():
             slider.click()
        #點擊儲存按鈕
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "SaveButton")))
        self.driver.find_element(By.CLASS_NAME, "SaveButton").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))

         # 最後統一檢查是否有錯
        if self.errors:
            raise AssertionError("\n".join(self.errors))

    #確認ALPR的Audio Format
    def test_case101_Check_ALPR_AudioFormat(self):
        self.errors = []  # 一開始先建立 list
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
         #開啟ALPR stream，預設是關閉
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #定位Audio Format
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "SC_span_AudioFormat")))
        AudioFormat= self.driver.find_element(By.ID, "SC_span_AudioFormat").text
        print(AudioFormat)
        #判斷是否為AAC
        try:
            self.assertEqual(AudioFormat, "PCM", f"Audio Format is {AudioFormat}, not PCM")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))
        
         #關閉ALPR stream並save
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if checkbox.is_selected():
             slider.click()
        #點擊儲存按鈕
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "SaveButton")))
        self.driver.find_element(By.CLASS_NAME, "SaveButton").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        # 最後統一檢查是否有錯
        if self.errors:
            raise AssertionError("\n".join(self.errors))
    
    #確認ALPR的Rate Control
    def test_case102_Check_ALPR_RateControl(self):
        self.errors = []  # 一開始先建立 list
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
        #開啟ALPR stream，預設是關閉
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #定位Rate Control
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "MainStreamVBR")))
        button = self.driver.find_element(By.ID, "MainStreamVBR")

        try:
            bg_color = button.value_of_css_property("background-color")
            print(bg_color)
            if bg_color == "rgba(75, 93, 118, 1)":
                print("Rate Control is VBR")
            else:
                self.errors.append("Rate Control is not VBR")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))

        #關閉ALPR stream並save
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if checkbox.is_selected():
             slider.click()
        #點擊儲存按鈕
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "SaveButton")))
        self.driver.find_element(By.CLASS_NAME, "SaveButton").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        # 最後統一檢查是否有錯
        if self.errors:
            raise AssertionError("\n".join(self.errors))
    '''
    #確認ALPR的Target Rate
    def test_case103_Check_ALPR_TargetRate(self):
        self.errors = []  # 一開始先建立 list
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
        #開啟ALPR stream，預設是關閉
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #定位Target Rate
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Stream_MainRange")))
        TargetRate= self.driver.find_element(By.ID, "input_Stream_MainRange").get_attribute("value")
        #判斷target rate
        try:
            self.assertEqual(TargetRate, "25600kbps", f"Target Rate is {TargetRate}, not 25600kbps")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))

         #關閉ALPR stream並save
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if checkbox.is_selected():
             slider.click()
        #點擊儲存按鈕
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "SaveButton")))
        self.driver.find_element(By.CLASS_NAME, "SaveButton").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        # 最後統一檢查是否有錯
        if self.errors:
            raise AssertionError("\n".join(self.errors))
    '''
    #確認ALPR stream的Video Quality
    def test_case103_Check_ALPR_VideoQuality(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Third").click()
        time.sleep(1)  # 等待value更新，DOM 更新有延遲，加一個等待就能解決：
        #定位Target Rate
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainVideoQuality_div")))
        VideoQuality= self.driver.find_element(By.ID, "select_Stream_MainVideoQuality_div").get_attribute("data-text")
        self.assertEqual(VideoQuality, "High", f" Video Quality is {VideoQuality}, not High")

    #確認ALPR的GOP Length
    def test_case104_Check_ALPR_GOP_Length(self):
        self.errors = []  # 一開始先建立 list
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence ALPR
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "SC_span_Third")))
        self.driver.find_element(By.ID, "SC_span_Third").click()
        #開啟ALPR stream，預設是關閉
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_StreamSwitch")))
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #定位GOP Length
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainGOPLength_div")))
        GOP_Length= self.driver.find_element(By.ID, "select_Stream_MainGOPLength_div").get_attribute("data-text")
        #判斷GOP
        try:
            self.assertEqual(GOP_Length, "60", f"GOP Length is {GOP_Length}, not 60")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))    
         #關閉ALPR stream並save
        checkbox = self.driver.find_element(By.ID, "switch_StreamSwitch")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_switch_StreamSwitch .slider")
        if checkbox.is_selected():
             slider.click()
        #點擊儲存按鈕
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "SaveButton")))
        self.driver.find_element(By.CLASS_NAME, "SaveButton").click()
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        # 最後統一檢查是否有錯
        if self.errors:
            raise AssertionError("\n".join(self.errors))   
        

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
       

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/AutoTest/test_reports'))
