import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class CreateContactTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=option)
        cls.url = "http://localhost"
        cls.name_query = 'user'

    def test(self):
        self.login_correct_credentials()
        self.create_contact()
        self.search_contact()

    def login_correct_credentials(self):
        login_url = self.url + '/login.php'
        self.browser.get(login_url)

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()

    def create_contact(self):
        create_url = self.url + '/create.php'
        self.browser.get(create_url)

        self.browser.find_element(By.ID, 'name').send_keys(self.name_query)
        self.browser.find_element(By.ID, 'email').send_keys('email@email.com')
        self.browser.find_element(By.ID, 'phone').send_keys('621234567890')
        self.browser.find_element(By.ID, 'title').send_keys('User')

        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        index_page_title = "Dashboard"
        actual_title = self.browser.title
        self.assertEqual(index_page_title, actual_title)

    def search_contact(self):
        search_query = self.name_query
        self.browser.find_element(By.ID, 'employee_filter').find_element(By.TAG_NAME, 'input').send_keys(search_query)
        self.browser.find_element(By.ID, 'employee_filter').find_element(By.TAG_NAME, 'input').send_keys(Keys.ENTER)

        searched_contact_name = self.name_query
        searched_contact_exists = self.browser.find_elements(By.XPATH, f"//td[contains(text(), '{searched_contact_name}')]")
        self.assertTrue(searched_contact_exists)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')