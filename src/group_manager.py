import time
from src.planning_center_bot import PlanningCenterBot
from selenium.webdriver.common.by import By

class GroupManager(PlanningCenterBot):

    def __init__(self, email, password, demo):
        self.email = email
        self.password = password
        self.demo = demo
        super().__init__()

    def delete_test_group(self, name):
        self.add_text_to_field(By.XPATH, "//*[@id='groups-index']/div/div[1]/div[2]/div/div[2]/div/input", name)
        self.hit_enter_on_element(By.XPATH, "//*[@id='groups-index']/div/div[1]/div[2]/div/div[2]/div/input")
        # handle when group isn't found
        success = self.attempt_find_element(By.XPATH, "//*[@id='groups-index']/div/div[3]/div[2]/div[3]/div/div/div[2]/div[1]/div[3]/div")
        if success:
            self.click_button(By.XPATH, "//*[@id='groups-index']/div/div[3]/div[2]/div[3]/div/div/div[2]/div[1]/div[3]/div")
            self.click_button(By.XPATH, "/html/body/main/div/aside/nav/ul/li[5]") # go to settings tab
            selected_group = self.attempt_find_element(By.XPATH, "//*[@id='groups-header']/header/div[2]/div[1]/h1")
            if name == selected_group.text:
                self.click_button(By.XPATH, "/html/body/main/div/div/section/header/div/a")
                self.click_button(By.XPATH, "/html/body/div[3]/div/div[3]/div/a")
                self.add_text_to_field(By.XPATH, "/html/body/div[4]/div/div[2]/input[1]", "DELETE")            
                self.hit_enter_on_element(By.XPATH, "/html/body/div[4]/div/div[2]/input[1]")
                print(f"Deleted group '{name}'")
            else:
                print("Selected wrong group.")
        else:
            print(f"Search for group '{name}' failed.")

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
        # TODO: self.add_group_location(group.get("location"))
        # TODO: self.add_group_tags(group.get("tags"))

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

    def go_to_main_groups_page(self):
        self.click_button(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/button[1]")
        self.click_button(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[1]/div/menu/a[2]")

    def return_out_to_main_groups_page(self):
        success = self.attempt_find_element(By.XPATH, "/html/body/div[1]/div/div[2]/a[1]")
        if success:
            self.click_button(By.XPATH, "/html/body/div[1]/div/div[2]/a[1]")
        else:
            self.click_button(By.XPATH, "/html/body/div/div/div[3]/a[1]")
