class StatusReport():

    def __init__(self):
        self.group_status = {}
        self.group_caveats = {}

    def add_group_status(self, group_name, group_status):
        self.group_status[group_name] = group_status

    def add_group_caveat(self, group_name, caveat):
        if group_name in self.group_caveats:
            self.group_caveats[group_name].append(caveat)
        else:
            self.group_caveats[group_name] = [caveat]

    def create_report(self, group_name):
        report = [self.group_status.get(group_name)]
        for caveat in self.group_caveats.get(group_name):
            report.append(caveat)
        report.append("\n")
        return "\n".join(report)
