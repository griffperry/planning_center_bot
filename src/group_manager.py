import time
# import traceback
from src.planning_center_bot import PlanningCenterBot
from src.status_report import StatusReport
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GroupManager(PlanningCenterBot, StatusReport):

    def __init__(self, email, password, demo, id):
        self.email = email
        self.password = password
        self.demo = demo
        self.id = id
        self.attempts = 0
        self.location_attempts = 0
        self.max_attempts = 3
        self.reports = []
        self.group_status = {}
        self.group_caveats = {}
        super().__init__()

    def delete_group(self, group):
        name = group["name"]
        self.add_text_to_field_safe(By.XPATH, "//input[contains(@placeholder, 'Search by filter')]", name)
        self.hit_enter_on_element_safe(By.XPATH, "//input[contains(@placeholder, 'Search by filter')]")
        success = self.click_button_safe(By.XPATH, "//*[@id='groups-index']/div/div[3]/div[2]/div[3]/div/div/div[2]/div[1]/div[3]/div")
        if success:
            self.go_to_settings_page()
            selected_group = self.attempt_find_element(By.XPATH, "//*[@id='groups-header']/header/div[2]/div[1]/h1")
            if selected_group and name == selected_group.text:
                self.select_archive_and_delete()
                group["added members"] = []
                return True
            else:
                print(f"(User {self.id}) Selected wrong group.")
                return False
        else:
            print(f"(User {self.id}) Search for group '{name}' failed.")
            return False

    def select_archive_and_delete(self):
        self.click_button_safe(By.XPATH, "/html/body/main/div/div/section/header/div/a")
        self.click_button_safe(By.XPATH, "/html/body/div[3]/div/div[3]/div/a")
        self.add_text_to_field_safe(By.XPATH, "/html/body/div[4]/div/div[2]/input[1]", "DELETE")
        self.hit_enter_on_element_safe(By.XPATH, "/html/body/div[4]/div/div[2]/input[1]")

    def create_group(self, group):
        group_name = group["name"]
        print(f"(User {self.id}) Start group {group_name}")
        self.group_status[group_name] = None
        self.group_caveats[group_name] = []
        try:
            success = self.add_group(group)
            if success:
                for member in group["members"].values():
                    self.add_member_to_group(group, member)
                self.add_group_settings(group)
                self.return_out_to_main_groups_page()
                self.add_group_status(group_name, f"(User {self.id}) Group '{group_name}' created.")
            else:
                self.add_group_status(group_name, f"(User {self.id}) Group '{group_name}' already exists.")

            self.reports.append(self.create_report(group_name))
            self.attempts = 0
            self.wait = self.start_wait
            group["added members"] = []
        except Exception:
            # trace_back_str = traceback.format_exc()
            # print(trace_back_str)
            self.retry_group_creation(group)

    def add_group(self, group):
        group_name = group["name"]
        self.click_button(By.XPATH, "//*[@id='filtered-groups-header']/div/div/div/button[2]")
        self.add_text_to_field(By.NAME, "group[name]", group_name)
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[3]/button/span")
        error = self.attempt_find_element(By.XPATH, "//div[contains(@class, 'warning-alert alert alert--warning')]", timeout=1)
        if error:
            self.click_button(By.XPATH, "/html/body/div[2]/div/div[1]/button") # Click X
            self.return_out_to_main_groups_page()
            return False
        return True

    def add_member_to_group(self, group, member):
        time.sleep(1)
        member_name = member.get("name")
        member_status = member.get("status")
        if len(group["added members"]) < 1:
            add_member_xpath = "//div[contains(text(), 'Add a person')]"
        else:
            add_member_xpath = "//div[contains(text(), 'Add person')]"
        self.click_button(By.XPATH, add_member_xpath)
        success = self.search_and_add_member(group, member)
        if "leader" in member_status and success:
            self.promote_member_to_leader(group, member_name)
        else:
            self.click_button(By.XPATH, "/html/body/div[2]/div/div[1]/button") # Click X

    def search_and_add_member(self, group, member):
        group_name = group.get("name")
        member_name = member.get("name")
        member_email = member.get("email")
        member_status = member.get("status")

        self.add_text_to_field(By.ID, "person_search", member_name)
        time.sleep(3)
        results = self.attempt_find_elements(By.XPATH, "//div[contains(@class, 'autocomplete-result-name')]")
        if len(results) == 0:
            self.add_group_caveat(group_name, f"(User {self.id}) {member_name} not found when added to '{group_name}'.")
            return False
        elif len(results) == 1:
            result_xpath = "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/ul[1]/li/button"
        else:
            success, result_xpath = self.verify_member_email(results, member_email, member_status)
            if not success:
                self.add_group_caveat(group_name, f"(User {self.id}) {member_name} not added to '{group_name}' as {member_status}.")
                return False
        self.click_button(By.XPATH, result_xpath)
        self.dont_notify_by_email()
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")
        group["added members"].append(member_name)
        return True

    def verify_member_email(self, results, email, status):
        success = False
        result_xpath = None
        if email and status == "leader":
            email_found = None
            for index, result in enumerate(results):
                try:
                    email_found = result.find_element(By.XPATH, f"..//span[contains(text(), '{email[:20]}')]")
                except Exception:
                    pass
                if email_found:
                    result_xpath = f"/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/ul[1]/li[{index+1}]/button"
                    success = True
                    break
                continue
        return success, result_xpath

    def promote_member_to_leader(self, group, member_name):
        time.sleep(1)
        members = self.attempt_find_elements(By.XPATH, "//div[contains(@aria-label, 'Edit membership role')]")
        sorted_members = sorted(group["added members"])
        member_position = sorted_members.index(member_name)
        members[member_position].click()
        time.sleep(self.wait)
        self.click_button(By.XPATH, "/html/body/div[2]/div/div[2]/div/form/fieldset[1]/div[1]/label")
        self.dont_notify_by_email()
        self.click_button(By.ID, "commit")

    def get_member_type(self, group, member):
        return list(group.keys())[list(group.values()).index(member)]

    def dont_notify_by_email(self):
        self.click_button(By.XPATH, "//label[contains(@class, 'checkbox-label c-dark')]")

    def add_group_settings(self, group):
        self.go_to_settings_page()
        self.add_meeting_schedule(group.get("schedule"))
        self.add_description(group.get("description"))
        self.add_group_contact_email(group.get("contact_email"))
        self.add_group_location(group.get("name"), group.get("address"))
        self.add_group_tags(group.get("tags"))

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
            self.hit_enter_on_element(By.ID, "group_contact_email")
            time.sleep(self.wait)

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
            self.click_button(By.XPATH, "//span[contains(text(), 'Add tags')]")
            self.find_and_select_tags(tags)
            self.click_button(By.XPATH, "//span[contains(text(), 'Add tags')]")

    def find_and_select_tags(self, tags):
        elements = self.attempt_find_elements(By.XPATH, "//li[contains(@class, 'mb-1')]")
        readable_elements = [ element.text for element in elements ]
        for tag in self.gen_simple_tag_list(tags):
            if tag in readable_elements:
                element_index = readable_elements.index(tag)
                elements[element_index].click()
                time.sleep(self.wait)

    def gen_simple_tag_list(self, tags):
        tag_list = []
        for tag in tags.values():
            if isinstance(tag, str):
                tag_list.append(tag)
            if isinstance(tag, list):
                for i in tag:
                    tag_list.append(i)
        return tag_list

    def go_to_settings_page(self):
        self.click_button_safe(By.XPATH, "/html/body/main/div/aside/nav/ul/li[5]")

    def go_to_main_groups_page(self):
        self.click_button_safe(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/button[1]")
        self.click_button_safe(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[1]/div/menu/a[2]")

    def return_out_to_main_groups_page(self):
        success = self.attempt_find_element(By.XPATH, "/html/body/div[1]/div/div[2]/a[1]")
        if success:
            self.click_button_safe(By.XPATH, "/html/body/div[1]/div/div[2]/a[1]")
        else:
            self.click_button_safe(By.XPATH, "/html/body/div/div/div[3]/a[1]")

    def retry_group_creation(self, group):
        group_name = group["name"]
        self.driver.refresh()
        self.wait += 0.25
        self.return_out_to_main_groups_page()
        self.delete_group(group)
        self.attempts += 1
        if self.attempts < self.max_attempts:
            print(f"(User {self.id}) Retry group creation {group_name}")
            self.return_out_to_main_groups_page()
            self.create_group(group)
        else:
            self.add_group_status(group_name, f"(User {self.id}) Failed to create group '{group_name}'")
