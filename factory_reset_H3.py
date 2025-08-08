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

    #到image_config頁面
    def go_to_image_config_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_ImageConfigs"))).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
    
    #到exposure_mode頁面
    def go_to_exposure_mode_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_ExposureMode"))).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading")))#等待loading消失

    #到advanced頁面
    def go_to_advanced_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_Image")))
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_AdvancedSetting"))).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
    
    #到system頁面->Device頁面
    def go_to_system_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "a_System")))
        elem = self.driver.find_element(By.ID, "a_System")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "a_System")))
        elem.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "maskLoading"))) #等待loading消失
    
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
    

    #case1~case8檢查image parameters頁面所有設定
    def test_case001_Check_Evidence_Brightness(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Brightness")))
        value = self.driver.find_element(By.ID, "input_Brightness").get_attribute('value')
        self.assertEqual(value, "50%", f"Brightness not 50%: {value}")

    def test_case002_Check_Evidence_Contrast(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Contrast")))
        value = self.driver.find_element(By.ID, "input_Contrast").get_attribute('value')
        self.assertEqual(value, "50%", f"Contrast not 50%: {value}")

    def test_case003_Check_Evidence_Saturation(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Saturation")))
        value = self.driver.find_element(By.ID, "input_Saturation").get_attribute('value')
        self.assertEqual(value, "50%", f"Saturation not 50%: {value}")

    def test_case004_Check_Evidence_Sharpness(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Sharpness")))
        value = self.driver.find_element(By.ID, "input_Sharpness").get_attribute('value')
        self.assertEqual(value, "50%", f"Sharpness not 50%: {value}")

    def test_case005_Check_Evidence_Gamma(self):
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Gamma")))
        value = self.driver.find_element(By.ID, "input_Gamma").get_attribute('value')
        self.assertEqual(value, "50%", f"Gamma not 50%: {value}")

    def test_case006_Check_Evidence_Auto_wb_Mode(self):
        self.go_to_image_page()
        time.sleep(2)
        checkbox = self.driver.find_element(By.ID, "WhiteBalanceAuto")
        self.assertTrue(checkbox.is_selected(), "WhiteBalanceAuto is OFF")

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

    def test_case008_Check_Evidence_LDC(self):
        self.go_to_image_page()
        checkbox = self.driver.find_element(By.ID, "LDC")
        self.assertFalse(checkbox.is_selected(), "LDC is ON")
         
    #Case9~Case12後開始檢查image config頁面的所有設定
    def test_case009_Check_Evidence_RotateViewFlip(self):
        self.go_to_image_config_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_Flip_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_Flip_div").get_attribute("data-text")
        self.assertEqual(status, "Off", f"Flip is not off, it's {status}")

    def test_case010_Check_Evidence_VideoOrientation(self):
        self.go_to_image_config_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_VideoOrientation_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_VideoOrientation_div").get_attribute("data-text")
        self.assertEqual(status, "0°", f"Video Orientation is not 0 degree, it's {status}")
    
    def test_case011_Check_Evidence_ViewAngle(self):
        self.go_to_image_config_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_ViewAngle_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_ViewAngle_div").get_attribute("data-text")
        self.assertEqual(status, "Narrow", f"View Angle is {status}, not Narrow")

    def test_case012_Check_Evidence_PowerLineSequence(self):
        self.go_to_image_config_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_PowerLineFrequency_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_PowerLineFrequency_div").get_attribute("data-text")
        self.assertEqual(status, "60Hz", f"Power line frequency is {status}, not 60Hz")

    #case13開始檢查exposure mode頁面的設定
    def test_case013_Check_Evidence_ExposureMode(self):
        #到Exposure頁面檢查ExposureMode
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_ExposureMode_div").get_attribute("data-text")
        self.assertEqual(status, "Multi Metering", f"Exposure Mode is {status}, not Multi Metering")

    def test_case014_Check_Evidence_AESpeed(self):
        #到Exposure頁面檢查AESpeed
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESpeed_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"AE Speed is {status}, not 50%")

    def test_case015_Check_Evidence_AESensitivity(self):
        #到Exposure頁面檢查AESensitivity
        self.go_to_exposure_mode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESensitivity_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"AE Sensitivity is {status}, not 50%")
    
    def test_case016_Check_Evidence_HDR_WDR(self):
        #到advance頁面檢查HDR/WDR
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_Image_WDRAndHDR_div").get_attribute("data-text")
        self.assertEqual(status, "Both Off", f"HDR/WDR is {status}, not Both Off")
    
    def test_case017_Check_Evidence_DigitalNoiseReduction(self):
        #到advance頁面檢查Digital Noise Reduction
        self.go_to_advanced_page()
        status = self.driver.find_element(By.ID, "select_Image_DigitalNoiseReduction_div").get_attribute("data-text")
        self.assertEqual(status, "3D NR", f"Digital Noise Reduction is {status}, not 3D NR")
    
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
        self.assertEqual(status, "Auto", f"Exposure Mode is {status}, not Auto")
    
    def test_case020_Check_Evidence_EV_Value(self):
        #到advance->exposure頁面檢查Auto的EV Value
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        self.assertEqual(status, "0", f"Exposure Mode is {status}, not 0")
    
    def test_case021_Check_Evidence_ExposureTime(self):
        #到advance->exposure頁面檢查ExposureTime
        self.go_to_advanced_page()
        self.driver.find_element(By.ID, "AS_div_Exposure").click()
        time.sleep(1)
        #切換成manual
        self.driver.find_element(By.ID, "select_AS_ExposureMode_div").click()
        self.driver.find_element(By.XPATH,"//li[@data-val='Manual']").click()
        time.sleep(3) #等待切換完成
        #檢查ExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_ExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_ExposureTime_div").get_attribute("data-text")
        self.assertEqual(status, "1/60s", f"Exposure Mode is {status}, not 1/60s")
        #儲存設定
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
        time.sleep(3) #等待切換完成
        #檢查Gain Value
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_GainValue_div")))
        status = self.driver.find_element(By.ID, "select_AS_GainValue_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"Exposure Mode is {status}, not 50%")
        #儲存設定
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
        time.sleep(3) #等待切換完成
        #檢查EV Value
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_EVValue_div")))
        status = self.driver.find_element(By.ID, "select_AS_EVValue_div").get_attribute("data-text")
        self.assertEqual(status, "0", f"Exposure Mode is {status}, not 0")
        #儲存設定
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
        time.sleep(3) #等待切換完成
        #檢查ExposureAuto
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_ExposureAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_ExposureAuto")
        self.assertTrue(checkbox.is_selected(), "ExposureAuto is off")
        #儲存設定
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
        time.sleep(3) #等待切換完成
        #檢查MinExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MinExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_MinExposureTime_div").get_attribute("data-text")
        self.assertEqual(status, "1/60s", f"Min. Exposure Time is {status}, not 1/60s")
        #儲存設定
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
        time.sleep(3) #等待切換完成
        #檢查MaxExposureTime
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_AS_MaxExposureTime_div")))
        status = self.driver.find_element(By.ID, "select_AS_MaxExposureTime_div").get_attribute("data-text")
        self.assertEqual(status, "1/60s", f"Max. Exposure Time is {status}, not 1/60s")
        #儲存設定
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
        time.sleep(3) #等待切換完成
        #檢查GainAuto
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "AS_input_GainAuto")))
        checkbox = self.driver.find_element(By.ID, "AS_input_GainAuto")
        self.assertTrue(checkbox.is_selected(), "GainAuto is off")
        #儲存設定
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

    def test_case029_Check_Evidence_MaxGain(self):
        #到advance->exposure->Priority頁面檢查Max. Gain
        self.go_to_advanced_page()
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

    def test_case030_Check_Evidence_Priority_EV_Value(self):
        #到advance->exposure->Priority頁面檢查EV Value
        self.go_to_advanced_page()
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
    
    def test_case031_Check_Evidence_HDR_WDR_Level(self):
        #到advance->exposure->Levels頁面HDR/WDR_Level
        self.go_to_advanced_page()
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
        self.assertEqual(status, "Level 2", f"3D NR level is {status}, not Level 2")

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
        self.assertEqual(status, "50%", f"2D NR level is {status}, not Level 2")
    
    def test_case034_Check_ALPR_Brightness(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Brightness")))
        value = self.driver.find_element(By.ID, "input_Brightness").get_attribute('value')
        self.assertEqual(value, "50%", f"Brightness not 50%: {value}")

    def test_case035_Check_ALPR_Contrast(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Contrast")))
        value = self.driver.find_element(By.ID, "input_Contrast").get_attribute('value')
        self.assertEqual(value, "50%", f"Contrast not 50%: {value}")

    def test_case036_Check_ALPR_Saturation(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Saturation")))
        value = self.driver.find_element(By.ID, "input_Saturation").get_attribute('value')
        self.assertEqual(value, "50%", f"Saturation not 50%: {value}")

    def test_case037_Check_ALPR_Sharpness(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Sharpness")))
        value = self.driver.find_element(By.ID, "input_Sharpness").get_attribute('value')
        self.assertEqual(value, "50%", f"Sharpness not 50%: {value}")

    def test_case038_Check_ALPR_Gamma(self):
        self.go_to_ALPR_image_page()
        self.go_to_image_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "input_Gamma")))
        value = self.driver.find_element(By.ID, "input_Gamma").get_attribute('value')
        self.assertEqual(value, "50%", f"Gamma not 50%: {value}")
    
    def test_case039_Check_ALPR_Auto_wb_Mode(self):  
        self.go_to_ALPR_image_page()
        checkbox = self.driver.find_element(By.ID, "WhiteBalanceAuto")
        self.assertTrue(checkbox.is_selected(), "WhiteBalanceAuto is OFF")

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
    
    #Case 41~43 檢查ALPR image configs頁面的設定
    def test_case041_Check_ALPR_RotateViewFlip(self):
        self.go_to_ALPR_image_configs_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_Flip_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_Flip_div").get_attribute("data-text")
        self.assertEqual(status, "Off", f"Flip is not off, it's {status}")

    def test_case042_Check_ALPR_VideoOrientation(self):
        self.go_to_ALPR_image_configs_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_VideoOrientation_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_VideoOrientation_div").get_attribute("data-text")
        self.assertEqual(status, "0°", f"Video Orientation is not 0 degree, it's {status}")
    
    def test_case043_Check_ALPR_PowerLineSequence(self):
        self.go_to_ALPR_image_configs_page()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select_ImagePara_PowerLineFrequency_div")))
        status = self.driver.find_element(By.ID, "select_ImagePara_PowerLineFrequency_div").get_attribute("data-text")
        self.assertEqual(status, "60Hz", f"Power line frequency is {status}, not 60Hz")

    #case44開始檢查exposure mode頁面的設定
    def test_case044_Check_ALPR_ExposureMode(self):
        #到Exposure頁面檢查ExposureMode
        self.go_to_ALPR_ExposureMode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_ExposureMode_div").get_attribute("data-text")
        self.assertEqual(status, "Multi Metering", f"Exposure Mode is {status}, not Multi Metering")

    def test_case045_Check_ALPR_AESpeed(self):
        #到Exposure頁面檢查AESpeed
        self.go_to_ALPR_ExposureMode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESpeed_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"AE Speed is {status}, not 50%")

    def test_case046_Check_ALPR_AESensitivity(self):
        #到Exposure頁面檢查AESensitivity
        self.go_to_ALPR_ExposureMode_page()
        status = self.driver.find_element(By.ID, "select_ExposureMode_AESensitivity_div").get_attribute("data-text")
        self.assertEqual(status, "50%", f"AE Sensitivity is {status}, not 50%")
        
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

    #case80開始確認camera information
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
        #進入system頁面
        self.go_to_system_page()
        #定位firmware Version
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "span_Device_FWVersion")))
        model = self.driver.find_element(By.ID,"span_Device_FWVersion").text
        self.assertEqual(model, "VER_0.033.000", f"model is {model}, not VER_0.033.000")
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner.HTMLTestRunner(output='D:/SeleniumProject/test_reports'))
