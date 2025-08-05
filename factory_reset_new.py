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
        config.read(r'D:/selenium project/config.ini')
        URL = config['URL_Config']['URL']
        username = config['Login_Config']['username']
        password = config['Login_Config']['password']

        #到URL網頁輸入帳號密碼並登入
        cls.driver.get(URL)
        WebDriverWait(cls.driver, 10).until(EC.presence_of_element_located((By.ID, "div_SignIn_Username"))).send_keys(username)
        cls.driver.find_element(By.ID, "div_SignIn_Password").send_keys(password)
        cls.driver.find_element(By.ID, "button_SignIn_OK").click()
        WebDriverWait(cls.driver, 30).until(EC.presence_of_element_located((By.ID, "a_Image")))
    
    #每個test case間暫停兩秒
    def setUp(self):
        time.sleep(2)

    #到image頁面，到頁面後要等待兩秒，等待所有元素就位
    def go_to_image_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        elem = self.driver.find_element(By.ID, "a_Image")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_Image")))
        elem.click()
        time.sleep(2)

    #到image_config頁面
    def go_to_image_config_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_ImageConfigs"))).click()
        time.sleep(2)
    
    #到exposure_mode頁面
    def go_to_exposure_mode_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_ExposureMode"))).click()
        time.sleep(2)

    #到advanced頁面
    def go_to_advanced_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_AdvancedSetting"))).click()
        time.sleep(4)

    #case1~case8檢查image parameters頁面所有設定
    def test_case001_Check_Brightness(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Brightness")))
        value = self.driver.find_element(By.ID, "input_Brightness").get_attribute('value')
        self.assertEqual(value, "50%", f"Brightness not 50%: {value}")

    def test_case002_Check_Contrast(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Contrast")))
        value = self.driver.find_element(By.ID, "input_Contrast").get_attribute('value')
        self.assertEqual(value, "50%", f"Contrast not 50%: {value}")

    def test_case003_Check_Saturation(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Saturation")))
        value = self.driver.find_element(By.ID, "input_Saturation").get_attribute('value')
        self.assertEqual(value, "50%", f"Saturation not 50%: {value}")

    def test_case004_Check_Sharpness(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Sharpness")))
        value = self.driver.find_element(By.ID, "input_Sharpness").get_attribute('value')
        self.assertEqual(value, "50%", f"Sharpness not 50%: {value}")

    def test_case005_Check_Gamma(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Gamma")))
        value = self.driver.find_element(By.ID, "input_Gamma").get_attribute('value')
        self.assertEqual(value, "50%", f"Gamma not 50%: {value}")

    def test_case006_Check_Auto_wb_Mode(self):
        self.go_to_image_page()
        time.sleep(2)
        checkbox = self.driver.find_element(By.ID, "WhiteBalanceAuto")
        self.assertTrue(checkbox.is_selected(), "WhiteBalanceAuto is OFF")

    def test_case007_Check_Color_Temperature(self):
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
        if current_temp == "5000":
            print("Color temperature is 5000K")
        else:
            self.fail(f"Color temperature is {current_temp}K, not 5000K")
        #等待三秒後切換回為ON，不能馬上切換，否則會失敗
        time.sleep(3)
        # 再點回 ON（恢復勾選）
        WebDriverWait(self.driver, 5).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "#div_WhiteBalance .slider"))
        ).click()

    def test_case008_Check_LDC(self):
        self.go_to_image_page()
        checkbox = self.driver.find_element(By.ID, "LDC")
        self.assertFalse(checkbox.is_selected(), "LDC is ON")
         
        #Case9~Case12後開始檢查image config頁面的所有設定
    def test_case009_Check_RotateViewFlip(self):
        self.go_to_image_config_page()
        status = self.driver.find_element(By.ID, "select_ImagePara_Flip_div").get_attribute("data-text")
        self.assertEqual(status, "Off", f"Flip is not off, it's {status}")

    def test_case010_Check_VideoOrientation(self):
        self.go_to_image_config_page()
        status = self.driver.find_element(By.ID, "select_ImagePara_VideoOrientation_div").get_attribute("data-text")
        self.assertEqual(status, "0°", f"Video Orientation is not 0 degree, it's {status}")

    def test_case011_Check_DIS(self):
        self.go_to_image_config_page()
        checkbox = self.driver.find_element(By.ID, "checkbox_DIS")
        self.assertFalse(checkbox.is_selected(), "DIS is ON")

    def test_case012_Check_PowerLineSequence(self):
        self.go_to_image_config_page()
        status = self.driver.find_element(By.ID, "select_ImagePara_PowerLineFrequency_div").get_attribute("data-text")
        self.assertEqual(status, "60Hz", f"Power line frequency is {status}, not 60Hz")

        #case13開始檢查exposure mode頁面的設定
    def test_case013_Check_ExposureMode(self):
        #到Exposure頁面檢查ExposureMode
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_ExposureMode_div").get_attribute("data-text")
        self.assertEqual(status, "Multi Metering", f"Exposure Mode is {status}, not Multi Metering")

    def test_case014_Check_AESpeed(self):
        #到Exposure頁面檢查AESpeed
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESpeed_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"AE Speed is {status}, not 50%")

    def test_case015_Check_AESensitivity(self):
        #到Exposure頁面檢查AESensitivity
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESensitivity_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"AE Sensitivity is {status}, not 50%")
    
    def test_case016_Check_HDR_WDR(self):
        #到advance頁面檢查HDR/WDR
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_Image_WDRAndHDR_div").get_attribute("data-text")
        self.assertEqual(status, "Both On", f"HDR/WDR is {status}, not Both On")
    
    def test_case017_Check_DigitalNoiseReduction(self):
        #到advance頁面檢查Digital Noise Reduction
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_Image_DigitalNoiseReduction_div").get_attribute("data-text")
        self.assertEqual(status, "3D NR", f"Digital Noise Reduction is {status}, not 3D NR")
    
    def test_case018_Check_FilterMode(self):
        #到advance頁面檢查FilterMode
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_AS_FilterMode_div").get_attribute("data-text")
        self.assertEqual(status, "Auto", f"FilterMode is {status}, not Auto")
    
    def test_case019_Check_BaseOn(self):
        #到advance頁面檢查BaseOn
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_AS_BaseOn_div").get_attribute("data-text")
        self.assertEqual(status, "Light Sensor", f"FilterMode is {status}, not Light Sensor")
    
    def test_case020_Check_LightLevel(self):
        #到advance頁面檢查LightLevel
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_AS_LightLevel_div").get_attribute("data-text")
        self.assertEqual(status, "Level 3", f"FilterMode is {status}, not Level 3")
    
    def test_case021_Check_DetectionInterval(self):
         #到advance頁面檢查DetectionInterval
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_AS_DetectionInterval_div").text
        self.assertEqual(status, "5s", f"FilterMode is {status}, not 5s")
    
    def test_case022_Check_SmartIR(self):
         #到advance頁面檢查SmartIR
        self.go_to_advanced_page()
        checkbox = self.driver.find_element(By.ID, "AS_input_IRIntensityAuto")
        self.assertTrue(checkbox.is_selected(), "SmartIR is off")
    
    def test_case023_Check_SmartIR_Value(self):
         #到advance頁面檢查SmartIR關閉後的預設值
        self.go_to_advanced_page()
        checkbox = self.driver.find_element(By.ID, "AS_input_IRIntensityAuto")
        slider = self.driver.find_element(By.CSS_SELECTOR, "span.slider.round")     
        #判斷是否開啟，有開的話要關閉
        if checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)  # 使用javascript強制點擊 checkbox，因為checkbox和slider不能直接互動
            WebDriverWait(self.driver, 10).until(
            lambda x: not checkbox.is_selected()
            )
        time.sleep(2) #等待兩秒確定狀態已更新
        SmartIR_Value =  self.driver.find_element(By.ID, "select_AS_IRIntensityValue_div").get_attribute("data-text")
        self.assertEqual(SmartIR_Value, "50%" , f"Smart IR Value is not 50%, It's {SmartIR_Value}")
            # 更新 checkbox 元素狀態
        checkbox = self.driver.find_element(By.ID, "AS_input_IRIntensityAuto")
        if not checkbox.is_selected(): #將slider還原
            self.driver.execute_script("arguments[0].click();", checkbox)  # 使用javascript強制點擊 checkbox，因為checkbox和slider不能直接互動
            WebDriverWait(self.driver, 10).until(
            lambda x: checkbox.is_selected()
            )
        time.sleep(1)
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case024_Check_TDN_Sync(self):
         #到advance頁面檢查TDN Sync
        self.go_to_advanced_page()
        checkbox = self.driver.find_element(By.ID, "AS_input_ICRSync")
        self.assertFalse(checkbox.is_selected(), "TDN Sync is on")
    
    def test_case025_Check_ExposureMode(self):
        #到advance->exposure頁面檢查Exposure Mode
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        status = self.driver.find_element(By.ID, "select_AS_ExposureMode_div").get_attribute("data-text")
        self.assertEqual(status, "Auto", f"Exposure Mode is {status}, not Auto")
    
    def test_case026_Check_EV_Value(self):
        #到advance->exposure頁面檢查EV Value
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        self.assertEqual(status, "0", f"Exposure Mode is {status}, not 0")
    
    def test_case027_Check_ExposureTime(self):
        #到advance->exposure頁面檢查ExposureTime
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        time.sleep(3) #等待切換完成
        #檢查ExposureTime
        status = self.driver.find_element(By.ID, "select_AS_ExposureTime_div").get_attribute("data-text")
        self.assertEqual(status, "1/60s", f"Exposure Mode is {status}, not 1/60s")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)
    
    def test_case028_Check_GainValue(self):
        #到advance->exposure頁面檢查ExposureTime
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        time.sleep(3) #等待切換完成
        #檢查Gain Value
        status = self.driver.find_element(By.ID, "select_AS_GainValue_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"Exposure Mode is {status}, not 50%")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    def test_case029_Check_GainValue(self):
        #到advance->exposure頁面檢查ExposureTime
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        time.sleep(3) #等待切換完成
        #檢查EV Value
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        self.assertEqual(status, "0", f"Exposure Mode is {status}, not 0")
        #儲存設定
        SaveButton =  self.driver.find_element(By.ID, "AS_button_Save")
        SaveButton.click()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/SeleniumProject/test_reports'))
