import pandas as pd


class DataGenerator():
    def __init__(self):
        self.valid = False  # default
        self.data = {}
        self.num_groups = 0

    def verify_data(self, data):
        print(f"Verify {data}")
        file_object = pd.read_excel(data)
        groups = self.translate_data(file_object)
        print(groups)
        """
        groups = {
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
        """
        for i in range(self.num_groups):
            self.data[i] = groups[i]

    def translate_data(self, data_object):
        # import pdb; pdb.set_trace()
        groups = {}
        group_names = data_object["Unnamed: 15"].to_list()[1:]
        self.num_groups = len(group_names)
        for index in range(self.num_groups):
            groups[index] = {}

        leader_first_names = data_object["Unnamed: 1"].to_list()[1:]
        leader_last_names = data_object["Unnamed: 2"].to_list()[1:]
        leader_emails = data_object["Unnamed: 3"].to_list()[1:]
        leader_addresses = data_object["Unnamed: 7"].to_list()[1:]
        group_campuses = data_object["Unnamed: 8"].to_list()[1:]
        co_leader_names = data_object["Unnamed: 11"].to_list()[1:]
        co_leader_emails = data_object["Unnamed: 12"].to_list()[1:]
        group_descriptions = data_object["Unnamed: 16"].to_list()[1:]
        group_age_ranges = data_object["Unnamed: 17"].to_list()[1:]
        group_genders = data_object["Unnamed: 18"].to_list()[1:]
        groups_in_home = data_object["Unnamed: 19"].to_list()[1:]
        groups_out_home = data_object["Unnamed: 20"].to_list()[1:]
        group_occurences = data_object["Unnamed: 21"].to_list()[1:]
        group_days = data_object["Unnamed: 22"].to_list()[1:]
        group_times = data_object["Unnamed: 23"].to_list()[1:]
        group_types = data_object["Unnamed: 24"].to_list()[1:]
        group_childcare = data_object["Unnamed: 25"].to_list()[1:]

        for index, name in enumerate(group_names):
            groups[index]["name"] = name
        # for index in range(self.num_groups):
        #     groups[index]["members"] = name
        for index in range(self.num_groups):
            groups[index]["added_members"] = []
        # for index in range(self.num_groups):
        #     groups[index]["schedule"] = name
        for index, description in enumerate(group_descriptions):
            groups[index]["description"] = description
        for index, email in enumerate(leader_emails):
            groups[index]["contact_email"] = email
        # for index in range(self.num_groups):
        #     groups[index]["address"] = name
        # for index in range(self.num_groups):
        #     groups[index]["tags"] = name

        return groups
