import sys
import traceback
import time
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor
from src.group_manager import GroupManager
# from src.data_generator import DataGenerator


def setup_worker(email, password, demo, id):
    bot = GroupManager(email, password, demo, id)
    if bot.driver:
        bot.go_to_main_groups_page()
    return bot

def handle_create_group(bot):
    if bot.driver:
        while len(groups) > 0:
            group = groups.pop(next(iter(groups)))
            try:
                bot.create_group(group)
            except Exception as error:
                trace_back_str = traceback.format_exc()
                print(trace_back_str)
                sys.exit(1)
        bot.close_session()

def handle_delete_group(bot):
    if bot.driver:
        while len(groups) > 0:
            group = groups.pop(next(iter(groups)))
            try:
                if bot.delete_group(group):
                    print(f"(User {bot.id}) Group '{group['name']}' deleted.")
            except Exception as error:
                trace_back_str = traceback.format_exc()
                print(trace_back_str)
                sys.exit(1)
        bot.close_session()

def register_session(id):
    bot = setup_worker(email, password, demo, id)
    if bot.driver:
        sessions.append(bot)
    return bot

def register_sessions(bot_count):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=bot_count) as executor:
        executor.map(register_session, range(bot_count))
    total_time = time.time() - start_time
    print(f"Sessions ready in {total_time} seconds.\n")

def run_threads(command):
    bot_count = len(sessions)

    func_ = handle_create_group
    if command == "delete_groups":
        func_ = handle_delete_group

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=bot_count) as executor:
        executor.map(func_, sessions)
    total_time = time.time() - start_time
    print(f"Finished in {total_time} seconds")

def get_group_data(num_groups):
    # data = DataGenerator()
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

    groups = {}
    for i in range(num_groups):
        groups[i] = data[i]
    return groups

def get_login_info():
    global email
    global password
    global demo
    email = input("\nEmail: ")
    password = getpass()
    answer = input("Watch bots? [y/n]: ")
    demo = True if "y" in answer else False
    return email, password, demo

def create_report_summary(sessions):
    file = "small_group_creator_report.txt"
    open(file, "w").close()
    f = open(file, "w")
    for session in sessions:
        for report in session.reports:
            f.write(report)
    f.close()

def main_func(email=None, password=None, demo=False, app_run=False):
    global groups
    groups = get_group_data(6)
    global sessions
    sessions = []

    if not app_run:
        get_login_info()

    try:
        command = sys.argv[-1]
        if not app_run and command not in ["create_groups", "delete_groups"]:
            print("Invalid function command.")
            sys.exit(1)

        bot_count = 1 if len(groups) == 1 else 3
        register_sessions(bot_count)
        if len(sessions) > 0:
            run_threads(command)
            create_report_summary(sessions)

        if app_run and demo:
            register_sessions(bot_count)
            if len(sessions) > 0:
                run_threads("delete_groups")

        return True
    except Exception:
        trace_back_str = traceback.format_exc()
        print(trace_back_str)
        return False
