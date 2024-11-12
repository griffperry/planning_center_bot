import pandas as pd
import re
from datetime import datetime
import datetime as dt
from enum import Enum
from planning_center_backend import groups as pcb_groups


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
        self.num_test_groups = 1
        self.campus = "Madison"

    def verify_data(self, data_file):
        data_object = self.get_excel_sheet_object(data_file)
        self.translate_data(data_object)
        return True

    def get_excel_sheet_object(self, data_file):
        file_object = pd.read_excel(data_file)
        file_object = file_object.fillna('')
        campus_data = self.filter_on_campus(file_object)
        return campus_data

    def filter_on_campus(self, file_object):
        file_object = file_object.loc[file_object[Fields.GROUP_CAMPUSES.value] == self.campus]
        return file_object

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
        # self.num_groups = self.num_groups if self.app_run else self.num_test_groups
        for i in range(self.num_groups):
            self.data[i] = groups[i]

    def _gen_data_list(self, data_object, column_name):
        return data_object[column_name].to_list()

    def _gen_members_data(self, index, groups, data_object):
        leader_first_names = self._gen_data_list(data_object, Fields.LEADER_FIRST_NAMES.value)
        leader_last_names = self._gen_data_list(data_object, Fields.LEADER_LAST_NAMES.value)
        leader_emails = self._gen_data_list(data_object, Fields.LEADER_EMAILS.value)
        co_leader_names = []
        co_leader_emails = []
        groups[index]["members"] = {
            0: {
                "name": f"{leader_first_names[index].strip()} {leader_last_names[index].strip()}",
                "status": "leader",
                "email": leader_emails[index].strip() if leader_emails[index] else None,
            },
        }

        def format_co_leader_info(info):
            if "and" in info:
                return info.split("and")
            if "//" in info:
                return info.split("//")
            return info

        for co_leader_name in self._gen_data_list(data_object, Fields.CO_LEADER_NAMES.value):
            co_leader_names.append(format_co_leader_info(co_leader_name))
        for co_leader_email in self._gen_data_list(data_object, Fields.CO_LEADER_EMAILS.value):
            co_leader_emails.append(format_co_leader_info(co_leader_email))

        co_leader_name = co_leader_names[index]
        co_leader_email = co_leader_emails[index]
        if isinstance(co_leader_name, list) and isinstance(co_leader_email, list):
            for co_index, co_leader_name in enumerate(co_leader_name, 1):
                groups[index]["members"][co_index] = {}
                groups[index]["members"][co_index]["name"] = co_leader_name.strip()
                groups[index]["members"][co_index]["status"] = "co-leader"
            for co_index, co_leader_email in enumerate(co_leader_email, 1):
                groups[index]["members"][co_index]["email"] = co_leader_email.strip()
        else:
            groups[index]["members"][1] = {
                    "name": co_leader_name.strip(),
                    "status": "co-leader",
                    "email": co_leader_email.strip() if co_leader_email else None,
                }

    def _gen_schedule_data(self, idx, groups, data_object):
        group_occurrences = self._gen_data_list(data_object, Fields.GROUP_OCCURRENCES.value)
        group_occurrences = [ x.strip() for x in group_occurrences ]
        group_days = self._gen_data_list(data_object, Fields.GROUP_DAYS.value)
        group_times = self._gen_data_list(data_object, Fields.GROUP_TIMES.value)
        self._format_group_days(group_days)
        self._format_group_times(group_times)
        groups[idx]["schedule"] = f"{group_days[idx]} @ {group_times[idx]} {group_occurrences[idx]}"

        if "Monday" in group_days[idx]:
            weekday = pcb_groups.GroupMeetingWeekday.Monday
        elif "Tuesday" in group_days[idx]:
            weekday = pcb_groups.GroupMeetingWeekday.Tuesday
        elif "Wednesday" in group_days[idx]:
            weekday = pcb_groups.GroupMeetingWeekday.Wednesday
        elif "Thursday" in group_days[idx]:
            weekday = pcb_groups.GroupMeetingWeekday.Thursday
        elif "Friday" in group_days[idx]:
            weekday = pcb_groups.GroupMeetingWeekday.Friday
        elif "Saturday" in group_days[idx]:
            weekday = pcb_groups.GroupMeetingWeekday.Saturday
        elif "Sunday" in group_days[idx]:
            weekday = pcb_groups.GroupMeetingWeekday.Sunday
        else:
            raise ValueError("Cannot parse weekday")

        start = dt.datetime.strptime(group_times[idx], "%I:%M %p")
        end = start + dt.timedelta(hours=2)

        if group_occurrences[idx] == "Weekly":
            meeting_settings = pcb_groups.GroupMeetingSettings.weekly(
                weekday=weekday,
                start_time=start.time(),
                end_time=end.time(),
            )
        elif group_occurrences[idx] == "Bi-weekly":
            meeting_settings = pcb_groups.GroupMeetingSettings.biweekly(
                weekday=weekday,
                start_time=start.time(),
                end_time=end.time(),
            )
        else:
            raise ValueError("Cannot parse meeting schedule")
        groups[idx]["meeting_settings"] = meeting_settings

    def _format_group_days(self, group_days):
        for idx, set_days in enumerate(group_days):
            day_string = ""
            days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday",
                                "Friday", "Saturday", "Sunday"]
            for day in days_of_the_week:
                if day in set_days:
                    day_string += f"{day}, "
            group_days[idx] = day_string.rstrip(", ")

    def _format_group_times(self, group_times):
        for idx, time in enumerate(group_times):
            group_times[idx] = "TBD"
            time_period = "AM" if "a" in time.lower() else "PM"
            result = re.search(r'\d{2}', time)
            all_nums = re.findall(r'\d', time)
            hour = all_nums[0] if all_nums else None
            if result and result.group(0) == f"{all_nums[0]}{all_nums[1]}":
                if all_nums[0] == "1" and all_nums[1] in ["0", "1", "2"]:
                    hour = result.group(0)
                elif all_nums[0] == "0":
                    hour = all_nums[1]
            minute = "00"
            if all_nums:
                if len(all_nums) > 1:
                    hour_past = False
                    for val in all_nums:
                        if val == "3":
                            if hour == "3" and not hour_past:
                                hour_past = True
                            else:
                                minute = "30"
                                break
                group_times[idx] = f"{hour}:{minute} {time_period}"

    def _gen_address_data(self, index, groups, data_object):
        groups_meet_type = self._gen_data_list(data_object, Fields.GROUP_MEET_TYPES.value)
        groups_out_home_address = self._gen_data_list(data_object, Fields.GROUP_OUT_HOME_ADDRESSES.value)
        leader_addresses = self._gen_data_list(data_object, Fields.LEADER_ADDRESSES.value)
        groups[index]["address"] = groups_out_home_address[index]
        if "In Home" in groups_meet_type[index] and groups_out_home_address[index] == '':
            groups[index]["address"] = leader_addresses[index].strip("Home:/\n")
        self._format_group_address(index, groups)

    def _format_group_address(self, index, groups):
        if groups[index]["address"]:
            address = groups[index]["address"]
            first_address_value = address.split(" ")[0]
            address_number = re.search("\d+", first_address_value)
            groups[index]["address"] = ''
            if address_number is not None:
                groups[index]["address"] = address.replace("\n", " ")

    def _gen_tags_data(self, index, groups, data_object):
        group_campuses = self._gen_data_list(data_object, Fields.GROUP_CAMPUSES.value)
        group_occurrences = self._gen_data_list(data_object, Fields.GROUP_OCCURRENCES.value)
        formatted_regularity = [ self._format_group_occurrence(x) for x in group_occurrences ]
        group_days = self._gen_data_list(data_object, Fields.GROUP_DAYS.value)
        self._format_group_days(group_days)
        groups[index]["tags"] = {
            "campus": group_campuses[index],
            "year": self._get_year(),
            "season": self._get_season(),
            "regularity": formatted_regularity[index],
            "group attributes": self._get_attributes(index, data_object),
            "group type": self._get_types(index, data_object),
            "group age": self._get_age_range(index, data_object),
            "group members": self._get_genders(index, data_object),
            "day of week": [group_days[index]],
        }

    def _format_group_occurrence(self, occurrence):
        if occurrence.lower() == "bi-weekly":
            return "Every Other Week"
        valid_occurrences = [
                "Weekly",
                "Monthly",
                "Every Other Week",
                "Twice Monthly",
                "Varied",
                "None",
        ]
        if occurrence in valid_occurrences:
            return occurrence
        return "None"

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
        if "Online" in groups_meet_type[index]:
            attributes.append("Online group")
        if group_childcare[index].lower() == "yes":
            attributes.append("Childcare Available")
        return attributes

    def _get_types(self, index, data_object):
        def remove_whitespace(val):
            return val.replace(" ", "") if "/" in val else val.strip()

        all_group_types = self._gen_data_list(data_object, Fields.GROUP_TYPES.value)
        group_types = all_group_types[index]
        formatted_group_types = []
        if "," in group_types:
            for group_type in group_types.split(","):
                formatted_group_types.append(remove_whitespace(group_type))
        else:
            formatted_group_types.append(remove_whitespace(group_types))
        return formatted_group_types

    def _get_age_range(self, index, data_object):
        all_age_ranges = self._gen_data_list(data_object, Fields.GROUP_AGE_RANGES.value)
        age_ranges = all_age_ranges[index]
        formatted_age_ranges = set()
        if "," in age_ranges:
            for age_range in age_ranges.split(","):
                formatted_age_ranges.add(age_range.strip())
        else:
            formatted_age_ranges.add(age_ranges.strip())
        if "All ages welcome" in formatted_age_ranges:
            formatted_age_ranges.update({
                "Under 18",
                "18-30",
                "31-55",
                "55+",
                "18 and up",
            })
        return list(formatted_age_ranges)

    def _get_genders(self, index, data_object):
        all_genders = self._gen_data_list(data_object, Fields.GROUP_GENDERS.value)
        genders = all_genders[index]
        formatted_genders = set()
        if "," in genders:
            for gender in genders.split(","):
                formatted_genders.add(gender.strip())
        else:
            formatted_genders.add(genders.strip())
        if "Co-ed (Men and Women welcome)" in formatted_genders:
            formatted_genders.update({
                "Men",
                "Women",
            })
        return list(formatted_genders)
