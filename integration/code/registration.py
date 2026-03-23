class Registration:
    def __init__(self):
        self.members = {}

    def register(self, name, role, skill):
        if name and name not in self.members:
            self.members[name] = {"role": role, "skill": skill}
            return True
        return False

    def get_role(self, name):
        return self.members.get(name, {}).get("role")

    def set_role(self, name, role):
        if name in self.members:
            self.members[name]["role"] = role
            return True
        return False

    def get_skill(self, name):
        return self.members.get(name, {}).get("skill")

    def set_skill(self, name, skill):
        if name in self.members:
            self.members[name]["skill"] = skill
            return True
        return False

    def get_members(self):
        return list(self.members.keys())

    def is_registered(self, name):
        return name and name in self.members
