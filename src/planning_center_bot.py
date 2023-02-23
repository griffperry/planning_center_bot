import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class PlanningCenterBot():

    def __init__(self):
        self.start_wait = 2
        self.wait = self.start_wait
        options = Options()
        if not self.demo:
            self.start_wait = 0.5
            self.wait = self.start_wait
            options.add_argument('-headless')
        options.add_argument('log-level=3')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://login.planningcenteronline.com/login/new")
        self.add_text_to_field_safe(By.ID, "email", self.email)
        self.add_text_to_field_safe(By.ID, "password", self.password)
        self.click_button_safe(By.NAME, "commit")

        email_error_message = "Email or phone not found"
        password_error_message = "Password is incorrect"
        errors = self.attempt_find_elements(By.XPATH, "/html/body/div[1]/div[2]/div/div")
        if any(email_error_message in e.text for e in errors):
            print("[!] Login failed | Wrong email")
            self.close_session()
            self.driver = None
        elif any(password_error_message in e.text for e in errors):
            print("[!] Login failed | Wrong password")
            self.close_session()
            self.driver = None
        else:
            print("[+] Login successful")
    
    def click_button(self, by_type, xpath):
        button = self.attempt_find_element(by_type, xpath)
        if button:
            button.click()
            time.sleep(self.wait)
            return True
        else:
            # print(f"Could not find button at {xpath}")
            raise Exception

    def add_text_to_field(self, by_type, xpath, text):
        field = self.attempt_find_element(by_type, xpath)
        if field:
            field.send_keys(text)
            time.sleep(self.wait)
            return True
        else:
            # print(f"Could not find field at {xpath}")
            raise Exception

    def hit_enter_on_element(self, by_type, xpath):
        self.add_text_to_field(by_type, xpath, Keys.ENTER)
        time.sleep(self.wait)

    def click_button_safe(self, by_type, xpath):
        button = self.attempt_find_element(by_type, xpath)
        if button:
            button.click()
            time.sleep(self.wait)
            return True
        else:
            # print(f"Could not find button at {xpath}")
            return False

    def add_text_to_field_safe(self, by_type, xpath, text):
        field = self.attempt_find_element(by_type, xpath)
        if field:
            field.send_keys(text)
            time.sleep(self.wait)
            return True
        else:
            # print(f"Could not find field at {xpath}")
            return False

    def hit_enter_on_element_safe(self, by_type, xpath):
        self.add_text_to_field_safe(by_type, xpath, Keys.ENTER)
        time.sleep(self.wait)

    def attempt_find_element(self, by_type, xpath, timeout=5):
        sleep_time = 0.5
        max_tries = timeout/sleep_time
        tries = 0
        while tries < max_tries:
            try:
                element = self.driver.find_element(by_type, xpath)
                break
            except Exception:
                tries += 1
                time.sleep(sleep_time)
                element = None
        return element

    def attempt_find_elements(self, by_type, xpath, timeout=5):
        sleep_time = 0.5
        max_tries = timeout/sleep_time
        tries = 0
        while tries < max_tries:
            try:
                element = self.driver.find_elements(by_type, xpath)
                break
            except Exception:
                tries += 1
                time.sleep(sleep_time)
                element = []
        return element

    def close_session(self):
        print("Closing session")
        self.driver.close()
