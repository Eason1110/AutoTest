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
        #service = Service(ChromeDriverManager().install())
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
    
    def test_case0118_Check_Overlay_textOverlay_text1_FreeText(self):
        self.errors = []  # 一開始先建立 list
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #點擊text overlay tab
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_div_TextOverlay_Selector")))
        self.driver.find_element(By.ID, "Overlay_div_TextOverlay_Selector").click()
        #開啟text1
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_1")))
        checkbox= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_1")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_1 .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_Text_1_FreeText_input")))
        FreeText1= self.driver.find_element(By.ID, "Overlay_Text_1_FreeText_input").get_attribute("value")
        try:
            self.assertEqual(FreeText1,"Free Text 1",f"Free Text is {FreeText1}, not Free Text 1")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))  
        #關閉free text1並save
        checkbox = self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_1")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_1 .slider")
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
    
    def test_case0119_Check_Overlay_textOverlay_text2_FreeText(self):
        self.errors = []  # 一開始先建立 list
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #點擊text overlay tab
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_div_TextOverlay_Selector")))
        self.driver.find_element(By.ID, "Overlay_div_TextOverlay_Selector").click()
        #開啟text2
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_2")))
        checkbox= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_2")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_2 .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_Text_2_FreeText_input")))
        FreeText2= self.driver.find_element(By.ID, "Overlay_Text_2_FreeText_input").get_attribute("value")
        try:
            self.assertEqual(FreeText2,"Free Text 2",f"Free Text is {FreeText2}, not Free Text 2")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))  
        #關閉free text1並save
        checkbox = self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_2")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_2 .slider")
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
    
    def test_case0120_Check_Overlay_textOverlay_text3_FreeText(self):
        self.errors = []  # 一開始先建立 list
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #點擊text overlay tab
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_div_TextOverlay_Selector")))
        self.driver.find_element(By.ID, "Overlay_div_TextOverlay_Selector").click()
        #開啟text3
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_3")))
        checkbox= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_3")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_3 .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_Text_3_FreeText_input")))
        FreeText3= self.driver.find_element(By.ID, "Overlay_Text_3_FreeText_input").get_attribute("value")
        try:
            self.assertEqual(FreeText3,"Free Text 3",f"Free Text is {FreeText3}, not Free Text 3")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))  
        #關閉free text1並save
        checkbox = self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_3")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_3 .slider")
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
    
    def test_case0121_Check_Overlay_textOverlay_text4_FreeText(self):
        self.errors = []  # 一開始先建立 list
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #點擊text overlay tab
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_div_TextOverlay_Selector")))
        self.driver.find_element(By.ID, "Overlay_div_TextOverlay_Selector").click()
        #開啟text1
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_4")))
        checkbox= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_4")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_4 .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_Text_4_FreeText_input")))
        FreeText4= self.driver.find_element(By.ID, "Overlay_Text_4_FreeText_input").get_attribute("value")
        try:
            self.assertEqual(FreeText4,"Free Text 4",f"Free Text is {FreeText4}, not Free Text 4")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))  
        #關閉free text1並save
        checkbox = self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_4")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_4 .slider")
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
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/SeleniumProject/test_reports'))
