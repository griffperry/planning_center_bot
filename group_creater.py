#!/usr/bin/env python3

import argparse
import sys
import traceback
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class PlanningCenterBot():

    def __init__(self, email, password):
        self.wait = 0.3
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
        self.add_member_to_group(group, group["leader"])
        if group.get("co-leader"):
            self.add_member_to_group(group, group["co-leader"])
        self.add_group_settings(group)
        self.return_out_to_main_groups_page()

    def create_group(self, group):
        self.click_button(By.XPATH, "//*[@id='filtered-groups-header']/div/div/div/button[2]")
        self.add_text_to_field(By.NAME, "group[name]", group.get("name"))
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[3]/button/span")

    def add_member_to_group(self, group, member):
        member_type = self.get_member_type(group, member)
        if member_type == "leader":
            add_member_xpath = "/html/body/main/div/div/div[2]/div/div/div/div[3]/div[2]/div/div"
        else:
            add_member_xpath = "//*[@id='group-member-finder']/div/div[3]/div[2]/div"
        self.click_button(By.XPATH, add_member_xpath)
        success = self.search_and_add_member(member)
        if "leader" in member_type and success:
            self.promote_member_to_leader(group, member)

    def search_and_add_member(self, member):
        # print(f"Search for {member}")
        self.add_text_to_field(By.ID, "person_search", member)
        second_member_xpath = "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/ul[1]/li[2]/button"
        found_second_member = self.attempt_find_element(By.XPATH, second_member_xpath)
        if found_second_member:
            # TODO: Use email to verify member when multiple members found.
            print(f"More than one result when searching for {member}")
            self.click_button(By.XPATH, "/html/body/div[2]/div/div[1]/button") # Click X
            return False
        only_result_xpath = "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/ul[1]/li/button"
        self.click_button(By.XPATH, only_result_xpath)
        self.dont_notify_by_email()
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")
        return True

    def promote_member_to_leader(self, group, member):
        member_type = self.get_member_type(group, member)
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

    def get_member_type(self, group, member):
        return list(group.keys())[list(group.values()).index(member)]

    def dont_notify_by_email(self):
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[2]/form/div/label")

    def add_group_settings(self, group):
        self.click_button(By.XPATH, "/html/body/main/div/aside/nav/ul/li[5]")
        self.add_meeting_schedule(group.get("schedule"))
        self.add_description(group.get("description"))
        self.add_group_contact_email(group.get("contact_email"))
        # self.add_group_location(group.get("location"))
        # self.add_group_tags(group.get("tags"))

    def add_meeting_schedule(self, schedule):
        if schedule:
            self.add_text_to_field(By.ID, "group_schedule", schedule)
            self.click_button(By.XPATH, "/html/body/main/div/div/section/section[1]/div/div[1]/div[2]/form[1]/div/div/div/div/a")

    def add_description(self, description):
        if description:
            self.add_text_to_field(By.XPATH,
                               "/html/body/main/div/div/section/section[2]/div[1]/div[2]/div/form/div/div/div/div[1]/trix-editor",
                               description,
                            )
            self.click_button(By.XPATH, "/html/body/main/div/div/section/section[2]/div[1]/div[2]/div/form/div/div/div/div[2]/div/a")

    def add_group_contact_email(self, email):
        if email:
            self.add_text_to_field(By.ID, "group_contact_email", email)
            self.add_text_to_field(By.ID, "group_contact_email", Keys.ENTER)
            time.sleep(self.wait)

    def go_to_main_groups_page(self):
        self.click_button(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/button[1]")
        self.click_button(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[1]/div/menu/a[2]")

    def return_out_to_main_groups_page(self):
        self.click_button(By.XPATH, "/html/body/div/div/div[3]/a[1]")

    def click_button(self, by_type, xpath):
        button = self.attempt_find_element(by_type, xpath)
        if button:
            button.click()
            time.sleep(self.wait)
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
                time.sleep(sleep_time)
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

    # groups = get_groups(args.groups_file)
    # Read in excel file, build groups dict
    groups = {
        1: {
            "name": "test bot 1",
            "leader": "Griff Perry",
            "co-leader": "Josh Smith",
            "schedule": "Thursday @ 11:30 AM Weekly",
            "description": "Test description",
            "contact_email": "test@gmail.com",
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
            "co-leader": "Kaylee Perry",
            "schedule": "Thursday @ 11:30 AM Weekly",
            "description": "Test description",
            "contact_email": "lgp0008@auburn.edu",
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
        3: {
            "name": "test bot 3",
            "leader": "Griff Perry",
            "co-leader": None,
            "schedule": "Thursday @ 11:30 AM Weekly",
            "description": "Test description",
            "contact_email": "lgp0008@auburn.edu",
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

    def setup_workers():
        return PlanningCenterBot(args.email, args.password)

    def init_process(bot, group):
        if bot.driver:
            try:
                bot.go_to_main_groups_page()
                # for group in groups.values():
                bot.group_init(group)
                print(f"Group '{group['name']}' created.")
            except Exception as error:
                trace_back_str = traceback.format_exc()
                print(trace_back_str)
                sys.exit(1)
            finally:
                if bot:
                    bot.close_session()

    start_time = time.time()
    bots = [ setup_workers() for _ in range(len(groups)) ]
    total_time = time.time() - start_time
    print(f"Registered sessions in {total_time} seconds\n")

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=len(groups)) as executor:
        executor.map(init_process, bots, groups.values())
    total_time = time.time() - start_time
    print(f"Created all groups in {total_time} seconds")

if __name__ == "__main__":
    main()
