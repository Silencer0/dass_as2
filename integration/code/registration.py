class Registration:
    def __init__(self):
        self.members = {}

    def register(self, name, role):
        self.members[name] = role

    def get_members(self):
        return list(self.members.keys())

    def is_registered(self, name):
        return name in self.members
