import time
import traceback
from planning_center_backend import planning_center
from planning_center_backend.people import PeopleQueryExpression
from src.status_report import StatusReport
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GroupManager(StatusReport):

    def __init__(self, email, password, id):
        self.start_wait = 0.5
        self.wait = self.start_wait
        self.id = id
        self.attempts = 0
        self.location_attempts = 0
        self.max_attempts = 3
        self.reports = []
        self.group_status = {}
        self.group_caveats = {}
        self.backend = planning_center.PlanningCenterBackend()
        self.backend.login(email, password)
        super().__init__()

    def delete_group(self, group):
        group_deleted = False
        name = group["name"]
        groups = self.backend.groups.query(name)
        if groups:
            groups[0].delete()
        if not self.backend.groups._check_exists(name):
            group["added members"] = []
            group_deleted = True
        else:
            print(f"(User {self.id}) Search for group '{name}' failed.")
        return group_deleted

    def create_group(self, group):
        group_name = group["name"]
        print(f"(User {self.id}) Start group {group_name}")
        self.group_status[group_name] = None
        self.group_caveats[group_name] = []
        try:
            success = self.add_group(group)
            if success:
                for member in group["members"].values():
                    self.add_member_to_group(member)
                self.add_group_settings(group)
                self.add_group_status(group_name, f"(User {self.id}) Group '{group_name}' created.")
            self.reports.append(self.create_report(group_name))
            self.attempts = 0
            self.wait = self.start_wait
            group["added members"] = []
        except Exception:
            trace_back_str = traceback.format_exc()
            print(trace_back_str)

    def add_group(self, group):
        group_name = group["name"]
        if not self.backend.groups._check_exists(group_name):
            self.current_group = self.backend.groups.create(group_name)
        else:
            self.add_group_status(group_name, f"(User {self.id}) Group '{group_name}' already exists.")
            self.current_group = self.backend.groups.query(group_name)[0]
        if self.backend.groups._check_exists(group_name):
            return True
        return False

    def add_member_to_group(self, member):
        member_name = member.get("name")
        member_status = member.get("status")
        member_email = member.get("email")
        promote_member = "leader" in member_status
        qe = PeopleQueryExpression(search_name=member_name, search_name_or_email=member_email)
        if qe:
            person_obj = self.backend.people.query(qe)
            if len(person_obj) == 1:
                self.current_group.add_member(person_id=person_obj[0].id, leader=promote_member)

    def add_group_settings(self, group):
        with self.current_group.no_refresh():
            self.add_meeting_schedule(group.get("schedule"))
            self.add_description(group.get("description"))
            self.add_group_contact_email(group.get("contact_email"))
            self.add_group_tags(group.get("tags"))
            # self.add_group_location(group.get("name"), group.get("address"))

    def add_meeting_schedule(self, schedule):
        if schedule:
            self.current_group.schedule = schedule

    def add_description(self, description):
        if description:
            self.current_group.description = description

    def add_group_contact_email(self, email):
        if email:
            self.current_group.contact_email = email

    def add_group_location(self, group_name, address):
        if group_name and address:
            self.click_button(By.XPATH, "//option[contains(text(), 'Create a new location...')]")
            self.add_location_contents(group_name, address)

    def add_location_contents(self, group_name, address):
        try:
            address_container = self.attempt_find_element(By.XPATH, "//div[contains(@class, 'address-container')]")
            text_box = address_container.find_element(By.XPATH, ".//input[contains(@type, 'text')]")
            text_box.send_keys(f"{group_name} location")
            text_box.send_keys(Keys.ENTER)
            time.sleep(self.wait)
            text_box = address_container.find_element(By.XPATH, ".//input[contains(@placeholder, 'Street address')]")
            text_box.send_keys(address)
            text_box.send_keys(Keys.ENTER)
            time.sleep(self.wait)
            self.click_button(By.XPATH, "//option[contains(@value, 'hidden')]")
            save_location_buttons = self.attempt_find_elements(By.XPATH, "//span[contains(text(), 'Save location')]")
            if len(save_location_buttons) > 1:
                save_location_buttons[1].click()
            time.sleep(self.wait)
            self.location_attempts = 0
        except Exception:
            self.driver.refresh()
            self.location_attempts += 1
            if self.location_attempts < self.max_attempts:
                print(f"(User {self.id}) Retry adding location  '{group_name}'")
                self.add_group_location(group_name, address)
            else:
                self.add_group_caveat(group_name, f"(User {self.id}) Failed to add location in group '{group_name}'")

    def add_group_tags(self, tags):
        if tags:
            tag_list = self.gen_simple_tag_list(tags)
            for tag in tag_list:
                self.current_group.add_tag(tag)

    def gen_simple_tag_list(self, tags):
        tag_list = []
        for tag in tags.values():
            if isinstance(tag, str):
                tag_list.append(tag)
            if isinstance(tag, list):
                for i in tag:
                    tag_list.append(i)
        return tag_list
