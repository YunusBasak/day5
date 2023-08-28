from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from pathlib import Path
from datetime import date

class Test_Sauce:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.folderPath= str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True) 

    def teardown_method(self):
        self.driver.quit()

    def waitforelementVisible(self,locator):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located(locator))


    @pytest.mark.parametrize("username,password",[(" "," ")])
    # @pytest.mark.skip()
    def test_EmptyLogin(self,username,password):
        loginBtn =self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        errorResult = errorMessage.text == "Epic sadface: Username is required"
        # Kullanıcı adı ve şifre alanları boş geçildiğinde bu iki inputun yanında da kırmızı "X" ikonu çıkmalıdır. Daha sonra aşağıda çıkan uyarı mesajının kapatma butonuna tıklandığında bu "X" ikonları kaybolmalıdır.
        errorX = self.driver.find_element(By.CLASS_NAME,"error-button")
        errorX.click()
        self.driver.save_screenshot(f"{self.folderPath}/test_EmptyLogin.png")
        print(f"Test Sonucu: {errorX}")
        print(f"Test Sonucu: {errorResult}")
       

    @pytest.mark.parametrize("username",[("1",)])
    def test_EmptyPassword(self,username):
        # Sadece şifre alanı boş geçildiğinde uyarı mesajı olarak "Epic sadface: Password is required" gösterilir.
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
        usernameInput= self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys(username)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        errorResult = errorMessage.text == "Epic sadface: Password is required" 
        self.driver.save_screenshot(f"{self.folderPath}/test_EmptyPassword.png")
        print(f"Test Sonucu: {errorResult}")
        

    @pytest.mark.parametrize("username,password",[("locked_out_user","secret-sauce"), ("user", "123"), ("user", "pp")])
    def test_Login(self,username,password):
        # Kullanıcı adı locked_out_user şifre alanı secret_sauce gönderildiğinde Epic sadface: Sorry, this user has been locked out. mesajı gösterilir
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys(password)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        errorMessage = self.driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3")
        assert errorMessage.text == "Epic sadface: Username and password do not match any user in this service"
        self.driver.save_screenshot(f"{self.folderPath}/test_Login-{username}-{password}.png")
        # print(f"Test Sonucu: {errorResult}")
       
        
    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")])
    # @pytest.mark.skip()
    def test_PageLogin(self,username,password):
        # Kullanıcı adı "standard_user" şifre "secret_sauce" gönderildiğinde kullanıcı "/inventory.html" sayfasına gönderilmelidir.
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys(password)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        self.driver.save_screenshot(f"{self.folderPath}/test_PageLogin.png")

    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")])
    def test_ListOfCourse(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys(password)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        self.driver.save_screenshot(f"{self.folderPath}/test_ListOfCourse.png")
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.CLASS_NAME,"inventory_item")))
        listOfCourse = self.driver.find_elements(By.CLASS_NAME,"inventory_item")
        print(f"Şu anda {len(listOfCourse)} adet ürün vardır.")
        
      
        
    # Giriş yaptıktan sonra ürün ekleme butonuna tıklayan (ürün ekleyen) case
    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")])
    def test_AddToCart(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys(password)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"add-to-cart-sauce-labs-backpack")))
        cart = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack")
        cart.click()
        self.driver.save_screenshot(f"{self.folderPath}/test_AddToCart.png")
       
      # Giriş yaptıktan sonra eklenen ürünler sayfasına giren case
    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")])
    def test_ShoppingCart(self,username,password):
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys(username)
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys(password)
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"add-to-cart-sauce-labs-backpack")))
        cart = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack")
        cart.click()
        
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.CLASS_NAME,"shopping_cart_link")))
        ShoppingCart = self.driver.find_element(By.CLASS_NAME,"shopping_cart_link")
        ShoppingCart.click()
        self.driver.save_screenshot(f"{self.folderPath}/test_ShoppingCart.png")

        

    # Giriş yaptıktan sonra eklenen ürünler sayfasından ürünü silen case
    @pytest.mark.parametrize("username,password",[("standard_user","secret_sauce")])
    def test_RemoveToCart(self,username,password):
        self.waitforelementVisible((By.ID,"user-name"))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        usernameInput.send_keys("standard_user")
        self.waitforelementVisible((By.ID,"password"))
        passwordInput = self.driver.find_element(By.ID,"password")
        passwordInput.send_keys("secret_sauce")
        loginBtn = self.driver.find_element(By.ID,"login-button")
        loginBtn.click()
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"add-to-cart-sauce-labs-backpack")))
        cart = self.driver.find_element(By.ID,"add-to-cart-sauce-labs-backpack")
        cart.click()
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.CLASS_NAME,"shopping_cart_link")))
        ShoppingCart = self.driver.find_element(By.CLASS_NAME,"shopping_cart_link")
        ShoppingCart.click()
        WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"remove-sauce-labs-backpack")))
        cart = self.driver.find_element(By.ID,"remove-sauce-labs-backpack")
        cart.click()
        self.driver.save_screenshot(f"{self.folderPath}/test_RemoveToCart.png")
    
   