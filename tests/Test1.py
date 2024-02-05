import unittest
import os
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TestCreateAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        browser_options = webdriver.FirefoxOptions()
        browser_options.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=browser_options)
        try:
            cls.url = os.environ['URL']
        except:
            cls.url = "http://localhost"
        cls.name_query = ''.join(random.choices(string.ascii_letters, k=10))

    def test(self):
        self.perform_correct_login()
        self.create_and_manage_contact()
        self.verify_contact_search()
        self.verify_contact_deletion()

    def perform_correct_login(self):
        login_url = self.url + '/login.php'
        self.browser.get(login_url)

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()

    def create_and_manage_contact(self):
        create_url = self.url + '/create.php'
        self.browser.get(create_url)

        self.browser.find_element(By.ID, 'name').send_keys(self.name_query)
        self.browser.find_element(By.ID, 'email').send_keys('user@user.com')
        self.browser.find_element(By.ID, 'phone').send_keys('1234')
        self.browser.find_element(By.ID, 'title').send_keys('User')

        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        expected_title = "Dashboard"
        actual_title = self.browser.title
        self.assertEqual(expected_title, actual_title)

    def verify_contact_search(self):
        search_query = self.name_query
        search_input = self.browser.find_element(By.ID, 'employee_filter').find_element(By.TAG_NAME, 'input')
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.ENTER)

        searched_contact_name = self.name_query
        searched_contact_exists = self.browser.find_elements(By.XPATH, f"//td[contains(text(), '{searched_contact_name}')]")
        self.assertTrue(searched_contact_exists)

    def verify_contact_deletion(self):
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")

        delete_button.click()

        self.browser.switch_to.alert.accept()
        time.sleep(3)

        search_query = self.name_query
        search_input = self.browser.find_element(By.ID, 'employee_filter').find_element(By.TAG_NAME, 'input')
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.ENTER)

        searched_contact_name = self.name_query
        searched_contact_exists = self.browser.find_elements(By.XPATH, f"//td[contains(text(), '{searched_contact_name}')]")
        self.assertFalse(searched_contact_exists)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
