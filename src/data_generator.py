import pandas as pd
import re
from datetime import datetime
from enum import Enum


class Fields(Enum):

    LEADER_FIRST_NAMES = "First Name"
    LEADER_LAST_NAMES = "Last Name"
    LEADER_EMAILS = "Email"
    LEADER_ADDRESSES = "Address"
    GROUP_CAMPUSES = "What Daystar Campus do you attend?"
    CO_LEADER_NAMES = "Co-Leader Names"
    CO_LEADER_EMAILS = "Co-Leader Emails"
    GROUP_NAMES = "Group Name"
    GROUP_DESCRIPTIONS = "Group Description"
    GROUP_AGE_RANGES = "Age Range?"
    GROUP_GENDERS = "Group Members to be:"
    GROUP_MEET_TYPES = "How will your Small Group meet?"
    GROUP_OUT_HOME_ADDRESSES = "Where will your Group meet? (If address other than your home, just type in address)"
    GROUP_OCCURRENCES = "How often will your Group meet? "
    GROUP_DAYS = "What day will your Group meet?"
    GROUP_TIMES = "What time will your Group meet? (Specify am or pm)"
    GROUP_TYPES = "Type of Small Group (check all that apply)"
    GROUP_CHILDCARE = "Will Childcare be provided?"


class DataGenerator():

    def __init__(self, app_run=False):
        self.data = {}
        self.num_groups = 0
        self.app_run = app_run
        self.num_test_groups = 6
        self.campus = "Madison"

    def verify_data(self, data_file):
        data_object = self.get_excel_sheet_object(data_file)
        self.translate_data(data_object)
        return True

    def filter_on_campus(self, file_object):
        file_object = file_object.loc[file_object[Fields.GROUP_CAMPUSES.value] == self.campus]
        return file_object

    def get_excel_sheet_object(self, data_file):
        file_object = pd.read_excel(data_file)
        file_object = file_object.fillna('')
        campus_data = self.filter_on_campus(file_object)
        return campus_data

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
            self._gen_members_data(index, groups, data_object)
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
        self.num_groups = self.num_groups if self.app_run else self.num_test_groups
        for i in range(self.num_groups):
            self.data[i] = groups[i]

    def _gen_data_list(self, data_object, column_name):
        return data_object[column_name].to_list()

    def _gen_members_data(self, index, groups, data_object):
        leader_first_names = self._gen_data_list(data_object, Fields.LEADER_FIRST_NAMES.value)
        leader_last_names = self._gen_data_list(data_object, Fields.LEADER_LAST_NAMES.value)
        leader_emails = self._gen_data_list(data_object, Fields.LEADER_EMAILS.value)
        groups[index]["members"] = {
            0: {
                "name": f"{leader_first_names[index].strip()} {leader_last_names[index].strip()}",
                "status": "leader",
                "email": f"{leader_emails[index].strip()}" if leader_emails[index] else None,
            },
        }

        co_leader_names = []
        for co_index, co_leader in enumerate(self._gen_data_list(data_object, Fields.CO_LEADER_NAMES.value)):
            co_leader_names.append(co_leader)
            if " and " in co_leader:
                co_leader_names[co_index] = co_leader.split("and")
            if " // " in co_leader:
                co_leader_names[co_index] = co_leader.split("//")

        co_leader_emails = []
        for co_index, co_leader in enumerate(self._gen_data_list(data_object, Fields.CO_LEADER_EMAILS.value)):
            co_leader_emails.append(co_leader)
            if " and " in co_leader:
                co_leader_emails[co_index] = co_leader.split("and")
            if " // " in co_leader:
                co_leader_emails[co_index] = co_leader.split("//")

        if isinstance(co_leader_names[index], list) and isinstance(co_leader_emails[index], list):
            for co_index, co_leader_name in enumerate(co_leader_names[index]):
                groups[index]["members"][co_index + 1] = {}
                groups[index]["members"][co_index + 1]["name"] = co_leader_name.strip()
                groups[index]["members"][co_index + 1]["status"] = "co-leader"
            for co_index, co_leader_email in enumerate(co_leader_emails[index]):
                groups[index]["members"][co_index + 1]["email"] = co_leader_email.strip() if co_leader_email else None
        else:
            groups[index]["members"][1] = {
                    "name": f"{co_leader_names[index].strip()}",
                    "status": "co-leader",
                    "email": f"{co_leader_emails[index].strip()}" if co_leader_emails[index] else None,
                }

    def _gen_schedule_data(self, idx, groups, data_object):
        group_occurrences = self._gen_data_list(data_object, Fields.GROUP_OCCURRENCES.value)
        group_days = self._gen_data_list(data_object, Fields.GROUP_DAYS.value)
        group_times = self._gen_data_list(data_object, Fields.GROUP_TIMES.value)
        self._format_group_days(group_days)
        self._format_group_times(group_times)
        groups[idx]["schedule"] = f"{group_days[idx]} @ {group_times[idx]} {group_occurrences[idx]}"

    def _format_group_days(self, group_days):
        for idx, set_days in enumerate(group_days):
            day_string = ""
            days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday",
                                "Friday", "Saturday", "Sunday"]
            for day in days_of_the_week:
                if day in set_days:
                    day_string += f"{day}, "

            group_days[idx] = day_string.rstrip(", ") if "," in day_string else day_string

    def _format_group_times(self, group_times):
        for idx, time in enumerate(group_times):
            hour = None
            time_period = "AM" if "a" in time.lower() else "PM"
            result = re.search(r'\d{2}', time)
            all_digits = re.findall(r'\d', time)
            if result:
                if "1" == result.group(0)[0]:
                    hour = result.group(0)
                elif "0" == result.group(0)[0] and result.group(0)[0] == all_digits[0]:
                    hour = result.group(0)[1]
                elif result.group(0)[0] == all_digits[0]:
                    hour = all_digits[0]
            if all_digits:
                minute = "00"
                if hour is None:
                    hour = all_digits[0]
                if len(all_digits) != 1:
                    hour_past = False
                    for val in all_digits:
                        if val in ["0", "3"]:
                            if val != hour and val != "0":
                                minute = f"{val}0"
                                break
                            elif val == hour and not hour_past:
                                hour_past = True
                                continue
                            elif hour_past:
                                minute = f"{val}0"
                                break
                group_times[idx] = f"{hour}:{minute} {time_period}"
            else:
                group_times[idx] = "TBD"

    def _gen_address_data(self, index, groups, data_object):
        groups_meet_type = self._gen_data_list(data_object, Fields.GROUP_MEET_TYPES.value)
        groups_out_home_address = self._gen_data_list(data_object, Fields.GROUP_OUT_HOME_ADDRESSES.value)
        leader_addresses = self._gen_data_list(data_object, Fields.LEADER_ADDRESSES.value)
        if "In Home" in groups_meet_type[index]:
            if groups_out_home_address[index]:
                groups[index]["address"] = groups_out_home_address[index]
            else:
                groups[index]["address"] = leader_addresses[index].strip("Home:/\n")
        elif groups_meet_type[index] != "Online":
            groups[index]["address"] = groups_out_home_address[index]
        else:
            groups[index]["address"] = ''
        self._format_group_address(index, groups)

    def _format_group_address(self, index, groups):
        if groups[index]["address"] != '':
            address = groups[index]["address"]
            address_number = re.search("\d+", address.split(" ")[0])
            if address_number is None:
                groups[index]["address"] = ''
            else:
                groups[index]["address"] = address.replace("\n", " ")

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
