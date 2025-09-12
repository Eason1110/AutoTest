import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
import HTMLTestRunner  # type: ignore
import configparser
import time


class FactoryReset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1,
            "download.default_directory": "D:\\downloads"
        })

        #service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

        #讀取config ini檔
        config = configparser.ConfigParser()
        config.read(r'D:/AutoTest/config.ini')
        URL = config['URL_Config']['URL']
        username = config['Login_Config']['username']
        password = config['Login_Config']['password']

        #到URL網頁輸入帳號密碼並登入
        cls.driver.get(URL)
        WebDriverWait(cls.driver, 10).until(EC.presence_of_element_located((By.ID, "div_SignIn_Username"))).send_keys(username)
        cls.driver.find_element(By.ID, "div_SignIn_Password").send_keys(password)
        cls.driver.find_element(By.ID, "button_SignIn_OK").click()
        WebDriverWait(cls.driver, 30).until(EC.presence_of_element_located((By.ID, "a_Image")))
    
    #每個test case間暫停一秒
    def setUp(self):
        time.sleep(1)

    #到image頁面，到頁面後要等待兩秒，等待所有元素就位
    def go_to_image_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        elem = self.driver.find_element(By.ID, "a_Image")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Image")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
        time.sleep(1)

    #到image_config頁面
    def go_to_image_config_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_ImageConfigs"))).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
        time.sleep(1)
    
    #到exposure_mode頁面
    def go_to_exposure_mode_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_ExposureMode"))).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))#等待loading消失
        time.sleep(1)

    #到advanced頁面
    def go_to_advanced_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_AdvancedSetting"))).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
        time.sleep(1)
    
    #到system頁面->Device頁面
    def go_to_system_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_System")))
        elem = self.driver.find_element(By.ID, "a_System")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_System")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
        time.sleep(1)
    
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
        time.sleep(1)
    
    #到ALPR image頁面，等待所有元素就位
    def go_to_ALPR_image_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        elem = self.driver.find_element(By.ID, "a_Image")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Image")))
        elem.click()
        #切換到ALPR cam
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "span_CameraSwitch_Camera")))
        self.driver.find_element(By.ID, "span_CameraSwitch_Camera").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='ALPR_Camera']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
        time.sleep(1)
    
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
        time.sleep(1)
    
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
        time.sleep(1)
    
    #到ALPR_AdvancedSetting頁面，等待所有元素就位
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
        time.sleep(1)
    
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
        time.sleep(1)
    
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
        time.sleep(1)
    
    #到Network Basic頁面，等待所有元素就位
    def go_to_Network_Basic_page(self):
        #切換到system頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Network")))
        elem = self.driver.find_element(By.ID, "a_Network")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Network")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1)
    
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
        time.sleep(1)
    
    # 到Notification頁面，等待所有元素就位
    def go_to_Notification_page(self):
        #切換到system頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Notification")))
        elem = self.driver.find_element(By.ID, "a_Notification")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Notification")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1)
    
    # 到Storage頁面，等待所有元素就位
    def go_to_Storage_page(self):
        #切換到Storage頁面
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Storage")))
        elem = self.driver.find_element(By.ID, "a_Storage")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Storage")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1)
    
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
    
    def test_case021_Check_Evidence_ExposureTime(self):
        #到advance->exposure頁面檢查ExposureTime
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查ExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_ExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_ExposureTime_div").get_attribute("data-text")
        #使用subTest如果判斷結果是失敗，後續的程式碼也可以正常執行，才能正常點擊save按鈕
        with self.subTest():
            self.assertEqual(status, "1/640s", f"Exposure Mode is {status}, not 1/640s")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case022_Check_Evidence_GainValue(self):
        #到advance->exposure頁面檢查GainValue
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查Gain Value
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_GainValue_div")))
        status = self.driver.find_element(By.ID, "select_AS_GainValue_div").get_attribute("data-text")
         #使用subTest如果判斷結果是失敗，後續的程式碼也可以正常執行，才能正常點擊save按鈕
        with self.subTest():
            self.assertEqual(status, "60%", f"Gain Value is {status}, not 60%")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case023_Check_Evidence_EV_Value(self):
        #到advance->exposure頁面檢查Manual的EV Value
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查EV Value
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_EVValue_div")))
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
         #使用subTest如果判斷結果是失敗，後續的程式碼也可以正常執行，才能正常點擊save按鈕
        with self.subTest():
            self.assertEqual(status, "-2", f"EV_Value is {status}, not -2")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
   
    def test_case024_Check_Evidence_ExposureAuto(self):
        #到advance->exposure->Priority頁面檢查ExposureAuto
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查ExposureAuto
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_ExposureAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_ExposureAuto")
        self.assertTrue(checkbox.is_selected(), "ExposureAuto is off")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case025_Check_Evidence_MinExposureTime(self):
        #到advance->exposure->Priority頁面檢查Min. Exposure Time
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查MinExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MinExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_MinExposureTime_div").get_attribute("data-text")
        with self.subTest():
            self.assertEqual(status, "1/800s", f"Min. Exposure Time is {status}, not 1/60s")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case026_Check_Evidence_MaxExposureTime(self):
        #到advance->exposure->Priority頁面檢查Max. Exposure Time
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查MaxExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MaxExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_MaxExposureTime_div").get_attribute("data-text")
        with self.subTest():
            self.assertEqual(status, "1/640s", f"Max. Exposure Time is {status}, not 1/60s")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case027_Check_Evidence_GainAuto(self):
        #到advance->exposure->Priority頁面檢查GainAuto
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查GainAuto
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_GainAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_GainAuto")
        with self.subTest():
            self.assertTrue(checkbox.is_selected(), "GainAuto is off")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case028_Check_Evidence_MinGain(self):
        #到advance->exposure->Priority頁面檢查Min. Gain
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查MinGain
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MinGain_div")))
        status = self.driver.find_element(By.ID, "select_AS_MinGain_div").get_attribute("data-text")
        with self.subTest():
            self.assertEqual(status, "10%", f"Min. Gain is {status}, not 10%")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case029_Check_Evidence_MaxGain(self):
        #到advance->exposure->Priority頁面檢查Max. Gain
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查MaxGain
        # 先定位可滾動的容器與目標元素
        container = self.driver.find_element(By.ID, "AS_div_Exposure_Main")
        target = self.driver.find_element(By.ID, "select_AS_MaxGain_div")
        # 執行 JavaScript 讓容器捲動，目標元素出現在可見範圍
        self.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", container, target)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MaxGain_div")))
        status = self.driver.find_element(By.ID, "select_AS_MaxGain_div").get_attribute("data-text")
        with self.subTest():
            self.assertEqual(status, "90%", f"Max. Gain is {status}, not 90%")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case030_Check_Evidence_Priority_EV_Value(self):
        #到advance->exposure->Priority頁面檢查EV Value
        self.go_to_advanced_page()
        time.sleep(1)
        #切換成Priority
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Priority']").click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        #檢查EV value
        # 先定位可滾動的容器與目標元素
        container = self.driver.find_element(By.ID, "AS_div_Exposure_Main")
        target = self.driver.find_element(By.ID, "select_AS_EVValue_div")
        # 執行 JavaScript 讓容器捲動，目標元素出現在可見範圍
        self.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop;", container, target)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_EVValue_div")))
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        with self.subTest():
            self.assertEqual(status, "-2", f"EV Value is {status}, not -2")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
     #----------------2025/08/26--------------------------------------------------------------------------

    def test_case031_Check_Evidence_HDR_WDR_Level(self):
        #到advance->exposure->Levels頁面HDR/WDR_Level
        self.go_to_advanced_page()
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
        self.assertEqual(status, "Level 1", f"EV Value is {status}, not Level 2")       
    
    def test_case032_Check_Evidence_3DNR_Level(self):
        #到advance->exposure->Levels頁面HDR/WDR_Level
        self.go_to_advanced_page()
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
        self.assertEqual(status, "Level 1", f"3D NR level is {status}, not Level 2")

    def test_case033_Check_Evidence_2DNR_Level(self):
        #到advance->exposure->Levels頁面HDR/WDR_Level
        self.go_to_advanced_page()
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
        self.assertEqual(status, "60%", f"2D NR level is {status}, not 60%")
    
    def test_case034_Check_ALPR_Brightness(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Brightness")))
        value = self.driver.find_element(By.ID, "input_Brightness").get_attribute('value')
        self.assertEqual(value, "40%", f"Brightness not 40%: {value}")

    def test_case035_Check_ALPR_Contrast(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Contrast")))
        value = self.driver.find_element(By.ID, "input_Contrast").get_attribute('value')
        self.assertEqual(value, "40%", f"Contrast not 40%: {value}")

    def test_case036_Check_ALPR_Saturation(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Saturation")))
        value = self.driver.find_element(By.ID, "input_Saturation").get_attribute('value')
        self.assertEqual(value, "40%", f"Saturation not 40%: {value}")

    def test_case037_Check_ALPR_Sharpness(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Sharpness")))
        value = self.driver.find_element(By.ID, "input_Sharpness").get_attribute('value')
        self.assertEqual(value, "40%", f"Sharpness not 40%: {value}")

    def test_case038_Check_ALPR_Gamma(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Gamma")))
        value = self.driver.find_element(By.ID, "input_Gamma").get_attribute('value')
        self.assertEqual(value, "40%", f"Gamma not 40%: {value}")
    
    def test_case039_Check_ALPR_Auto_wb_Mode(self):  
        self.go_to_ALPR_image_page()
        checkbox = self.driver.find_element(By.ID, "WhiteBalanceAuto")
        self.assertFalse(checkbox.is_selected(), "WhiteBalanceAuto is ON")

    def test_case040_Check_ALPR_Color_Temperature(self):
        self.go_to_ALPR_image_page()
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
        if current_temp == "4000":
            print("Color temperature is 4000K")
        else:
            self.fail(f"Color temperature is {current_temp}K, not 4000K")
        #等待三秒後切換回為ON，不能馬上切換，否則會失敗
        time.sleep(3)
        # 再點回 ON（恢復勾選）
        WebDriverWait(self.driver, 5).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "#div_WhiteBalance .slider"))
        ).click()
    
    #Case 41~43 檢查ALPR image configs頁面的設定
    def test_case041_Check_ALPR_RotateViewFlip(self):
        self.go_to_ALPR_image_configs_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_Flip_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_Flip_div").get_attribute("data-text")
        self.assertEqual(status, "Vertical", f"Flip is not Vertical, it's {status}")

    def test_case042_Check_ALPR_VideoOrientation(self):
        self.go_to_ALPR_image_configs_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_VideoOrientation_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_VideoOrientation_div").get_attribute("data-text")
        self.assertEqual(status, "90°", f"Video Orientation is not 90 degree, it's {status}")
    
    def test_case043_Check_ALPR_PowerLineSequence(self):
        self.go_to_ALPR_image_configs_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_PowerLineFrequency_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_PowerLineFrequency_div").get_attribute("data-text")
        self.assertEqual(status, "50Hz", f"Power line frequency is {status}, not 50Hz")

    #case44開始檢查exposure mode頁面的設定
    def test_case044_Check_ALPR_ExposureMode(self):
        #到Exposure頁面檢查ExposureMode
        self.go_to_ALPR_ExposureMode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_ExposureMode_div").get_attribute("data-text")
        self.assertEqual(status, "Center Metering", f"Exposure Mode is {status}, not Center Metering")

    def test_case045_Check_ALPR_AESpeed(self):
        #到Exposure頁面檢查AESpeed
        self.go_to_ALPR_ExposureMode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESpeed_div").get_attribute("data-text")
        self.assertEqual(status, "40%", f"AE Speed is {status}, not 50%")

    def test_case046_Check_ALPR_AESensitivity(self):
        #到Exposure頁面檢查AESensitivity
        self.go_to_ALPR_ExposureMode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESensitivity_div").get_attribute("data-text")
        self.assertEqual(status, "40%", f"AE Sensitivity is {status}, not 50%")
        
    def test_case047_Check_ALPR_Evidence_HDR_WDR(self):
        #到advance頁面檢查HDR/WDR
        self.go_to_ALPR_AdvancedSetting_page()
        status = self.driver.find_element(By.ID, "select_Image_WDRAndHDR_div").get_attribute("data-text")
        self.assertEqual(status, "WDR Only", f"HDR/WDR is {status}, not WDR Only")
    
    def test_case048_Check_ALPR_DigitalNoiseReduction(self):
        #到advance頁面檢查Digital Noise Reduction
        self.go_to_ALPR_AdvancedSetting_page()
        status = self.driver.find_element(By.ID, "select_Image_DigitalNoiseReduction_div").get_attribute("data-text")
        self.assertEqual(status, "2D NR", f"Digital Noise Reduction is {status}, not 3D NR")
    
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
        self.assertEqual(status, "Manual", f"Exposure Mode is {status}, not Manual")
    
    def test_case051_Check_ALPR_EV_Value(self):
        #到advance->exposure頁面檢查Auto的EV Value
        self.go_to_ALPR_AdvancedSetting_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        self.assertEqual(status, "-1", f"EV_Value is {status}, not -1")
    
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
        self.assertEqual(status, "1/1000s", f"Exposure Mode is {status}, not 1/1000s")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        self.assertEqual(status, "40%", f"Exposure Mode is {status}, not 40%")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        self.assertEqual(status, "-1", f"Exposure Mode is {status}, not -1")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        self.assertEqual(status, "1/200s", f"Min. Exposure Time is {status}, not 1/200s")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        self.assertEqual(status, "1/100s", f"Max. Exposure Time is {status}, not 1/60s")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        self.assertEqual(status, "20%", f"Min. Gain is {status}, not 20%")
        time.sleep(2)
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        self.assertEqual(status, "80%", f"Max. Gain is {status}, not 80%")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
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
        self.assertEqual(status, "-1", f"EV Value is {status}, not -1")
        #儲存設定
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "AS_button_Save")))
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case062_Check_ALPR_HDR_WDR_Level(self):
        #到advance->exposure->Levels頁面HDR/WDR_Level
        self.go_to_ALPR_AdvancedSetting_page()
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
        self.assertEqual(status, "Level 1", f"EV Value is {status}, not Level 2")
    
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
        self.assertEqual(status, "Level 1", f"3D NR level is {status}, not Level 2")

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
        self.assertEqual(status, "40%", f"2D NR level is {status}, not 40%")

    #case65開始確認camera information
    def test_case065_Check_Manufacturer(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Manufacturer名稱
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "span_Device_Brand")))
        Manufacturer = self.driver.find_element(By.ID,"span_Device_Brand").text
        self.assertEqual(Manufacturer, "Safe Fleet", f"Manufacturer is {Manufacturer}, not Safe Fleet")
    
    #確認model name
    def test_case066_Check_Model(self):
        #進入system頁面
        self.go_to_system_page()
        #定位model名稱
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "span_Device_Model")))
        model = self.driver.find_element(By.ID,"span_Device_Model").text
        self.assertEqual(model, "Focus-25-00-01", f"model is {model}, not Focus-25-00-01")
    
    #確認Firmware Version
    def test_case067_Check_FirmwareVersion(self):   
        #讀取config ini檔
        config = configparser.ConfigParser()
        config.read(r'D:/AutoTest/config.ini')
        Version = config['Version_Config']['version']
        #進入system頁面
        self.go_to_system_page()
        #定位firmware Version
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "span_Device_FWVersion")))
        FirmwareVersion = self.driver.find_element(By.ID,"span_Device_FWVersion").text
        self.assertEqual(FirmwareVersion, Version, f"FirmwareVersion is {FirmwareVersion}, not {Version}")
    
    #確認Camera Name
    def test_case068_Check_CameraName(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Camera Name欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CameraName")))
        CameraName = self.driver.title #該camera name名稱是綁定driver.title名稱
        self.assertEqual(CameraName, "Focus-25-00-02", f"CameraName is {CameraName}, not Focus-25-00-01")
    
    #確認Config Version 
    def test_case069_Check_ConfigVersion(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Config Version 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_ConfigVersion")))
        ConfigVersion =  self.driver.find_element(By.ID, "input_ConfigVersion").get_attribute("value")
        self.assertEqual(ConfigVersion, "1.0.1", f"Config Version is {ConfigVersion}, not 1.0.0")

    #確認Date Format
    def test_case070_Check_DateFormat(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Time Format 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Device_TimeFormat_div")))
        DateFormat =  self.driver.find_element(By.ID, "select_Device_TimeFormat_div").get_attribute("data-text")
        self.assertEqual(DateFormat, "YMD", f"Time Format is {DateFormat}, not YMD")
    
    #確認Time Format
    def test_case071_Check_TimeFormat(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Time Format 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Device_input_TimeFormat_24Hour")))
        # 讀取配置文件
        config = configparser.ConfigParser()
        config.read(r'D:/AutoTest/config.ini')
        URL = config['URL_Config']['URL']
        #該ratio button不是checkbox，因此不能用is_selected()
        #是用圖判斷，圖是存在src屬性內，因此是判斷src屬性是哪一張圖。
        radio_12 = self.driver.find_element(By.ID, "24hour")
        src_value = radio_12.get_attribute("src")
        print(src_value)
        if URL + "/from_temp/res/img/Content/System_Device/bt-storage-check-2-pre.png" in src_value:
            print("24-hour is selected")
        else:
            self.fail("24-hour is not selected")
    
    #確認Time Zone
    def test_case072_Check_Timezone(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Time Zone 欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Device_TimeZone_div")))
        TimeZone =  self.driver.find_element(By.ID, "select_Device_TimeZone_div").get_attribute("data-text")
        self.assertEqual(TimeZone, "(UTC+08:00) Taiwan", f"Time Zone is {TimeZone}, not (UTC+08:00) Taiwan")

    #確認Daylight Saving
    def test_case073_Check_DaylightSaving(self):
        #進入system頁面
        self.go_to_system_page()
        #定位Daylight Saving欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Daylight")))
        DaylightSaving = self.driver.find_element(By.ID, "Daylight")
        self.assertFalse(DaylightSaving.is_selected(),"Daylight saving is enabled")
    
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
    
    #確認Evidence Stream的Resolution
    def test_case076_Check_Evidence_Resolution(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位resolution
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainResolution_div")))
        resolution= self.driver.find_element(By.ID, "select_Stream_MainResolution_div").get_attribute("data-text")
        self.assertEqual(resolution, "1280x720(16:9)", f"Resolution is {resolution}, not 1280x720(16:9)")
    
    #確認Evidence Stream的Resolution
    def test_case077_Check_Evidence_StreamFormat(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位StreamFormat
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainStreamFormat_div")))
        StreamFormat= self.driver.find_element(By.ID, "select_Stream_MainStreamFormat_div").get_attribute("data-text")
        self.assertEqual(StreamFormat, "H.265", f"Stream Format is {StreamFormat}, not H.265")
    
    #確認Evidence Stream的FrameRate
    def test_case078_Check_Evidence_FrameRate(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位FrameRate
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainFrameRate_div")))
        FrameRate= self.driver.find_element(By.ID, "select_Stream_MainFrameRate_div").get_attribute("data-text")
        self.assertEqual(FrameRate, "25", f"Stream Format is {FrameRate}, not 25")
    
    #確認Evidence Stream的Overlay
    def test_case079_Check_Evidence_Overlay(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位overlay
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_Overlay")))
        Overlay= self.driver.find_element(By.ID, "switch_Overlay")
        self.assertFalse(Overlay.is_selected(),"Overlay is enabled")
    
    #確認Evidence Stream的URL String
    def test_case080_Check_Evidence_URL_String(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位URL String
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Stream_URLString")))
        URL_String= self.driver.find_element(By.ID, "input_Stream_URLString").get_attribute("value")
        self.assertEqual(URL_String, "stream111", f"URL Stream is {URL_String}, not stream111")

    #確認Evidence Stream的Audio Format
    def test_case081_Check_Evidence_AudioFormat(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位Audio Format
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainAudioFormat_div")))
        AudioFormat= self.driver.find_element(By.ID, "select_Stream_MainAudioFormat_div").get_attribute("data-text")
        self.assertEqual(AudioFormat, "PCM", f"Audio Format is {AudioFormat}, not PCM")
    
    #確認Evidence Stream的Rate Control
    def test_case082_Check_Evidence_RateControl(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位Audio Format
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "MainStreamVBR")))
        button = self.driver.find_element(By.ID, "MainStreamVBR")
        bg_color = button.value_of_css_property("background-color")
        print(bg_color)
        if bg_color == "rgba(75, 93, 118, 1)":
            print("Rate Control is VBR")
        else:
            self.fail("Rate Control is not VBR")
    
    #確認Evidence Stream的Video Quality
    def test_case083_Check_Evidence_VideoQuality(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位Target Rate
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainVideoQuality_div")))
        VideoQuality= self.driver.find_element(By.ID, "select_Stream_MainVideoQuality_div").get_attribute("data-text")
        self.assertEqual(VideoQuality, "High", f"Video Quality is {VideoQuality}, not High")
    
    #確認Evidence Stream的GOP Length
    def test_case084_Check_Evidence_GOP_Length(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #定位GOP Length
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainGOPLength_div")))
        GOP_Length= self.driver.find_element(By.ID, "select_Stream_MainGOPLength_div").get_attribute("data-text")
        self.assertEqual(GOP_Length, "60", f"GOP Length is {GOP_Length}, not 60")

    #確認Evidence Live的Resolution
    def test_case086_Check_Evidence_Live_Resolution(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位resolution
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainResolution_div")))
        resolution= self.driver.find_element(By.ID, "select_Stream_MainResolution_div").get_attribute("data-text")
        self.assertEqual(resolution, "848x480(16:9)", f"Resolution is {resolution}, not 848x480(16:9)")
    
    
    #確認Evidence Live的Stream format
    def test_case087_Check_Evidence_Live_StreamFormat(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位StreamFormat
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainStreamFormat_div")))
        StreamFormat= self.driver.find_element(By.ID, "select_Stream_MainStreamFormat_div").get_attribute("data-text")
        self.assertEqual(StreamFormat, "H.265", f"Stream Format is {StreamFormat}, not H.265")
    
    #確認Evidence Live的FrameRate
    def test_case088_Check_Evidence_Live_FrameRate(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        time.sleep(1) #等待更新
        #定位FrameRate
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainFrameRate_div")))
        FrameRate= self.driver.find_element(By.ID, "select_Stream_MainFrameRate_div").get_attribute("data-text")
        self.assertEqual(FrameRate, "20", f"Stream Format is {FrameRate}, not 20")
    
    #確認Evidence Live的Overlay
    def test_case089_Check_Evidence__Live_Overlay(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位overlay
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_Overlay")))
        Overlay= self.driver.find_element(By.ID, "switch_Overlay")
        self.assertFalse(Overlay.is_selected(),"Overlay is enabled")
    
    #確認Evidence Live的URL String
    def test_case090_Check_Evidence_Live_URL_String(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
         #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        time.sleep(1)  # 等待value更新，DOM 更新有延遲，加一個等待就能解決：
        #定位URL String
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Stream_URLString")))
        URL_String= self.driver.find_element(By.ID, "input_Stream_URLString").get_attribute("value")
        self.assertEqual(URL_String, "stream222", f"URL Stream is {URL_String}, not stream222")

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
        self.assertEqual(AudioFormat, "PCM", f"Audio Format is {AudioFormat}, not PCM")
    
    #確認Evidence Live的Rate Control
    def test_case092_Check_Evidence_Live_RateControl(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位Audio Format
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "MainStreamVBR")))
        button = self.driver.find_element(By.ID, "MainStreamVBR")
        bg_color = button.value_of_css_property("background-color")
        print(bg_color)
        if bg_color == "rgba(75, 93, 118, 1)":
            print("Rate Control is VBR")
        else:
            self.fail("Rate Control is not VBR")
    
    #確認Evidence Live的Target Rate
    def test_case093_Check_Evidence_Live_VideoQuality(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        time.sleep(1)  # 等待value更新，DOM 更新有延遲，加一個等待就能解決：
        #定位Target Rate
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainVideoQuality_div")))
        VideoQuality= self.driver.find_element(By.ID, "select_Stream_MainVideoQuality_div").get_attribute("data-text")
        self.assertEqual(VideoQuality, "High", f" Video Quality is {VideoQuality}, not High")
    
    #確認Evidence Live的GOP Length
    def test_case094_Check_Evidence_Live_GOP_Length(self):
        #進入stream config頁面
        self.go_to_stream_config_page()
        #點擊evidence live
        self.driver.find_element(By.ID, "SC_span_Second").click()
        #定位GOP Length 
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Stream_MainGOPLength_div")))
        GOP_Length= self.driver.find_element(By.ID, "select_Stream_MainGOPLength_div").get_attribute("data-text")
        self.assertEqual(GOP_Length, "60", f"GOP Length is {GOP_Length}, not 60")

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
    
    #確認overlay front size
    def test_case106_Check_Overlay_FontSize(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Overlay_FontSize_div")))
        FontSize= self.driver.find_element(By.ID, "select_Overlay_FontSize_div").get_attribute("data-text")
        self.assertEqual(FontSize,"Large",f"Font Size is {FontSize}, not Large")
    
     #確認overlay Font Color開關
    def test_case107_Check_Overlay_FontColor(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_Overlay_Font")))
        FontColor= self.driver.find_element(By.ID, "switch_Overlay_Font")
        self.assertFalse(FontColor.is_selected(),"Front Color is enabled")
    
    #確認overlay background Color開關
    def test_case108_Check_Overlay_BackgroundColor(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "switch_Overlay_BackgroundColor")))
        BackgroundColor= self.driver.find_element(By.ID, "switch_Overlay_BackgroundColor")
        self.assertFalse(BackgroundColor.is_selected(),"Background Color is enabled")
    
     #確認overlay Date and Time開關
    def test_case109_Check_Overlay_DateandTime_Switch(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "TimeEnable")))
        DateandTime= self.driver.find_element(By.ID, "TimeEnable")
        self.assertTrue(DateandTime.is_selected(),"Date and Time is not enabled")
    
    #確認overlay Date and Time的format
    def test_case110_Check_Overlay_DateandTime_Format(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Overlay_DateTimeFormat_div")))
        DateandTime_Format= self.driver.find_element(By.ID, "select_Overlay_DateTimeFormat_div").get_attribute("data-text")
        self.assertEqual(DateandTime_Format,"Date",f"format is {DateandTime_Format},not Date")
        
    #確認overlay Date and Time的Position
    def test_case111_Check_Overlay_DateandTime_Position(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Overlay_DataTimePosition_div")))
        DateandTime_Position= self.driver.find_element(By.ID, "select_Overlay_DataTimePosition_div").get_attribute("data-text")
        self.assertEqual(DateandTime_Position,"Bottom-Right",f"Date and Time Position is {DateandTime_Position},not Bottom-Right")
    
     #確認overlay Camera Name開關
    def test_case112_Check_Overlay_CameraName_Switch(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "TextEnable")))
        CameraName= self.driver.find_element(By.ID, "TextEnable")
        self.assertTrue(CameraName.is_selected(),"Camera Name is not enabled")
    
    #確認overlay Camera Name的Position
    def test_case113_Check_Overlay_CameraName_Position(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Overlay_CameraNamePosition_div")))
        CameraName_Position= self.driver.find_element(By.ID, "select_Overlay_CameraNamePosition_div").get_attribute("data-text")
        self.assertEqual(CameraName_Position,"Bottom-Right",f"Camera Name Position is {CameraName_Position},not Bottom-Right")
    
    #確認overlay Font Color text1開關
    def test_case114_Check_Overlay_textOverlay_text1(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_1")))
        text1= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_1")
        self.assertTrue(text1.is_selected(),"text1 is not enabled")
    
    #確認overlay Font Color開關
    def test_case115_Check_Overlay_textOverlay_text2(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_2")))
        text2= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_2")
        self.assertTrue(text2.is_selected(),"text2 is not enabled")
    
    #確認overlay Font Color開關
    def test_case116_Check_Overlay_textOverlay_text3(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_3")))
        text3= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_3")
        self.assertTrue(text3.is_selected(),"text3 is not enabled")
    
    #確認overlay Font Color開關
    def test_case117_Check_Overlay_textOverlay_text4(self):
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #檢查開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_4")))
        text4= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_4")
        self.assertTrue(text4.is_selected(),"text4 is not enabled")
    
    def test_case118_Check_Overlay_textOverlay_text1_FreeText(self):
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
            self.assertEqual(FreeText1,"Free Text 111",f"Free Text is {FreeText1}, not Free Text 111")
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
    
    def test_case119_Check_Overlay_textOverlay_text2_FreeText(self):
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
            self.assertEqual(FreeText2,"Free Text 222",f"Free Text is {FreeText2}, not Free Text 222")
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
    
    def test_case120_Check_Overlay_textOverlay_text3_FreeText(self):
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
            self.assertEqual(FreeText3,"Free Text 333",f"Free Text is {FreeText3}, not Free Text 333")
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
    
    def test_case121_Check_Overlay_textOverlay_text4_FreeText(self):
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
            self.assertEqual(FreeText4,"Free Text 444",f"Free Text is {FreeText4}, not Free Text 444")
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
    
    #檢查Text Overlay text1的position
    def test_case122_Check_Overlay_textOverlay_text1_Position(self):
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
        #檢查position
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Overlay_Text_1_Position_div")))
        Position1= self.driver.find_element(By.ID, "select_Overlay_Text_1_Position_div").get_attribute("data-text")
        try:
            self.assertEqual(Position1,"Bottom-Right",f"Position1 is {Position1}, not Bottom-Right")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))  
        #關閉text1
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
    
    #檢查Text Overlay text2的position
    def test_case123_Check_Overlay_textOverlay_text2_Position(self):
        self.errors = []  # 一開始先建立 list
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #點擊text overlay tab
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_div_TextOverlay_Selector")))
        self.driver.find_element(By.ID, "Overlay_div_TextOverlay_Selector").click()
        #開啟text1
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_2")))
        checkbox= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_2")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_2 .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #檢查position
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Overlay_Text_2_Position_div")))
        Position2= self.driver.find_element(By.ID, "select_Overlay_Text_2_Position_div").get_attribute("data-text")
        try:
            self.assertEqual(Position2,"Bottom-Right",f"Position2 is {Position2}, not Bottom-Right")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))  
        #關閉text2
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
    
    #檢查Text Overlay text3的position
    def test_case124_Check_Overlay_textOverlay_text3_Position(self):
        self.errors = []  # 一開始先建立 list
        #進入overlay頁面
        self.go_to_Systme_Overlay_page()
        #點擊text overlay tab
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_div_TextOverlay_Selector")))
        self.driver.find_element(By.ID, "Overlay_div_TextOverlay_Selector").click()
        #開啟text1
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Overlay_input_checkbox_Text_3")))
        checkbox= self.driver.find_element(By.ID, "Overlay_input_checkbox_Text_3")
        slider = self.driver.find_element(By.CSS_SELECTOR, "#Overlay_TextOverlay_Table_3 .slider")
        if not checkbox.is_selected():
            slider.click()
        time.sleep(1)#等待元素就位
        #檢查position
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Overlay_Text_3_Position_div")))
        Position3= self.driver.find_element(By.ID, "select_Overlay_Text_3_Position_div").get_attribute("data-text")
        try:
            self.assertEqual(Position3,"Bottom-Right",f"Position3 is {Position3}, not Bottom-Right")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))  
        #關閉text3
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
    
    #檢查Text Overlay text4的position
    def test_case125_Check_Overlay_textOverlay_text4_Position(self):
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
        #檢查position
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Overlay_Text_4_Position_div")))
        Position4= self.driver.find_element(By.ID, "select_Overlay_Text_4_Position_div").get_attribute("data-text")
        try:
            self.assertEqual(Position4,"Bottom-Right",f"Position4 is {Position4}, not Bottom-Right")
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))  
        #關閉text3
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
    
     #檢查system->Audio設定
    def test_case126_Check_System_Microphone(self):
        #進入audio頁面
        self.go_to_Systme_Audio_page()
        #檢查Microphone開關
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "DisableMic")))
        Microphone = self.driver.find_element(By.ID, "DisableMic")
        self.assertTrue(Microphone.is_selected(),"Microphone switch is off")
    
     #檢查system->Audio Microphone音量
    def test_case127_Check_System_Volume(self):
        #進入audio頁面
        self.go_to_Systme_Audio_page()
        #檢查Volume
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Audio_MicVolume_div")))
        Volume = self.driver.find_element(By.ID, "select_Audio_MicVolume_div").get_attribute("data-text")
        self.assertEqual(Volume,"60%",f"Volume is {Volume}, not 60%")
    
     #檢查basic的網路設定，檢查Type
    def test_case128_Check_Network_Basic_Type(self):
        #進入basic頁面
        self.go_to_Network_Basic_page()
        #檢查Type
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Basic_NetworkType_div")))
        Type = self.driver.find_element(By.ID, "select_Basic_NetworkType_div").get_attribute("data-text")
        self.assertEqual(Type,"DHCP IPv4",f"Type is {Type}, not DHCP IPv4")
    
     #檢查basic的網路設定，檢查Retry Interval
    def test_case129_Check_Network_RetryInterval(self):
        #進入basic頁面
        self.go_to_Network_Basic_page()
        #檢查Retry Interval
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "RetryInterval")))
        RetryInterval = self.driver.find_element(By.ID, "RetryInterval").get_attribute("value")
        self.assertEqual(RetryInterval,"25s",f"Retry Interval is {RetryInterval}, not 25s")
    
     #檢查basic的網路設定，檢查Fallback IP
    def test_case130_Check_Network_FallbackIP(self):
        #進入basic頁面
        self.go_to_Network_Basic_page()
        #檢查Fallback IP
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_Basic_DefaultIP_div")))
        FallbackIP = self.driver.find_element(By.ID, "select_Basic_DefaultIP_div").get_attribute("data-text")
        self.assertEqual(FallbackIP,"Use Last Known IP Address From DHCP Server",f"Fallback IP {FallbackIP}, not Use Last Known IP Address From DHCP Server")
    
    #檢查advanced的網路設定，檢查WS Discovery
    def test_case131_Check_Network_WS_Discovery(self):
        #進入advanced頁面
        self.go_to_Network_Advanced_page()
        #檢查WS Discovery
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "DisableWSDiscovery")))
        checkbox = self.driver.find_element(By.ID, "DisableWSDiscovery")
        self.assertFalse(checkbox.is_selected(),"WS_Discovery is on")
    
    #檢查advanced的網路設定，檢查mDNS
    def test_case132_Check_Network_mDNS(self):
        #進入advanced頁面
        self.go_to_Network_Advanced_page()
        #檢查mDNS
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "DisablemDNS")))
        checkbox = self.driver.find_element(By.ID, "DisablemDNS")
        self.assertFalse(checkbox.is_selected(),"mDNS is on")
    
    #檢查advanced的網路設定，檢查HTTP/HTTPS Server
    def test_case133_Check_Network_HTTP_HTTPS_Server(self):
        #進入advanced頁面
        self.go_to_Network_Advanced_page()
        #檢查HTTP/HTTPS Server
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Network_Advanced_input_HTTPHTTPS_Encyption_Enable")))
        checkbox = self.driver.find_element(By.ID, "Network_Advanced_input_HTTPHTTPS_Encyption_Enable")
        self.assertFalse(checkbox.is_selected(),"HTTP/HTTPS is on")
    
    #檢查advanced的網路設定，檢查HTTP/HTTPS Server port
    def test_case134_Check_Network_HTTP_HTTPS_Server_Port(self):
        #進入advanced頁面
        self.go_to_Network_Advanced_page()
        #檢查HTTP/HTTPS Server Port
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Network_Advanced_input_HTTPSServer_Port")))
        Port = self.driver.find_element(By.ID, "Network_Advanced_input_HTTPSServer_Port").get_attribute("value")
        self.assertEqual(Port,"80",f"Port is not 80, it's {Port}")
    
    #檢查advanced的網路設定，檢查RTSP Server port
    def test_case135_Check_Network_RTSP_Server_Port(self):
        #進入advanced頁面
        self.go_to_Network_Advanced_page()
        #檢查RTSP Server Port
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Network_Advanced_input_RTSPServer_Port")))
        Port = self.driver.find_element(By.ID, "Network_Advanced_input_RTSPServer_Port").get_attribute("value")
        self.assertEqual(Port,"49152",f"Port is not 49152, it's {Port}")
    
    #檢查Notification設定，檢查Log File Size
    def test_case136_Check_Notification_LogFileSize(self):
        #進入Notification頁面
        self.go_to_Notification_page()
        #檢查Log File Size
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CameraLog_input_Size")))
        Size = self.driver.find_element(By.ID, "CameraLog_input_Size").get_attribute("value")
        self.assertEqual(Size,"64",f"Port is not 64, it's {Size}")
    
    #檢查Notification設定，檢查Device log
    def test_case137_Check_Notification_Devicelog(self):
        #進入Notification頁面
        self.go_to_Notification_page()
        #檢查Device log
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CameraLog_input_DeviceLog")))
        checkbox = self.driver.find_element(By.ID, "CameraLog_input_DeviceLog")
        self.assertFalse(checkbox.is_selected(),"Device log is enabled")
    
    #檢查Notification設定，檢查Access log
    def test_case138_Check_Notification_Accesslog(self):
        #進入Notification頁面
        self.go_to_Notification_page()
        #檢查Access Log
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "CameraLog_input_AccessLog")))
        checkbox = self.driver.find_element(By.ID, "CameraLog_input_AccessLog")
        self.assertFalse(checkbox.is_selected(),"Access log is enabled")
    
    #檢查Storage設定，檢查Auto Format
    def test_case139_Check_Storage_AutoFormat(self):
        #進入storage頁面
        self.go_to_Storage_page()
        #檢查Auto Format
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "checkbox_AutoFormat")))
        checkbox = self.driver.find_element(By.ID, "checkbox_AutoFormat")
        self.assertFalse(checkbox.is_selected(),"Auto Format is enabled")
    
     #檢查Administration設定，檢查SSH Server
    def test_case140_Check_SSH_Server(self):
        #進入Administration頁面
        self.go_to_Administration_page()
        #檢查SSH
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Admin_input_SSH_OnOffSwitch")))
        checkbox = self.driver.find_element(By.ID, "Admin_input_SSH_OnOffSwitch")
        self.assertFalse(checkbox.is_selected(),"SSH Server is enabled")
    
    
    #檢查Administration設定，檢查SSH Server Port
    def test_case141_Check_SSH_Server_Port(self):
        self.errors = []  # 一開始先建立 list，用來暫存false
        #進入Administration頁面
        self.go_to_Administration_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Admin_input_SSH_OnOffSwitch")))
        checkbox = self.driver.find_element(By.ID, "Admin_input_SSH_OnOffSwitch")
        slider =  self.driver.find_element(By.CSS_SELECTOR, "#Admin_input_SSH_OnOffSwitch + .slider")
        if not checkbox.is_selected():
            slider.click()
        #檢查SSH 
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Admin_input_Port")))
        Port = self.driver.find_element(By.ID, "Admin_input_Port").get_attribute("value")
        try:
            self.assertEqual(Port,"50000",f"SSH Port is {Port}, not 50000" )
        except AssertionError as e:
            print("Assertion failed:", e)
            self.errors.append(str(e))
        #關閉SSH
        if checkbox.is_selected():
            slider.click()
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "adminSave")
        SaveButton.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1)
         # 最後統一檢查是否有錯
        if self.errors:
         raise AssertionError("\n".join(self.errors))
    
    #確認Auth. Method
    def test_case142_Check_SSH_AuthMethod(self):
        self.errors = []  # 一開始先建立 list，用來暫存false
        #進入Administration頁面
        self.go_to_Administration_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Admin_input_SSH_OnOffSwitch")))
        checkbox = self.driver.find_element(By.ID, "Admin_input_SSH_OnOffSwitch")
        slider =  self.driver.find_element(By.CSS_SELECTOR, "#Admin_input_SSH_OnOffSwitch + .slider")
        #開啟SSH
        if not checkbox.is_selected():
            slider.click()
        #定位欄位
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "SSHServer_Password")))
        # 讀取配置文件
        config = configparser.ConfigParser()
        config.read(r'D:/AutoTest/config.ini')
        URL = config['URL_Config']['URL']
        #該ratio button不是checkbox，因此不能用is_selected()
        #是用圖判斷，圖是存在src屬性內，因此是判斷src屬性是哪一張圖。
        password = self.driver.find_element(By.ID, "SSHServer_Password")
        src_value = password.get_attribute("src")
        print(src_value)
        if URL + "/from_temp/res/img/Content/System_Device/bt-storage-check-2-pre.png" in src_value:
            print("password is selected")
        else:
            self.errors.append("password is not selected")
        #關閉SSH
        if checkbox.is_selected():
            slider.click()
         #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "adminSave")
        SaveButton.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))
        time.sleep(1)
         # 最後統一檢查是否有錯
        if self.errors:
         raise AssertionError("\n".join(self.errors))
    
    def test_case143_Check_Evidence_Priority_ExposureAuto_off_ExposureTime(self):
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
            self.assertEqual(ExposureTime,"1/1000s",f"Exposure Time is {ExposureTime}, not 1/1000s" )
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
    
    def test_case144_Check_Evidence_Priority_GainAuto_off_GainValue(self):
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
            self.assertEqual(GainValue,"40%",f"Gain Value is {GainValue}, not 40%" )
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
        
    def test_case145_Check_ALPR_Priority_ExposureAuto_off_ExposureTime(self):
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
            self.assertEqual(ExposureTime,"1/1000s",f"Exposure Time is {ExposureTime}, not 1/1000s" )
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
    
    def test_case146_Check_ALPR_Priority_GainAuto_off_GainValue(self):
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
            self.assertEqual(GainValue,"40%",f"Gain Value is {GainValue}, not 40%" )
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
