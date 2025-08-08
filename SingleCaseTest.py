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
        time.sleep(4)
    
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
    
    def test_case047_Check_ALPR_Evidence_HDR_WDR(self):
        #到advance頁面檢查HDR/WDR
        self.go_to_ALPR_AdvancedSetting_page()
        status = self.driver.find_element(By.ID, "select_Image_WDRAndHDR_div").get_attribute("data-text")
        self.assertEqual(status, "Both Off", f"HDR/WDR is {status}, not Both Off")
    
    def test_case048_Check_ALPR_DigitalNoiseReduction(self):
        #到advance頁面檢查Digital Noise Reduction
        self.go_to_ALPR_AdvancedSetting_page()
        status = self.driver.find_element(By.ID, "select_Image_DigitalNoiseReduction_div").get_attribute("data-text")
        self.assertEqual(status, "3D NR", f"Digital Noise Reduction is {status}, not 3D NR")
    
    def test_case049_Check_ALPR_FilterMode(self):
        #到advance頁面檢查FilterMode
        self.go_to_ALPR_AdvancedSetting_page()
        status = self.driver.find_element(By.ID, "select_AS_FilterMode_div").get_attribute("data-text")
        self.assertEqual(status, "Auto", f"FilterMode is {status}, not Auto")

    def test_case050_Check_ALPR_ExposureMode(self):
        #到advance->exposure頁面檢查ExposureMode
        self.go_to_ALPR_AdvancedSetting_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        status = self.driver.find_element(By.ID, "select_AS_ExposureMode_div").get_attribute("data-text")
        self.assertEqual(status, "Auto", f"Exposure Mode is {status}, not Auto")
    
    def test_case051_Check_ALPR_EV_Value(self):
        #到advance->exposure頁面檢查Auto的EV Value
        self.go_to_ALPR_AdvancedSetting_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        self.assertEqual(status, "0", f"Exposure Mode is {status}, not 0")
    
    def test_case052_Check_ALPR_ExposureTime(self):
        #到advance->exposure頁面檢查ExposureTime
        self.go_to_ALPR_AdvancedSetting_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
        #檢查ExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_ExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_ExposureTime_div").get_attribute("data-text")
        self.assertEqual(status, "1/60s", f"Exposure Mode is {status}, not 1/60s")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case053_Check_ALPR_GainValue(self):
        #到advance->exposure頁面檢查GainValue
        self.go_to_ALPR_AdvancedSetting_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
        #檢查Gain Value
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_GainValue_div")))
        status = self.driver.find_element(By.ID, "select_AS_GainValue_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"Exposure Mode is {status}, not 50%")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case054_Check_ALPR_EV_Value(self):
        #到advance->exposure頁面檢查Manual的EV Value
        self.go_to_ALPR_AdvancedSetting_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
        #檢查EV Value
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_EVValue_div")))
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        self.assertEqual(status, "0", f"Exposure Mode is {status}, not 0")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case055_Check_ALPR_ExposureAuto(self):
        #到advance->exposure->Priority頁面檢查ExposureAuto
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
        #檢查ExposureAuto
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_ExposureAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_ExposureAuto")
        self.assertTrue(checkbox.is_selected(), "ExposureAuto is off")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case056_Check_ALPR_MinExposureTime(self):
        #到advance->exposure->Priority頁面檢查Min. Exposure Time
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
        #檢查MinExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MinExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_MinExposureTime_div").get_attribute("data-text")
        self.assertEqual(status, "1/60s", f"Min. Exposure Time is {status}, not 1/60s")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case057_Check_ALPR_MaxExposureTime(self):
        #到advance->exposure->Priority頁面檢查Max. Exposure Time
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
        #檢查MaxExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MaxExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_MaxExposureTime_div").get_attribute("data-text")
        self.assertEqual(status, "1/60s", f"Max. Exposure Time is {status}, not 1/60s")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case058_Check_ALPR_GainAuto(self):
        #到advance->exposure->Priority頁面檢查GainAuto
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
        #檢查GainAuto
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_GainAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_GainAuto")
        self.assertTrue(checkbox.is_selected(), "GainAuto is off")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case059_Check_ALPR_MinGain(self):
        #到advance->exposure->Priority頁面檢查Min. Gain
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
        #檢查MinGain
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MinGain_div")))
        status = self.driver.find_element(By.ID, "select_AS_MinGain_div").get_attribute("data-text")
        self.assertEqual(status, "0%", f"Min. Gain is {status}, not 0%")
        time.sleep(2)
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case060_Check_ALPR_MaxGain(self):
        #到advance->exposure->Priority頁面檢查Max. Gain
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
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

    def test_case061_Check_ALPR_Priority_EV_Value(self):
        #到advance->exposure->Priority頁面檢查EV Value
        self.go_to_ALPR_AdvancedSetting_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1) #等待切換完成
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
    
    def test_case062_Check_ALPR_HDR_WDR_Level(self):
        #到advance->exposure->Levels頁面HDR/WDR_Level
        self.go_to_ALPR_AdvancedSetting_page()
        #點選HDR/WDR切換both on，確保HDR/WDR_Level 點亮
        #HDR_WDR_button = self.driver.find_element(By.CLASS_NAME,"div_NowSelected")
        #HDR_WDR_button.click()
        #BothOn_button = self.driver.find_element(By.XPATH,"//li[@data-val='Both On']")
        #BothOn_button.click()
        #time.sleep(3) #等待HDR切換完成
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_div_Levels")))
        self.driver.find_element(By.ID, "AS_div_Levels").click()
        #time.sleep(1)
        # 檢查HDR/WDR_Level 先定位可滾動的容器與目標元素
        container = self.driver.find_element(By.ID, "AS_div_Levels_Main")
        target = self.driver.find_element(By.ID, "select_AS_WDRAndHDRLevel_div")
        # 執行 JavaScript 讓容器捲動，目標元素出現在可見範圍
        self.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", container, target)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_WDRAndHDRLevel_div")))
        status = self.driver.find_element(By.ID, "select_AS_WDRAndHDRLevel_div").get_attribute("data-text")
        self.assertEqual(status, "Level 2", f"EV Value is {status}, not Level 2")
        #點選HDR/WDR切換回預設值both Off
        #HDR_WDR_button = self.driver.find_element(By.CLASS_NAME,"div_NowSelected")
        #HDR_WDR_button.click()
        #BothOn_button = self.driver.find_element(By.XPATH,"//li[@data-val='Both Off']")
        #BothOn_button.click()
        #time.sleep(3)
    
    def test_case063_Check_ALPR_3DNR_Level(self):
        #到advance->exposure->Levels頁面HDR/WDR_Level
        self.go_to_ALPR_AdvancedSetting_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_div_Levels")))
        self.driver.find_element(By.ID, "AS_div_Levels").click()
        time.sleep(1)
        #檢查3D NR_Level
        # 先定位可滾動的容器與目標元素
        container = self.driver.find_element(By.ID, "AS_div_Levels_Main")
        target = self.driver.find_element(By.ID, "select_AS_3DNRLevel_div")
        # 執行 JavaScript 讓容器捲動，目標元素出現在可見範圍
        self.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", container, target)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_3DNRLevel_div")))
        status = self.driver.find_element(By.ID, "select_AS_3DNRLevel_div").get_attribute("data-text")
        self.assertEqual(status, "Level 2", f"3D NR level is {status}, not Level 2")

    def test_case064_Check_ALPR_2DNR_Level(self):
        #到advance->exposure->Levels頁面HDR/WDR_Level
        self.go_to_ALPR_AdvancedSetting_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_div_Levels")))
        self.driver.find_element(By.ID, "AS_div_Levels").click()
        time.sleep(1)
        #檢查3D NR_Level
        # 先定位可滾動的容器與目標元素
        container = self.driver.find_element(By.ID, "AS_div_Levels_Main")
        target = self.driver.find_element(By.ID, "select_AS_2DNRLevel_div")
        # 執行 JavaScript 讓容器捲動，目標元素出現在可見範圍
        self.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", container, target)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_2DNRLevel_div")))
        status = self.driver.find_element(By.ID, "select_AS_2DNRLevel_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"2D NR level is {status}, not Level 2")
   

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
       

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/SeleniumProject/test_reports'))
