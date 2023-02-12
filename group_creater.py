#!/usr/bin/env python3

import argparse
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep


class PlanningCenterBot():

    def __init__(self, email, password):
        options = Options()
        options.add_argument('-headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://login.planningcenteronline.com/login/new")
        self.add_text_to_field(By.ID, "email", email)
        self.add_text_to_field(By.ID, "password", password)
        self.click_button(By.NAME, "commit")

        email_error_message = "Email or phone not found"
        password_error_message = "Password is incorrect"
        errors = self.driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div/div")
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
    
    def create_group(self, group):
        self.click_button(By.XPATH, "//*[@id='filtered-groups-header']/div/div/div/button[2]")
        self.add_text_to_field(By.NAME, "group[name]", group.get("name"))
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[3]/button/span")
        # create rest of group data
        self.return_out_to_main_groups_page()

    def go_to_main_groups_page(self):
        self.click_button(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/button[1]")
        self.click_button(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[1]/div/menu/a[2]")

    def return_out_to_main_groups_page(self):
        self.click_button(By.XPATH, "/html/body/div/div/div[3]/a[1]")

    def click_button(self, by_type, xpath):
        self.driver.find_element(by_type, xpath).click()
        sleep(1)

    def add_text_to_field(self, by_type, class_name, text):
        self.driver.find_element(by_type, class_name).send_keys(text)

    def close_session(self):
        print("Closing session")
        self.driver.close()

def parse_args():
    parser = argparse.ArgumentParser(description='Provide email and pw')
    parser.add_argument('email')
    parser.add_argument('password')
    return parser.parse_args()

def main():
    args = parse_args()
    bot = PlanningCenterBot(args.email, args.password)
    # groups = get_groups(args.groups_file)
    # Read in excel file, build groups dict
    groups = {
        1: {
            "name": "test bot 1",
            "type": "small groups",
            "schedule": "Thursday @ 11:30 AM Weekly",
            "description": "Test description",
            "contact email": "test@gmail.com",
            "location": "Perry Home",
            "tags": {
                "campus": "Madison",
                "year": "2023",
                "season": "Winter/Spring",
                "regularity": "Weekly",
                "group type": "Prayer",
                "group age": "All ages welcome",
                "group members": "Men",
                "day of week": "Thursday",
            },
        },
        2: {
            "name": "test bot 2",
            "type": "small groups",
            "schedule": "Thursday @ 11:30 AM Weekly",
            "description": "Test description",
            "contact email": "test@gmail.com",
            "location": "Perry Home",
            "tags": {
                "campus": "Madison",
                "year": "2023",
                "season": "Winter/Spring",
                "regularity": "Weekly",
                "group type": "Prayer",
                "group age": "All ages welcome",
                "group members": "Men",
                "day of week": "Thursday",
            },
        },
    }

    if bot.driver:
        try:
            bot.go_to_main_groups_page()
            for group in groups.values():
                bot.create_group(group)
                print(f"Group '{group['name']}' created.")
        except Exception as error:
            trace_back_str = traceback.format_exc()
            print(trace_back_str)
            sys.exit(1)
        finally:
            if bot:
                bot.close_session()

if __name__ == "__main__":
    main()
