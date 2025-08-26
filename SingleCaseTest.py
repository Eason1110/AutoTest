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
    
      #case1~case8檢查image parameters頁面所有設定
    def test_case001_Check_Evidence_Brightness(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Brightness")))
        value = self.driver.find_element(By.ID, "input_Brightness").get_attribute('value')
        self.assertEqual(value, "60%", f"Brightness not 60%: {value}")

    def test_case002_Check_Evidence_Contrast(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Contrast")))
        value = self.driver.find_element(By.ID, "input_Contrast").get_attribute('value')
        self.assertEqual(value, "60%", f"Contrast not 60%: {value}")

    def test_case003_Check_Evidence_Saturation(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Saturation")))
        value = self.driver.find_element(By.ID, "input_Saturation").get_attribute('value')
        self.assertEqual(value, "60%", f"Saturation not 60%: {value}")

    def test_case004_Check_Evidence_Sharpness(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Sharpness")))
        value = self.driver.find_element(By.ID, "input_Sharpness").get_attribute('value')
        self.assertEqual(value, "60%", f"Sharpness not 60%: {value}")

    def test_case005_Check_Evidence_Gamma(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Gamma")))
        value = self.driver.find_element(By.ID, "input_Gamma").get_attribute('value')
        self.assertEqual(value, "60%", f"Gamma not 60%: {value}")

    def test_case006_Check_Evidence_Auto_wb_Mode(self):
        self.go_to_image_page()
        time.sleep(2)
        checkbox = self.driver.find_element(By.ID, "WhiteBalanceAuto")
        self.assertFalse(checkbox.is_selected(), "WhiteBalanceAuto is ON")

    def test_case007_Check_Evidence_Color_Temperature(self):
        self.go_to_image_page()

        # 取消 Auto White Balance
        checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#div_WhiteBalance input[type='checkbox']"))
            )
        slider = self.driver.find_element(By.CSS_SELECTOR, "#div_WhiteBalance .slider")

        if checkbox.is_selected():
            slider.click()
        #關閉白平衡後須等待兩秒，才能正常讀取value數值
        time.sleep(2)
        # 找到色溫滑桿
        color_temp_slider = self.driver.find_element(By.ID, "slider_colorTemperature")
        # 取得當前的 value 屬性
        current_temp = color_temp_slider.get_attribute("value")
        # 驗證是否為 5000K
        if current_temp == "8000":
            print("Color temperature is 8000K")
        else:
            self.fail(f"Color temperature is {current_temp}K, not 8000K")
        #等待三秒後切換回為ON，不能馬上切換，否則會失敗
        time.sleep(3)
        # 再點回 ON（恢復勾選）
        #WebDriverWait(self.driver, 5).until(
          #EC.element_to_be_clickable((By.CSS_SELECTOR, "#div_WhiteBalance .slider"))
        #).click()

    def test_case008_Check_Evidence_LDC(self):
        self.go_to_image_page()
        checkbox = self.driver.find_element(By.ID, "LDC")
        self.assertTrue(checkbox.is_selected(), "LDC is OFF") 
         
    #-----------------------2025/08/21----------------------------------------

    #Case9~Case12後開始檢查image config頁面的所有設定
    def test_case009_Check_Evidence_RotateViewFlip(self):
        self.go_to_image_config_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_Flip_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_Flip_div").get_attribute("data-text")
        self.assertEqual(status, "Horizontal", f"Flip is not Horizontal, it's {status}")

    def test_case010_Check_Evidence_VideoOrientation(self):
        self.go_to_image_config_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_VideoOrientation_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_VideoOrientation_div").get_attribute("data-text")
        self.assertEqual(status, "180°", f"Video Orientation is not 180 degree, it's {status}")
    
    def test_case011_Check_Evidence_ViewAngle(self):
        self.go_to_image_config_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_ViewAngle_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_ViewAngle_div").get_attribute("data-text")
        self.assertEqual(status, "Wide", f"View Angle is {status}, not Wide")

    def test_case012_Check_Evidence_PowerLineSequence(self):
        self.go_to_image_config_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_PowerLineFrequency_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_PowerLineFrequency_div").get_attribute("data-text")
        self.assertEqual(status, "50Hz", f"Power line frequency is {status}, not 50Hz")

    #case13開始檢查exposure mode頁面的設定
    def test_case013_Check_Evidence_ExposureMode(self):
        #到Exposure頁面檢查ExposureMode
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_ExposureMode_div").get_attribute("data-text")
        self.assertEqual(status, "Center Metering", f"Exposure Mode is {status}, not Center Metering")

    def test_case014_Check_Evidence_AESpeed(self):
        #到Exposure頁面檢查AESpeed
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESpeed_div").get_attribute("data-text")
        self.assertEqual(status, "60%", f"AE Speed is {status}, not 60%")

    def test_case015_Check_Evidence_AESensitivity(self):
        #到Exposure頁面檢查AESensitivity
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESensitivity_div").get_attribute("data-text")
        self.assertEqual(status, "60%", f"AE Sensitivity is {status}, not 60%")
    
    def test_case016_Check_Evidence_HDR_WDR(self):
        #到advance頁面檢查HDR/WDR
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_Image_WDRAndHDR_div").get_attribute("data-text")
        self.assertEqual(status, "WDR Only", f"HDR/WDR is {status}, not WDR Only")
    
    def test_case017_Check_Evidence_DigitalNoiseReduction(self):
        #到advance頁面檢查Digital Noise Reduction
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_Image_DigitalNoiseReduction_div").get_attribute("data-text")
        self.assertEqual(status, "2D NR", f"Digital Noise Reduction is {status}, not 2D NR")
    
    def test_case018_Check_Evidence_FilterMode(self):
        #到advance頁面檢查FilterMode
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_AS_FilterMode_div").get_attribute("data-text")
        self.assertEqual(status, "Auto", f"FilterMode is {status}, not Auto")

    def test_case019_Check_Evidence_ExposureMode(self):
        #到advance->exposure頁面檢查ExposureMode
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        status = self.driver.find_element(By.ID, "select_AS_ExposureMode_div").get_attribute("data-text")
        self.assertEqual(status, "Manual", f"Exposure Mode is {status}, not Manual")
    
    def test_case020_Check_Evidence_EV_Value(self):
        #到advance->exposure頁面檢查Auto的EV Value
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #檢查EV
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text") 
        self.assertEqual(status, "-2", f"EV Value is {status}, not -2")
        

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
       

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/AutoTest/test_reports'))
