import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

class ProfileImageUploadTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure a headless Firefox browser and set the URL.
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        cls.browser = webdriver.Firefox(options=options)
        try:
            cls.url = os.environ['URL']
        except:
            cls.url = "http://localhost"

    def test_profile_image_upload(self):
        # Perform the test steps for profile picture upload.
        self.login_with_correct_credentials()
        self.go_to_profile_page()
        self.upload_new_profile_picture()

    def login_with_correct_credentials(self):
        # Log in using predefined credentials.
        login_url = f"{self.url}/login.php"
        self.browser.get(login_url)

        self.browser.find_element(By.ID, 'inputUsername').send_keys('admin')
        self.browser.find_element(By.ID, 'inputPassword').send_keys('nimda666!')
        self.browser.find_element(By.TAG_NAME, 'button').click()

    def go_to_profile_page(self):
        # Navigate to the user's profile page.
        profile_url = f"{self.url}/profil.php"
        self.browser.get(profile_url)

    def upload_new_profile_picture(self):
        # Upload a new profile picture and verify the changes.
        file_input = self.browser.find_element(By.ID, 'formFile')
        
        image_path = os.path.join(os.getcwd(), 'tests', 'test_images', 'image.jpg')
        file_input.send_keys(image_path)

        submit_button = self.browser.find_element(By.CSS_SELECTOR, 'button.btn-secondary')
        submit_button.click()

        redirected_url = f"{self.url}/profil.php"
        self.assertEqual(redirected_url, self.browser.current_url)

        new_profile_picture = self.browser.find_element(By.CSS_SELECTOR, 'img[src="image/profile.jpg"]')
        self.assertIsNotNone(new_profile_picture)

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests are executed.
        cls.browser.quit()

if __name__ == '__main__':
    # Run the tests with increased verbosity and ignore warnings.
    unittest.main(verbosity=2, warnings='ignore')
