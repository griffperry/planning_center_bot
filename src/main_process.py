import sys
import traceback
import time
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor
from src.group_manager import GroupManager
from src.data_generator import DataGenerator


class MainProcess():

    def __init__(self,
                 email=None,
                 password=None,
                 maps_api_key=None,
                 completed_groups=None,
            ):
        self.email = email
        self.password = password
        self.maps_api_key = maps_api_key
        self.login_success = False
        self.completed_groups = completed_groups
        self.num_workers = 1
        self.sessions = []

    def register_session(self, id):
        bot = GroupManager(self.email, self.password, id)
        if bot.backend.logged_in:
            self.login_success = True
            bot.maps_api_key = self.maps_api_key
            self.sessions.append(bot)
        else:
            print(f"(User {bot.id}) Failed to login.")

    def register_sessions(self):
        num_groups = len(self.groups)
        bot_count = num_groups if num_groups < self.num_workers else self.num_workers
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=bot_count) as executor:
            executor.map(self.register_session, range(bot_count))
        total_time = time.time() - start_time
        if self.login_success:
            print(f"Sessions ready in {total_time} seconds.\n")

    def handle_create_group(self, bot):
        while len(self.groups) > 0:
            group = self.groups.pop(next(iter(self.groups)))
            try:
                group_name = group["name"]
                print(f"(User {bot.id}) Start create group {group_name}")
                bot.create_group(group)
                self.completed_groups.append(group_name)
            except:
                trace_back_str = traceback.format_exc()
                print(trace_back_str)
                sys.exit(1)

    def handle_delete_group(self, bot):
        while len(self.groups) > 0:
            group = self.groups.pop(next(iter(self.groups)))
            try:
                group_name = group["name"]
                print(f"(User {bot.id}) Start delete group {group_name}")
                bot.delete_group(group)
                self.completed_groups.append(group_name)
            except:
                trace_back_str = traceback.format_exc()
                print(trace_back_str)
                sys.exit(1)

    def run_threads(self):
        bot_count = len(self.sessions)
        func_ = self.handle_create_group
        if self.command == "delete_groups":
            func_ = self.handle_delete_group
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=bot_count) as executor:
            executor.map(func_, self.sessions)
        total_time = time.time() - start_time
        print(f"Finished in {total_time} seconds")
        self.create_report_summary()

    def get_group_data(self):
        """ Function used for local testing """
        dg = DataGenerator()
        dg.verify_data("src/test_groups.xlsx")
        return dg.data

    def get_login_info(self):
        self.email = input("\nEmail: ")
        self.password = getpass()

    def get_maps_api_key(self):
        self.maps_api_key = input("Api Key: ")

    def create_report_summary(self):
        file = "small_groups_report.txt"
        open(file, "w").close()
        f = open(file, "w")
        for session in self.sessions:
            for report in session.reports:
                f.write(report)
        f.close()

    def main_func(self, app_run=False, command=None):
        self.command = sys.argv[-1] if not app_run else command
        if self.command not in ["create_groups", "delete_groups"]:
            print("Invalid function command.")
            sys.exit(1)

        self.success = False
        try:
            if not app_run:
                self.get_login_info()
                if self.command == "create_groups":
                    self.get_maps_api_key()
                self.groups = self.get_group_data()
                self.completed_groups = []
                self.register_sessions()
            if len(self.sessions) > 0:
                self.run_threads()
                self.success = True
        except Exception:
            trace_back_str = traceback.format_exc()
            print(trace_back_str)
