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
    
    #確認Camera Name
    def test_case068_Check_CameraName(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Camera Name欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CameraName")))
        CameraName = self.driver.title #該camera name名稱是綁定driver.title名稱
        self.assertEqual(CameraName, "Focus-25-00-01", f"CameraName is {CameraName}, not Focus-25-00-01")
    
    #確認Config Version 
    def test_case069_Check_ConfigVersion(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Config Version 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_ConfigVersion")))
        ConfigVersion =  self.driver.find_element(By.ID, "input_ConfigVersion").get_attribute("value")
        self.assertEqual(ConfigVersion, "1.0.0", f"Config Version is {ConfigVersion}, not 1.0.0")

    #確認Date Format
    def test_case070_Check_DateFormat(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Time Format 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Device_TimeFormat_div")))
        DateFormat =  self.driver.find_element(By.ID, "select_Device_TimeFormat_div").get_attribute("data-text")
        self.assertEqual(DateFormat, "MDY", f"Time Format is {DateFormat}, not MDY")
    
    #確認Time Format
    def test_case071_Check_TimeFormat(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Time Format 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Device_input_TimeFormat_12Hour")))
        #該ratio button不是checkbox，因此不能用is_selected()
        #是用圖判斷，圖是存在src屬性內，因此是判斷src屬性是哪一張圖。
        radio_12 = self.driver.find_element(By.ID, "12hour")
        src_value = radio_12.get_attribute("src")
        print(src_value)
        if "http://172.16.103.17/from_temp/res/img/Content/System_Device/bt-storage-check-2-pre.png" in src_value:
            print("12-hour is selected")
        else:
            self.fail("12-hour is not selected")
    
    #確認Time Zone
    def test_case072_Check_Timezone(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Time Zone 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Device_TimeZone_div")))
        TimeZone =  self.driver.find_element(By.ID, "select_Device_TimeZone_div").get_attribute("data-text")
        self.assertEqual(TimeZone, "(UTC±00:00) Coordinated Universal Time", f"Time Zone is {TimeZone}, not (UTC±00:00) Coordinated Universal Time")

    #確認Daylight Saving
    def test_case073_Check_DaylightSaving(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Daylight Saving欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Daylight")))
        DaylightSaving = self.driver.find_element(By.ID, "Daylight")
        self.assertTrue(DaylightSaving.is_selected(),"Daylight saving is not enabled")
    
    #確認Clock Sync	
    def test_case074_Check_ClockSync(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Time Zone 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Device_ClockSync_div")))
        ClockSync =  self.driver.find_element(By.ID, "select_Device_ClockSync_div").get_attribute("data-text")
        self.assertEqual(ClockSync, "Manual", f"Clock Sync is {ClockSync}, not Manual")
    
    #確認Recording Indicator LED
    def test_case075_Check_RecordingIndicatorLED(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Recording Indicator LED欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Device_LEDIndicator_div")))
        RecordingIndicatorLED =  self.driver.find_element(By.ID, "select_Device_LEDIndicator_div").get_attribute("data-text")
        self.assertEqual(RecordingIndicatorLED, "Off", f"Recording Indicator LED is {RecordingIndicatorLED}, not Off")
    

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
       

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/SeleniumProject/test_reports'))
