from planning_center_backend import planning_center
from planning_center_backend.people import PeopleQueryExpression
from planning_center_backend import maps
from src.status_report import StatusReport

class GroupManager(StatusReport):

    def __init__(self, email, password, id):
        self.id = id
        self.maps_api_key = None
        self.reports = []
        self.group_status = {}
        self.group_caveats = {}
        self.backend = planning_center.PlanningCenterBackend()
        self.backend.login(email, password)
        super().__init__()

    def delete_group(self, group):
        group_deleted = False
        group_name = group["name"]
        self.group_status[group_name] = None
        self.group_caveats[group_name] = []
        groups = self.backend.groups.query(group_name)
        if groups:
            groups[0].delete()
            group_deleted = True
            self.add_group_status(group_name, f"(User {self.id}) Group '{group_name}' deleted.")
        else:
            self.add_group_status(group_name, f"(User {self.id}) Group '{group_name}' doesn't exist.")
        self.reports.append(self.create_report(group_name))
        return group_deleted

    def create_group(self, group):
        group_name = group["name"]
        self.group_status[group_name] = None
        self.group_caveats[group_name] = []
        success = self.add_group(group)
        if success:
            for member in group["members"].values():
                self.add_member_to_group(group_name, member)
            self.add_group_settings(group)
            self.add_group_status(
                group_name,
                f"(User {self.id}) Group '{group_name}' created."
            )
        self.reports.append(self.create_report(group_name))

    def add_group(self, group):
        group_name = group["name"]
        if not self.backend.groups._check_exists(group_name):
            self.current_group = self.backend.groups.create(group_name)
        else:
            self.add_group_status(
                group_name,
                f"(User {self.id}) Group '{group_name}' already exists."
            )
            self.current_group = self.backend.groups.query(group_name)[0]
        if self.backend.groups._check_exists(group_name):
            return True
        return False

    def add_member_to_group(self, group_name, member):
        member_name = member.get("name")
        member_status = member.get("status")
        member_email = member.get("email")
        promote_member = "leader" in member_status
        qe = PeopleQueryExpression(search_name=member_name, search_name_or_email=member_email)
        if qe:
            person_obj = self.backend.people.query(qe)
            if len(person_obj) == 1:
                self.current_group.add_member(person_id=person_obj[0].id, leader=promote_member)
            else:
                self.add_group_caveat(
                    group_name,
                    f"(User {self.id}) {member_name} not found when added to '{group_name}'."
                )

    def add_group_settings(self, group):
        with self.current_group.no_refresh():
            self.add_meeting_schedule(group.get("schedule"))
            self.add_description(group.get("description"))
            self.add_group_contact_email(group.get("contact_email"))
            self.add_group_tags(group.get("tags"))
            self.add_group_location(group.get("name"), group.get("address"))

    def add_meeting_schedule(self, schedule):
        if schedule:
            self.current_group.schedule = schedule

    def add_description(self, description):
        if description:
            self.current_group.description = description

    def add_group_contact_email(self, email):
        if email:
            self.current_group.contact_email = email

    def add_group_location(self, group_name, address):
        if group_name and address:
            maps_api = maps.Maps(self.maps_api_key)
            try:
                location = maps_api.find_place_from_text(address)
                assert len(location) == 1
                geocodes = maps_api.geocode_from_place_id(location[0].place_id)
                assert len(geocodes) == 1
                group_location = self.current_group.locations.create(
                    f"{group_name} location",
                    geocodes[0],
                    shared=False
                )
                self.current_group.location_id = group_location
            except:
                self.add_group_caveat(
                    group_name,
                    f"(User {self.id}) Failed to add location in group '{group_name}'"
                )

    def add_group_tags(self, tags):
        if tags:
            tag_list = self.gen_simple_tag_list(tags)
            for tag in tag_list:
                try:
                    self.current_group.add_tag(tag)
                except:
                    tag_data = self.backend.groups.tags.query(tag)
                    for tag_element in tag_data:
                        if tag_element.attributes.name == tag:
                            self.current_group.add_tag(tag_element)
                            break

    def gen_simple_tag_list(self, tags):
        tag_list = []
        for tag in tags.values():
            if isinstance(tag, str):
                tag_list.append(tag)
            if isinstance(tag, list):
                for i in tag:
                    tag_list.append(i)
        return tag_list
