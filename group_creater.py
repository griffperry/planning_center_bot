#!/usr/bin/env python3

import sys
import traceback
import time
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class PlanningCenterBot():

    def __init__(self, email, password, demo):
        self.wait = 0.5
        options = Options()
        if not demo:
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

    def delete_test_group(self, name):
        self.add_text_to_field(By.XPATH, "//*[@id='groups-index']/div/div[1]/div[2]/div/div[2]/div/input", name)
        self.add_text_to_field(By.XPATH, "//*[@id='groups-index']/div/div[1]/div[2]/div/div[2]/div/input", Keys.ENTER)
        time.sleep(self.wait)
        # handle when group isn't found
        self.click_button(By.XPATH, "//*[@id='groups-index']/div/div[3]/div[2]/div[3]/div/div/div[2]/div[1]/div[3]/div")
        self.click_button(By.XPATH, "/html/body/main/div/aside/nav/ul/li[5]") # go to settings tab
        selected_group = self.attempt_find_element(By.XPATH, "//*[@id='groups-header']/header/div[2]/div[1]/h1")
        if name == selected_group.text:
            self.click_button(By.XPATH, "/html/body/main/div/div/section/header/div/a")
            self.click_button(By.XPATH, "/html/body/div[3]/div/div[3]/div/a")
            self.add_text_to_field(By.XPATH, "/html/body/div[4]/div/div[2]/input[1]", "DELETE")
            self.add_text_to_field(By.XPATH, "/html/body/div[4]/div/div[2]/input[1]", Keys.ENTER)
            time.sleep(self.wait)
        else:
            print("Selected wrong group.")

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
        success = self.attempt_find_element(By.XPATH, "/html/body/div[1]/div/div[2]/a[1]")
        if success:
            self.click_button(By.XPATH, "/html/body/div[1]/div/div[2]/a[1]")
        else:
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


def setup_worker(email, password, demo):
    bot = PlanningCenterBot(email, password, demo)
    bot.go_to_main_groups_page()
    return bot

def handle_group_init(bot, group):
    if bot.driver:
        try:
            bot.group_init(group)
            print(f"Group '{group['name']}' created.")
        except Exception as error:
            trace_back_str = traceback.format_exc()
            print(trace_back_str)
            sys.exit(1)

def delete_group(bot, group):
    if bot.driver:
        try:
            bot.delete_test_group(group.get("name"))
        except Exception as error:
            trace_back_str = traceback.format_exc()
            print(trace_back_str)
            sys.exit(1)

def register_sessions(bot_count, email, password, demo):
    start_time = time.time()
    bots = [ setup_worker(email, password, demo) for _ in range(bot_count) ]
    total_time = time.time() - start_time
    print(f"Registered sessions in {total_time} seconds\n")
    return bots

def init_process(bot_count, bots, groups):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=bot_count) as executor:
        bots *= int(len(groups)/bot_count)
        executor.map(handle_group_init, bots, groups)
    for bot in bots[:bot_count]:
        bot.close_session()
    total_time = time.time() - start_time
    print(f"Created all groups in {total_time} seconds")

def delete_groups(groups, email, password, demo):
    start_time = time.time()
    bot = setup_worker(email, password, demo)
    try:
        for group in groups:
            delete_group(bot, group)
    finally:
        if bot:
            bot.close_session()
    total_time = time.time() - start_time
    print(f"Deleted all groups in {total_time} seconds")

def main():
    bot_count = 2

    # groups = get_groups(groups_file) # Read in excel file, build groups dict
    groups = {
        1: {
            "name": "test group 1",
            "leader": "Griff Perry",
            "co-leader": "Josh Smith",
            # "co-leader": None,
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
            "name": "test group 2",
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
            "name": "test group 3",
            "leader": "Griff Perry",
            # "leader": "Mike Fitzgerald",
            "co-leader": None,
            "schedule": "Thursday @ 11:30 AM Weekly",
            "description": None,
            "contact_email": None,
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
        4: {
            "name": "test group 4",
            "leader": "Griff Perry",
            "co-leader": None,
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
        5: {
            "name": "test group 5",
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
        6: {
            "name": "test group 6",
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

    email = input("\nEmail: ")
    password = getpass()
    answer = input("Would you like to demo? [y/n]: ")
    demo = True if "y" in answer else False

    sessions = register_sessions(bot_count, email, password, demo)
    init_process(bot_count, sessions, groups.values())
    answer = input("Do you want to delete these groups? [y/n]: ")
    if "y" in answer:
        delete_groups(groups.values(), email, password, demo)

if __name__ == "__main__":
    main()
