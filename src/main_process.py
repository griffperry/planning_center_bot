import sys
import traceback
import time
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor
from src.group_manager import GroupManager
from src.data_generator import DataGenerator


class MainProcess():

    def __init__(self, email, password, demo):
        self.email = email
        self.password = password
        self.demo = demo
        self.sessions = []
        self.groups = {}

    def setup_worker(self, id):
        bot = GroupManager(self.email, self.password, self.demo, id)
        if bot.driver:
            bot.go_to_main_groups_page()
        return bot

    def register_session(self, id):
        bot = self.setup_worker(id)
        if bot.driver:
            self.sessions.append(bot)

    def register_sessions(self, bot_count):
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
                    if bot.delete_group(group):
                        bot.add_group_status(name, f"(User {bot.id}) Group '{name}' deleted.")
                    else:
                        bot.add_group_status(name, f"(User {bot.id}) Group '{name}' was not deleted.")
                    bot.reports.append(bot.create_report(name))
                except Exception as error:
                    trace_back_str = traceback.format_exc()
                    print(trace_back_str)
                    sys.exit(1)
            bot.close_session()

    def run_threads(self, command):
        bot_count = len(self.sessions)

        func_ = self.handle_create_group
        if command == "delete_groups":
            func_ = self.handle_delete_group

        start_time = time.time()
        with ThreadPoolExecutor(max_workers=bot_count) as executor:
            executor.map(func_, self.sessions)
        total_time = time.time() - start_time
        print(f"Finished in {total_time} seconds")

    def get_group_data(self, num_groups):
        dg = DataGenerator()  # This will return data from excel spreadsheet
        data = dg.verify_data("test_groups.xlsx")
        data = {
            0: {
                "name": "test group 1",
                "members": {
                    0: {
                        "name": "Griff",
                        "status": "leader",
                        "email": "lgp0008@auburn.edu",
                    },
                    1: {
                        "name": "Dont Exist User",
                        "status": "co-leader",
                        "email": None, # TODO: Do we require co-leader email?
                    },
                },
                "added members": [],
                "schedule": "Thursday @ 11:30 AM Weekly",
                "description": "Test description",
                "contact_email": "test@gmail.com",
                "address": "11306 County Line Rd, Madison, AL 35756",
                "tags": {
                    "campus": "Madison",
                    "year": "2023",
                    "season": "Winter/Spring",
                    "regularity": "Weekly",
                    "group attributes": [
                        "Childcare Available",
                        "Online group",
                    ],
                    "group type": [
                        "Prayer",
                        "Bible Study",
                        "Freedom",
                        "Book Study",
                        "Marriage",
                        "Finance",
                        "Outreach",
                        "Fitness/Health",
                        "Families",
                        "Fun/Hangout/Fellowship",
                        "Students",
                        "College Students",
                        "Other",
                        "Outdoor",
                        "Kids",
                    ],
                    "group age": [
                        "All ages welcome",
                        "Under 18",
                        "18-30",
                        "31-55",
                        "55+",
                        "18 and up",
                    ],
                    "group members": "Men",
                    "day of week": "Thursday",
                },
            },
            1: {
                "name": "test group 2",
                "members": {
                    0: {
                        "name": "Griff Perry",
                        "status": "leader",
                        "email": "lgp0008@auburn.edu",
                    },
                    1: {
                        "name": "Josh Smith",
                        "status": "co-leader",
                        "email": None,
                    },
                },
                "added members": [],
                "schedule": "Thursday @ 11:30 AM Weekly",
                "description": "Test description",
                "contact_email": "lgp0008@auburn.edu",
                "address": "11306 County Line Rd, Madison, AL 35756",
                "tags": {
                    "campus": "Madison",
                    "year": "2023",
                    "season": "Winter/Spring",
                    "regularity": "Weekly",
                    "group attributes": [
                        "Online group",
                    ],
                    "group type": [
                        "Prayer",
                        "Bible Study",
                        "Finance",
                        "Students",
                        "College Students",
                        "Outdoor",
                    ],
                    "group age": [
                        "18-30",
                        "31-55",
                        "55+",
                    ],
                    "group members": "Men",
                    "day of week": "Thursday",
                },
            },
            2: {
                "name": "test group 3",
                "members": {
                    0: {
                        "name": "Alex Springer",
                        "status": "leader",
                        "email": "springer.alex.h@gmail.com",
                    },
                    1: {
                        "name": "Griff",
                        "status": "co-leader",
                        "email": None,
                    },
                },
                "added members": [],
                "schedule": "Thursday @ 11:30 AM Weekly",
                "description": None,
                "contact_email": None,
                "address": "11306 County Line Rd, Madison, AL 35756",
                "tags": {
                    "campus": "Madison",
                    "year": "2023",
                    "season": "Winter/Spring",
                    "regularity": "Weekly",
                    "group attributes": [
                        "Online group",
                    ],
                    "group type": [
                        "Prayer",
                        "Bible Study",
                        "Finance",
                        "Students",
                        "College Students",
                        "Outdoor",
                    ],
                    "group age": [
                        "18-30",
                        "31-55",
                        "55+",
                    ],
                    "group members": "Men",
                    "day of week": "Thursday",
                },
            },
            3: {
                "name": "test group 4",
                "members": {
                    0: {
                        "name": "Alex",
                        "status": "leader",
                        "email": "lgp0008@auburn.edu",
                    },
                    1: {
                        "name": "Josh Smith",
                        "status": "co-leader",
                        "email": None,
                    },
                },
                "added members": [],
                "schedule": "Thursday @ 11:30 AM Weekly",
                "description": "Test description",
                "contact_email": "test@gmail.com",
                "address": "11306 County Line Rd, Madison, AL 35756",
                "tags": {
                    "campus": "Madison",
                    "year": "2023",
                    "season": "Winter/Spring",
                    "regularity": "Weekly",
                    "group attributes": [
                        "Online group",
                    ],
                    "group type": [
                        "Prayer",
                        "Bible Study",
                        "Finance",
                        "Students",
                        "College Students",
                        "Outdoor",
                    ],
                    "group age": [
                        "18-30",
                        "31-55",
                        "55+",
                    ],
                    "group members": "Men",
                    "day of week": "Thursday",
                },
            },
            4: {
                "name": "test group 5",
                "members": {
                    0: {
                        "name": "Griff Perry",
                        "status": "leader",
                        "email": "lgp0008@auburn.edu",
                    },
                    1: {
                        "name": "Alex Springer",
                        "status": "co-leader",
                        "email": None,
                    },
                },
                "added members": [],
                "schedule": "Thursday @ 11:30 AM Weekly",
                "description": "Test description",
                "contact_email": "lgp0008@auburn.edu",
                "address": "11306 County Line Rd, Madison, AL 35756",
                "tags": {
                    "campus": "Madison",
                    "year": "2023",
                    "season": "Winter/Spring",
                    "regularity": "Weekly",
                    "group attributes": [
                        "Online group",
                    ],
                    "group type": [
                        "Prayer",
                        "Bible Study",
                        "Finance",
                        "Students",
                        "College Students",
                        "Outdoor",
                    ],
                    "group age": [
                        "18-30",
                        "31-55",
                        "55+",
                    ],
                    "group members": "Men",
                    "day of week": "Thursday",
                },
            },
            5: {
                "name": "test group 6",
                "members": {
                    0: {
                        "name": "Alex Sp",
                        "status": "leader",
                        "email": "springer.alex.h@gmail.com",
                    },
                    1: {
                        "name": "Griff Perry",
                        "status": "co-leader",
                        "email": None,
                    },
                },
                "added members": [],
                "schedule": "Thursday @ 11:30 AM Weekly",
                "description": "Test description",
                "contact_email": "lgp0008@auburn.edu",
                "address": "11306 County Line Rd, Madison, AL 35756",
                "tags": {
                    "campus": "Madison",
                    "year": "2023",
                    "season": "Winter/Spring",
                    "regularity": "Weekly",
                    "group attributes": [
                        "Online group",
                    ],
                    "group type": [
                        "Prayer",
                        "Bible Study",
                        "Finance",
                        "Students",
                        "College Students",
                        "Outdoor",
                    ],
                    "group age": [
                        "18-30",
                        "31-55",
                        "55+",
                    ],
                    "group members": "Men",
                    "day of week": "Thursday",
                },
            },
        }

        for i in range(num_groups):
            self.groups[i] = data[i]

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

def main_func(email=None, password=None, demo=False, app_run=False, command=None):
    proc = MainProcess(email, password, demo)
    proc.get_group_data(6)  # Just because not officially reading excel file
    bot_count = 1 if len(proc.groups) == 1 else 3

    if not app_run:
        proc.get_login_info()
    try:
        command = sys.argv[-1] if not app_run else command
        if command not in ["create_groups", "delete_groups"]:
            print("Invalid function command.")
            sys.exit(1)
        proc.register_sessions(bot_count)
        if len(proc.sessions) > 0:
            proc.run_threads(command)
            proc.create_report_summary()
        return True
    except Exception:
        trace_back_str = traceback.format_exc()
        print(trace_back_str)
        return False
