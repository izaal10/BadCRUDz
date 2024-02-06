import unittest, os
from selenium import webdriver
from selenium.webdriver.common.by import By

class LogOutTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=option)
        cls.url = "http://localhost"

    def test(self):
        self.login_valid()
        self.index()
        self.logout()

    def login_valid(self):
        login_url = self.url +'/login.php'
        self.browser.get(login_url)

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()

    def index(self):
        expected_result = "admin"
        actual_result = self.browser.find_element(By.XPATH, "//h2[contains(text(),'Halo,')]").text.split(', ')[1]
        self.assertIn(expected_result, actual_result)

    def logout(self):
        self.browser.find_element(By.XPATH, "//a[contains(text(),'Sign out')]").click()
        login_page_result = "Login"
        actual_result = self.browser.title
        self.assertEqual(login_page_result, actual_result)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
