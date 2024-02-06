import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginInvalidTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up headless Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=options)

    def test_invalid_login(self):
        login_url = 'http://localhost/login.php'
        self.browser.get(login_url)

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('admin')
        self.browser.find_element(By.TAG_NAME, 'button').click()

    def test_error_message(self):
        expected_result = "Wrong usename or password"
        
        actual_result = self.browser.find_element(By.CLASS_NAME, 'checkbox').text
        self.assertIn(expected_result, actual_result)

    @classmethod
    def tearDownClass(cls):
        # Close browser 
        cls.browser.quit()

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2, warnings='ignore')
