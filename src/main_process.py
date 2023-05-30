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
                 demo=None,
                 completed_groups=None,
            ):
        self.email = email
        self.password = password
        self.demo = demo
        self.completed_groups = completed_groups
        self.sessions = []

    def setup_worker(self, id):
        bot = GroupManager(self.email, self.password, self.demo, id)
        if bot.driver:
            bot.go_to_main_groups_page()
        return bot

    def register_session(self, id):
        bot = self.setup_worker(id)
        if bot.driver:
            self.sessions.append(bot)

    def register_sessions(self):
        num_groups = len(self.groups)
        bot_count = num_groups if num_groups < 3 else 3
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=bot_count) as executor:
            executor.map(self.register_session, range(bot_count))
        total_time = time.time() - start_time
        print(f"Sessions ready in {total_time} seconds.\n")

    def handle_create_group(self, bot):
        if bot.driver:
            while len(self.groups) > 0:
                group = self.groups.pop(next(iter(self.groups)))
                try:
                    bot.create_group(group)
                    self.completed_groups.append(group["name"])
                except Exception as error:
                    trace_back_str = traceback.format_exc()
                    print(trace_back_str)
                    sys.exit(1)
            bot.close_session()

    def handle_delete_group(self, bot):
        if bot.driver:
            while len(self.groups) > 0:
                group = self.groups.pop(next(iter(self.groups)))
                try:
                    name = group["name"]
                    message = "was not deleted"
                    if bot.delete_group(group):
                        message = "deleted"
                    bot.add_group_status(name, f"(User {bot.id}) Group '{name}' {message}.")
                    bot.reports.append(bot.create_report(name))
                    self.completed_groups.append(name)
                except Exception as error:
                    trace_back_str = traceback.format_exc()
                    print(trace_back_str)
                    sys.exit(1)
            bot.close_session()

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
        dg = DataGenerator()
        dg.verify_data("src/test_groups.xlsx")
        return dg.data

    def get_login_info(self):
        self.email = input("\nEmail: ")
        self.password = getpass()
        answer = input("Watch bots? [y/n]: ")
        self.demo = True if "y" in answer else False

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
        if not app_run:
            self.get_login_info()
            self.groups = self.get_group_data()
            self.completed_groups = []
        try:
            self.register_sessions()
            if len(self.sessions) > 0:
                self.run_threads()
                self.success = True
        except Exception:
            trace_back_str = traceback.format_exc()
            print(trace_back_str)
