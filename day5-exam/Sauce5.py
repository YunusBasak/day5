from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class Test_Sauce:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")


    def teardown_method(self):
        self.driver.quit()


    # @pytest.mark.parametrize("username","password",[(" "," ")])
    # @pytest.skip()
    def emptyLogin(self):
        loginBtn =self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        sleep(2)
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        errorResult = errorMessage.text == "Epic sadface: Username is required"
        # Kullanıcı adı ve şifre alanları boş geçildiğinde bu iki inputun yanında da kırmızı "X" ikonu çıkmalıdır. Daha sonra aşağıda çıkan uyarı mesajının kapatma butonuna tıklandığında bu "X" ikonları kaybolmalıdır.
        errorX = self.driver.find_element(By.CLASS_NAME,"error-button")
        errorX.click()
        print(f"Test Sonucu: {errorX}")
        print(f"Test Sonucu: {errorResult}")
        sleep(2)

    # @pytest.mark.parametrize("username","password",[("1"," ")])
    def emptyPassword(self):
        # Sadece şifre alanı boş geçildiğinde uyarı mesajı olarak "Epic sadface: Password is required" gösterilir.

        username = self.driver.find_element(By.ID,"user-name")
        username.send_keys("1")
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        sleep(2)
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        errorResult = errorMessage.text == "Epic sadface: Password is required" 
        print(f"Test Sonucu: {errorResult}")
        sleep(1)

    # @pytest.mark.parametrize("username","password",[("locked_out_user","secret_sauce ")])
    def login(self):
        # Kullanıcı adı locked_out_user şifre alanı secret_sauce gönderildiğinde Epic sadface: Sorry, this user has been locked out. mesajı gösterilir
        username = self.driver.find_element(By.ID,"user-name")
        username.send_keys("locked_out_user")
        password = self.driver.find_element(By.ID,"password")
        password.send_keys("secret_sauce")
        sleep(1)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        errorResult =errorMessage.text == "Epic sadface: Sorry, this user has been locked out." 
        print(f"Test Sonucu: {errorResult}")
        sleep(4)
        
    # # @pytest.mark.parametrize("username","password",[("standard_user","secret_sauce ")])
    # @pytest.mark.skip()
    def pageLogin(self):
        # Kullanıcı adı "standard_user" şifre "secret_sauce" gönderildiğinde kullanıcı "/inventory.html" sayfasına gönderilmelidir.
        username = self.driver.find_element(By.ID,"user-name")
        username.send_keys("standard_user")
        password = self.driver.find_element(By.ID,"password")
        password.send_keys("secret_sauce")
        sleep(1)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        sleep(3)

 
        # Giriş yapıldıktan sonra kullanıcıya gösterilen ürün sayısı "6" adet olmalıdır.
        driver = webdriver.Chrome()
        listOfCourse = driver.find_elements(By.CLASS_NAME,"inventory_item")
        print(f"Şu anda {len(listOfCourse)} adet ürün vardır.")
        sleep(2)