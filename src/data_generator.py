import pandas as pd
from datetime import datetime
from enum import Enum


class Fields(Enum):

    LEADER_FIRST_NAMES = "Unnamed: 1"
    LEADER_LAST_NAMES = "Unnamed: 2"
    LEADER_EMAILS = "Unnamed: 3"
    LEADER_ADDRESSES = "Unnamed: 7"
    GROUP_CAMPUSES = "Unnamed: 8"
    CO_LEADER_NAMES = "Unnamed: 11"
    CO_LEADER_EMAILS = "Unnamed: 12"
    GROUP_NAMES = "Unnamed: 15"
    GROUP_DESCRIPTIONS = "Unnamed: 16"
    GROUP_AGE_RANGES = "Unnamed: 17"
    GROUP_GENDERS = "Unnamed: 18"
    GROUP_MEET_TYPES = "Unnamed: 19"
    GROUP_OUT_HOME_ADDRESSES = "Unnamed: 20"
    GROUP_OCCURRENCES = "Unnamed: 21"
    GROUP_DAYS = "Unnamed: 22"
    GROUP_TIMES = "Unnamed: 23"
    GROUP_TYPES = "Unnamed: 24"
    GROUP_CHILDCARE = "Unnamed: 25"
    GROUP_MEMBERS = "Unnamed: 27"


