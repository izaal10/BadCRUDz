import unittest
import os
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class ContactManagementTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up headless Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=options)

        # Set URL
        try:
            cls.url = os.environ.get('URL', 'http://localhost')
        except:
            cls.url = "http://localhost"

        # Randomizer
        cls.name_query = ''.join(random.choices(string.ascii_letters, k=10))

    def test_contact_actions(self):
        # Perform the end-to-end contact management flow.
        self.login_with_correct_credentials()
        self.create_contact()
        self.search_and_verify_contact()
        self.delete_contact()

    def valid_login(self):
        # Login.php
        login_url = f"{self.url}/login.php"
        self.browser.get(login_url)

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()

    def create_contact(self):
        # Create a new contact 
        create_url = f"{self.url}/create.php"
        self.browser.get(create_url)

        self.browser.find_element(By.ID, 'name').send_keys(self.name_query)
        self.browser.find_element(By.ID, 'email').send_keys('email@email.com')
        self.browser.find_element(By.ID, 'phone').send_keys('629876543210')
        self.browser.find_element(By.ID, 'title').send_keys('User')

        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        # Dashboard
        index_page_title = "Dashboard"
        actual_title = self.browser.title
        self.assertEqual(index_page_title, actual_title)

    def search_contact(self):
        # Search contact
        search_query = self.name_query
        search_input = self.browser.find_element(By.ID, 'employee_filter').find_element(By.TAG_NAME, 'input')
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.ENTER)

        searched_contact_name = self.name_query
        searched_contact_exists = self.browser.find_elements(By.XPATH, f"//td[contains(text(), '{searched_contact_name}')]")
        self.assertTrue(searched_contact_exists)

    def delete_contact(self):
        # Delete contact
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][1]//td[contains(@class, 'actions')]")
        delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
        delete_button.click()

        self.browser.switch_to.alert.accept()
        time.sleep(3)

        # Search deleted contact
        search_query = self.name_query
        search_input = self.browser.find_element(By.ID, 'employee_filter').find_element(By.TAG_NAME, 'input')
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.ENTER)

        searched_contact_name = self.name_query
        searched_contact_exists = self.browser.find_elements(By.XPATH, f"//td[contains(text(), '{searched_contact_name}')]")
        self.assertFalse(searched_contact_exists)

    @classmethod
    def tearDownClass(cls):
        # Close browser
        cls.browser.quit()

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2, warnings='ignore')
