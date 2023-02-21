import sys
import traceback
import time
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor
from src.group_manager import GroupManager
# from src.data_generator import DataGenerator


def setup_worker(email, password, demo):
    bot = GroupManager(email, password, demo)
    if bot.driver:
        bot.go_to_main_groups_page()
    return bot

def handle_create_group(bot, group):
    if bot.driver:
        try:
            bot.create_group(group)
            print(f"Group '{group['name']}' created.")
        except Exception as error:
            trace_back_str = traceback.format_exc()
            print(trace_back_str)
            sys.exit(1)

def handle_delete_group(bot, group):
    if bot.driver:
        try:
            bot.delete_group(group.get("name"))
        except Exception as error:
            trace_back_str = traceback.format_exc()
            print(trace_back_str)
            sys.exit(1)

def register_session(email, password, demo):
    start_time = time.time()
    bot = setup_worker(email, password, demo)
    total_time = time.time() - start_time
    if bot.driver:
        print(f"Session ready in {total_time} seconds\n")
    return bot

def register_sessions(bot_count, email, password, demo):
    sessions = [ register_session(email, password, demo) for _ in range(bot_count) ]
    return sessions

def gen_bots_list(bots, groups):
    bot_count = len(bots)
    if bot_count < 1:
        print("Error: no bots to run with.")
        sys.exit(1)
    bots *= int(len(groups)/bot_count)
    if (len(groups) % 2) == 1:
        bots.append(bots[0])
    return bots

def run_threads(bots, groups, command):
    bot_count = len(bots)
    gen_bots_list(bots, groups)

    func_ = handle_create_group
    action = "Created"
    if command == "delete_groups":
        func_ = handle_delete_group
        action = "Deleted"

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=bot_count) as executor:
        executor.map(func_, bots, groups)
    for bot in bots[:bot_count]:
        bot.close_session()
    total_time = time.time() - start_time
    print(f"{action} all groups in {total_time} seconds")

def get_group_data(num_groups):
    # data = DataGenerator()
    data = {
        0: {
            "name": "test group 1",
            "leader": "Griff Perry",
            "co-leader": "Josh Smith",
            "added members": [],
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
        1: {
            "name": "test group 2",
            "leader": "Griff Perry",
            "co-leader": "Alex Springer",
            "added members": [],
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
        2: {
            "name": "test group 3",
            "leader": "Alex Springer",
            "co-leader": "Griff Perry",
            "added members": [],
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
        3: {
            "name": "test group 4",
            "leader": "Griff Perry",
            "co-leader": "Josh Smith",
            "added members": [],
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
        4: {
            "name": "test group 5",
            "leader": "Griff Perry",
            "co-leader": "Alex Springer",
            "added members": [],
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
        5: {
            "name": "test group 6",
            "leader": "Griff Perry",
            "co-leader": "Kaylee Perry",
            "added members": [],
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

    groups = {}
    for i in range(num_groups):
        groups[i] = data[i]
    return groups.values()

def get_login_info():
    email = input("\nEmail: ")
    password = getpass()
    answer = input("Watch bots? [y/n]: ")
    demo = True if "y" in answer else False
    return email, password, demo

def main_func(email=None, password=None, demo=False, app_run=False):
    groups = get_group_data(6)
    sessions = []

    if not app_run:
        email, password, demo = get_login_info()

    try:
        command = sys.argv[-1]
        if not app_run and command not in ["create_groups", "delete_groups"]:
            print("Invalid function command.")
            sys.exit(1)

        bot_count = 1 if len(groups) == 1 else 2
        sessions = register_sessions(bot_count, email, password, demo)
        if len(sessions) > 0:
            run_threads(sessions, groups, command)

        if app_run and demo:
            sessions = register_sessions(bot_count, email, password, demo)
            if len(sessions) > 0:
                run_threads(sessions, groups, "delete_groups")

        return True
    except Exception:
        trace_back_str = traceback.format_exc()
        print(trace_back_str)
        return False
