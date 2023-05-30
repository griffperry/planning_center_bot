import pandas as pd
from datetime import datetime


class DataGenerator():
    def __init__(self):
        self.data = {}
        self.num_groups = 0

    def verify_data(self, data_file):
        file_object = pd.read_excel(data_file)
        file_object = file_object.fillna('')
        self.data = self.translate_data(file_object)
        return True

    def translate_data(self, data_object):
        groups = {}
        leader_emails = self._gen_data_list(data_object, "Unnamed: 3")
        group_descriptions = self._gen_data_list(data_object, "Unnamed: 16")
        group_names = self._gen_data_list(data_object, "Unnamed: 15")
        self.num_groups = len(group_names)

        for index in range(self.num_groups):
            groups[index] = {}
        for index, name in enumerate(group_names):
            groups[index]["name"] = name
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
        return groups

    def _gen_data_list(self, data_object, column):
        return data_object[column].to_list()[1:]

    def _gen_members_data(self, index, groups, data_object):
        leader_first_names = self._gen_data_list(data_object, "Unnamed: 1")
        leader_last_names = self._gen_data_list(data_object, "Unnamed: 2")
        leader_emails = self._gen_data_list(data_object, "Unnamed: 3")
        co_leader_names = self._gen_data_list(data_object, "Unnamed: 11")
        co_leader_emails = self._gen_data_list(data_object, "Unnamed: 12")
        groups[index]["members"] = {
            0: {
                "name": f"{leader_first_names[index]} {leader_last_names[index]}",
                "status": "leader",
                "email": f"{leader_emails[index]}" if leader_emails[index] else None,
            },
            1: {
                "name": f"{co_leader_names[index]}",
                "status": "co-leader",
                "email": f"{co_leader_emails[index]}" if co_leader_emails[index] else None,
            }
        }

    def _gen_schedule_data(self, index, groups, data_object):
        group_occurences = self._gen_data_list(data_object, "Unnamed: 21")
        group_days = self._gen_data_list(data_object, "Unnamed: 22")
        group_times = self._gen_data_list(data_object, "Unnamed: 23")
        groups[index]["schedule"] = f"{group_days[index]} @ {group_times[index]} {group_occurences[index]}"

    def _gen_address_data(self, index, groups, data_object):
        groups_meet_type = self._gen_data_list(data_object, "Unnamed: 19")
        groups_out_home_address = self._gen_data_list(data_object, "Unnamed: 20")
        leader_addresses = self._gen_data_list(data_object, "Unnamed: 7")
        if groups_meet_type[index] == "In Home":
            groups[index]["address"] = leader_addresses[index].strip("Home:/\n")
        elif groups_meet_type[index] != "Online":
            groups[index]["address"] = groups_out_home_address[index]
        else:
            groups[index]["address"] = None

    def _gen_tags_data(self, index, groups, data_object):
        group_campuses = self._gen_data_list(data_object, "Unnamed: 8")
        group_occurences = self._gen_data_list(data_object, "Unnamed: 21")
        group_days = self._gen_data_list(data_object, "Unnamed: 22")
        group_genders = self._gen_data_list(data_object, "Unnamed: 18")
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
        groups_meet_type = self._gen_data_list(data_object, "Unnamed: 19")
        group_childcare = self._gen_data_list(data_object, "Unnamed: 25")
        if groups_meet_type[index] == "Online":
            attributes.append("Online group")
        if group_childcare[index]:
            attributes.append("Childcare Available")
        return attributes

    def _get_types(self, index, data_object):
        all_group_types = self._gen_data_list(data_object, "Unnamed: 24")
        group_types = all_group_types[index]
        if "," in group_types:
            return group_types.replace(" ", "").split(",")
        return [group_types]

    def _get_age_range(self, index, data_object):
        all_age_ranges = self._gen_data_list(data_object, "Unnamed: 17")
        age_range = all_age_ranges[index]
        if "," in age_range:
            return age_range.replace(" ", "").split(",")
        return [age_range]
