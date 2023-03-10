import pandas


class DataGenerator():
    def __init__(self):
        self.valid = False  # default
        self.data = {}
        self.num_groups = 1

    def verify_data(self, data):
        print(f"Verify {data}")
        if True:
            self.valid = True
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
        for i in range(self.num_groups):
            self.data[i] = groups[i]

    def submit_data(self, data):
        # data: string (filepath to excel)
        self.verify_data(data)
        return self.valid
