import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class ValidLoginTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up headless Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=options)

    def test_valid_login(self):
        # login.php
        login_url = 'http://localhost/login.php'
        self.browser.get(login_url)

        # Input username dan password
        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()

    def test_index(self):
        # index.php
        def test_2_index_page(self):           
        expected_result = "admin"
        actual_result = self.browser.find_element(By.XPATH, "//h2[contains(text(),'Halo,')]").text.split(', ')[1]
        self.assertIn(expected_result, actual_result)

    @classmethod
    def tearDownClass(cls):
        # Close browser 
        cls.browser.quit()

if __name__ == '__main__':
    # Run the tests 
    unittest.main(verbosity=2, warnings='ignore')
