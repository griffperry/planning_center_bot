#!/usr/bin/env python3

import sys
import traceback
import time
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor
from group_manager import GroupManager


def setup_worker(email, password, demo):
    bot = GroupManager(email, password, demo)
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

def run_threads(bot_count, bots, groups):
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

    command = sys.argv[1:]
    if command == "create_groups":
        sessions = register_sessions(bot_count, email, password, demo)
        run_threads(bot_count, sessions, groups.values())
    elif command == "delete_groups":
        delete_groups(groups.values(), email, password, demo)
    else:
        print("Invalid command line argument")

if __name__ == "__main__":
    main()
