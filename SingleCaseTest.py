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
    
    #確認Evidence Live的Resolution
    def test_case086_Check_Evidence_Live_Resolution(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位resolution
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainResolution_div")))
        resolution= self.driver.find_element(By.ID, "select_Stream_MainResolution_div").get_attribute("data-text")
        self.assertEqual(resolution, "1280x720(16:9)", f"Resolution is {resolution}, not 1280x720(16:9)")
    
    
    #確認Evidence Live的Stream format
    def test_case087_Check_Evidence_Live_StreamFormat(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位StreamFormat
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainStreamFormat_div")))
        StreamFormat= self.driver.find_element(By.ID, "select_Stream_MainStreamFormat_div").get_attribute("data-text")
        self.assertEqual(StreamFormat, "H.264", f"Stream Format is {StreamFormat}, not H.264")
    
    #確認Evidence Live的FrameRate
    def test_case088_Check_Evidence_Live_FrameRate(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位FrameRate
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainFrameRate_div")))
        FrameRate= self.driver.find_element(By.ID, "select_Stream_MainFrameRate_div").get_attribute("data-text")
        self.assertEqual(FrameRate, "15", f"Stream Format is {FrameRate}, not 15")
    
    #確認Evidence Live的Overlay
    def test_case089_Check_Evidence__Live_Overlay(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位overlay
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_Overlay")))
        Overlay= self.driver.find_element(By.ID, "switch_Overlay")
        self.assertTrue(Overlay.is_selected(),"Overlay is not enabled")
    
    #確認Evidence Live的URL String
    def test_case090_Check_Evidence_Live_URL_String(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
         #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位URL String
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Stream_URLString")))
        URL_String= self.driver.find_element(By.ID, "input_Stream_URLString").get_attribute("value")
        self.assertEqual(URL_String, "stream2", f"URL Stream is {URL_String}, not stream2")

    #確認Evidence Live的Audio Format
    def test_case091_Check_Evidence_Live_AudioFormat(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位Audio Format
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "SC_span_AudioFormat")))
        AudioFormat= self.driver.find_element(By.ID, "SC_span_AudioFormat").text
        print(AudioFormat)
        self.assertEqual(AudioFormat, "AAC", f"Audio Format is {AudioFormat}, not AAC")
    
    #確認Evidence Live的Rate Control
    def test_case092_Check_Evidence__Live_RateControl(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位Audio Format
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "MainStreamCBR")))
        button = self.driver.find_element(By.ID, "MainStreamCBR")
        bg_color = button.value_of_css_property("background-color")
        print(bg_color)
        if bg_color == "rgba(75, 93, 118, 1)":
            print("Rate Control is CBR")
        else:
            self.fail("Rate Control is not CBR")
    
    #確認Evidence Live的Target Rate
    def test_case093_Check_Evidence_Live_TargetRate(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        time.sleep(1)  # 等待value更新，DOM 更新有延遲，加一個等待就能解決：
        #定位Target Rate
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Stream_MainRange")))
        TargetRate= self.driver.find_element(By.ID, "input_Stream_MainRange").get_attribute("value")
        self.assertEqual(TargetRate, "2048kbps", f"Target Rate is {TargetRate}, not 2048kbps")
    
    #確認Evidence Live的GOP Length
    def test_case094_Check_Evidence_Live_GOP_Length(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位GOP Length
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainGOPLength_div")))
        GOP_Length= self.driver.find_element(By.ID, "select_Stream_MainGOPLength_div").get_attribute("data-text")
        self.assertEqual(GOP_Length, "30", f"GOP Length is {GOP_Length}, not 30")
    
    #確認Evidence Live的Entropy Coding
    def test_case095_Check_Evidence_Live_EntropyCoding(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
         #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位Entropy Coding
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_EntropyCoding_div")))
        EntropyCoding= self.driver.find_element(By.ID, "select_Stream_EntropyCoding_div").get_attribute("data-text")
        self.assertEqual(EntropyCoding, "CABAC", f"Entropy Coding is {EntropyCoding}, not CABAC")    
    


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
       

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/SeleniumProject/test_reports'))