class DataGenerator():

    def __init__(self, app_run=False):
        self.data = {}
        self.num_groups = 0
        self.app_run = app_run
        self.num_test_groups = 6

    def verify_data(self, data_file):
        file_object = pd.read_excel(data_file)
        file_object = file_object.fillna('')
        self.translate_data(file_object)
        return True

    def translate_data(self, data_object):
        groups = {}
        leader_emails = self._gen_data_list(data_object, Fields.LEADER_EMAILS.value)
        group_descriptions = self._gen_data_list(data_object, Fields.GROUP_DESCRIPTIONS.value)
        group_names = self._gen_data_list(data_object, Fields.GROUP_NAMES.value)
        self.num_groups = len(group_names)

        for index in range(self.num_groups):
            groups[index] = {}
        for index, name in enumerate(group_names):
            groups[index]["name"] = name.strip().upper()
        for index in range(self.num_groups):
            self._gen_leaders_data(index, groups, data_object)
        for index in range(self.num_groups):
            groups[index]["added members"] = []
        for index in range(self.num_groups):
            self._gen_schedule_data(index, groups, data_object)
        for index, description in enumerate(group_descriptions):
            groups[index]["description"] = description
        for index, email in enumerate(leader_emails):
            groups[index]["contact_email"] = email
        for index in range(self.num_groups):
            self._gen_address_data(index, groups, data_object)
        for index in range(self.num_groups):
            self._gen_tags_data(index, groups, data_object)
        for index in range(self.num_groups):
            self._gen_attendees_data(index, groups, data_object)

        self.num_groups = self.num_groups if self.app_run else self.num_test_groups
        for i in range(self.num_groups):
            self.data[i] = groups[i]

    def _gen_data_list(self, data_object, column):
        return data_object[column].to_list()[1:]

    def _gen_leaders_data(self, index, groups, data_object):
        leader_first_names = self._gen_data_list(data_object, Fields.LEADER_FIRST_NAMES.value)
        leader_last_names = self._gen_data_list(data_object, Fields.LEADER_LAST_NAMES.value)
        leader_emails = self._gen_data_list(data_object, Fields.LEADER_EMAILS.value)
        co_leader_names = self._gen_data_list(data_object, Fields.CO_LEADER_NAMES.value)
        co_leader_emails = self._gen_data_list(data_object, Fields.CO_LEADER_EMAILS.value)
        groups[index]["members"] = {
            0: {
                "name": f"{leader_first_names[index].strip()} {leader_last_names[index].strip()}",
                "status": "leader",
                "email": f"{leader_emails[index].strip()}" if leader_emails[index] else None,
            },
            1: {
                "name": f"{co_leader_names[index].strip()}",
                "status": "co-leader",
                "email": f"{co_leader_emails[index].strip()}" if co_leader_emails[index] else None,
            }
        }

    def _gen_attendees_data(self, index, groups, data_object):
        groups[index]["attendees"] = self._get_attendees(index, data_object)

    def _gen_schedule_data(self, idx, groups, data_object):
        group_occurences = self._gen_data_list(data_object, Fields.GROUP_OCCURRENCES.value)
        group_days = self._gen_data_list(data_object, Fields.GROUP_DAYS.value)
        group_times = self._gen_data_list(data_object, Fields.GROUP_TIMES.value)
        groups[idx]["schedule"] = f"{group_days[idx]} @ {group_times[idx]} {group_occurences[idx]}"

    def _gen_address_data(self, index, groups, data_object):
        groups_meet_type = self._gen_data_list(data_object, Fields.GROUP_MEET_TYPES.value)
        groups_out_home_address = self._gen_data_list(data_object, Fields.GROUP_OUT_HOME_ADDRESSES.value)
        leader_addresses = self._gen_data_list(data_object, Fields.LEADER_ADDRESSES.value)
        if groups_meet_type[index] == "In Home":
            groups[index]["address"] = leader_addresses[index].strip("Home:/\n")
        elif groups_meet_type[index] != "Online":
            groups[index]["address"] = groups_out_home_address[index]
        else:
            groups[index]["address"] = None

    def _gen_tags_data(self, index, groups, data_object):
        group_campuses = self._gen_data_list(data_object, Fields.GROUP_CAMPUSES.value)
        group_occurences = self._gen_data_list(data_object, Fields.GROUP_OCCURRENCES.value)
        group_days = self._gen_data_list(data_object, Fields.GROUP_DAYS.value)
        group_genders = self._gen_data_list(data_object, Fields.GROUP_GENDERS.value)
        groups[index]["tags"] = {
            "campus": group_campuses[index],
            "year": self._get_year(),
            "season": self._get_season(),
            "regularity": group_occurences[index],
            "group attributes": self._get_attributes(index, data_object),
            "group type": self._get_types(index, data_object),
            "group age": self._get_age_range(index, data_object),
            "group members": group_genders[index],
            "day of week": group_days[index],
        }

    def _get_year(self):
        return str(datetime.now().year)

    def _get_season(self):
        current_month = datetime.now().month
        if current_month in [1, 2, 3, 4]:
            return "Winter/Spring"
        if current_month in [5, 6, 7]:
            return "Summer"
        return "Fall"

    def _get_attributes(self, index, data_object):
        attributes = []
        groups_meet_type = self._gen_data_list(data_object, Fields.GROUP_MEET_TYPES.value)
        group_childcare = self._gen_data_list(data_object, Fields.GROUP_CHILDCARE.value)
        if groups_meet_type[index] == "Online":
            attributes.append("Online group")
        if group_childcare[index].lower() == "yes":
            attributes.append("Childcare Available")
        return attributes

    def _get_types(self, index, data_object):
        all_group_types = self._gen_data_list(data_object, Fields.GROUP_TYPES.value)
        group_types = all_group_types[index]
        if "," in group_types:
            group_types_list = group_types.split(",")
            group_types = []
            for group_type in group_types_list:
                group_types.append(group_type.strip())
            return group_types
        return [group_types]

    def _get_attendees(self, index, data_object):
        all_attendees = self._gen_data_list(data_object, Fields.GROUP_MEMBERS.value)
        attendees = all_attendees[index]
        if "," in attendees:
            attendees_list = attendees.split(",")
            attendees = []
            for attendee in attendees_list:
                attendees.append(attendee.strip())
            return attendees
        return [attendees]

    def _get_age_range(self, index, data_object):
        all_age_ranges = self._gen_data_list(data_object, Fields.GROUP_AGE_RANGES.value)
        age_ranges = all_age_ranges[index]
        if "," in age_ranges:
            age_range_list = age_ranges.split(",")
            age_ranges = []
            for age_range in age_range_list:
                age_ranges.append(age_range.strip())
            return age_ranges
        return [age_ranges]
