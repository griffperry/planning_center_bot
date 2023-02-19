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
    print(f"Registered sessions in {total_time} seconds\n")
    return bot

def run_threads(bot_count, bots, groups):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=bot_count) as executor:
        bots *= int(len(groups)/bot_count)
        executor.map(handle_create_group, bots, groups)
    for bot in bots[:bot_count]:
        bot.close_session()
    total_time = time.time() - start_time
    print(f"Created all groups in {total_time} seconds")

def delete_groups(groups, email, password, demo):
    start_time = time.time()
    bot = setup_worker(email, password, demo)
    try:
        for group in groups:
            handle_delete_group(bot, group)
    finally:
        if bot:
            bot.close_session()
    total_time = time.time() - start_time
    print(f"Deleted all groups in {total_time} seconds")

def get_group_data(num_groups):
    # data = DataGenerator()
    data = {
        0: {
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
        1: {
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
        2: {
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
        3: {
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
        4: {
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
        5: {
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

    groups = {}
    for i in range(num_groups):
        groups[i] = data[i]
    return groups.values()

def get_login_info():
    email = input("\nEmail: ")
    password = getpass()
    answer = input("Would you like to demo? [y/n]: ")
    demo = True if "y" in answer else False
    return email, password, demo

def main_func(email=None, password=None, demo=False, app_run=False):
    groups = get_group_data(4)
    sessions = []

    if not app_run:
        email, password, demo = get_login_info()

    try:
        command = sys.argv[-1]
        if command == "create_groups" or app_run:
            bot_count = 2 if (len(groups) % 2) == 0 else 1
            sessions.append(register_session(email, password, demo))
            if bot_count > 1:
                sessions.append(register_session(email, password, demo))
            if sessions:
                run_threads(bot_count, sessions, groups)
        if command == "delete_groups" or app_run:
            delete_groups(groups, email, password, demo)
        return True
    except Exception:
        trace_back_str = traceback.format_exc()
        print(trace_back_str)
        sys.exit(1)
