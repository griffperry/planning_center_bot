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
    
    def group_init(self, group):
        self.create_group(group)
        self.add_leader_to_group(group)
        if group.get("co-leader"):
            self.add_member_to_group(group, leader=True)
        # self.add_group_settings(group)
        self.return_out_to_main_groups_page()

    def go_to_main_groups_page(self):
        self.click_button(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/button[1]")
        self.click_button(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[1]/div/menu/a[2]")

    def return_out_to_main_groups_page(self):
        self.click_button(By.XPATH, "/html/body/div/div/div[3]/a[1]")

    def create_group(self, group):
        self.click_button(By.XPATH, "//*[@id='filtered-groups-header']/div/div/div/button[2]")
        self.add_text_to_field(By.NAME, "group[name]", group.get("name"))
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[3]/button/span")

    def add_leader_to_group(self, group):
        add_first_member_xpath = "/html/body/main/div/div/div[2]/div/div/div/div[3]/div[2]/div/div"
        self.click_button(By.XPATH, add_first_member_xpath)
        self.search_for_member(group["leader"])
        self.promote_member_to_leader(group, group["leader"])

    def add_member_to_group(self, group, leader=False):
        if leader:
            # breakpoint()
            self.click_button(By.XPATH, "//*[@id='group-member-finder']/div/div[3]/div[2]/div")
            self.search_for_member(group["co-leader"])
            self.promote_member_to_leader(group, group["co-leader"])

    def search_for_member(self, member):
        self.add_text_to_field(By.ID, "person_search", member)
        only_result_xpath = "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/ul[1]/li/button"
        success = self.click_button(By.XPATH, only_result_xpath)
        if not success:
            # TODO: Use email to verify member when multiple members found.
            print(f"More than one result when searching for {member}")
            return
        self.dont_notify_by_email()
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")

    def promote_member_to_leader(self, group, member):
        member_type = list(group.keys())[list(group.values()).index(member)]
        if "leader" == member_type:
            promote_xpath = "//*[@id='group-member-finder']/div/div[5]/div[2]/div/div[5]/div/div"
        elif "co-leader" == member_type:
            promote_xpath = "//*[@id='group-member-finder']/div/div[5]/div[2]/div[2]/div[5]/div/div"
        else:
            print(f"Can't find promote button for {member}")
            return
        self.click_button(By.XPATH, promote_xpath)
        self.dont_notify_by_email()
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")

    def dont_notify_by_email(self):
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[2]/form/div/label")

    def click_button(self, by_type, xpath):
        button = self.attempt_find_element(by_type, xpath)
        if button:
            button.click()
            sleep(0.5)
            return True
        else:
            print(f"Could not find button at {xpath}")
            return False

    def add_text_to_field(self, by_type, xpath, text):
        field = self.attempt_find_element(by_type, xpath)
        if field:
            field.send_keys(text)
            return True
        else:
            print(f"Could not find field at {xpath}")
            return False

    def attempt_find_element(self, by_type, xpath, timeout=3):
        element = None
        sleep_time = 0.5
        max_tries = timeout/sleep_time
        tries = 0
        while tries < max_tries:
            try:
                element = self.driver.find_element(by_type, xpath)
                break
            except Exception:
                tries += 1
                sleep(sleep_time)
        return element

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
            "leader": "Griff Perry",
            "co-leader": "Kaylee Perry",
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
            "leader": "Griff Perry",
            "co-leader": None,
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
                bot.group_init(group)
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
