class CrewManagement:
    def __init__(self, registration):
        self.registration = registration

    def edit_skill(self, name, new_val):
        return self.registration.set_skill(name, new_val)

    def change_role(self, name, role):
        return self.registration.set_role(name, role)

    def get_member_details(self, name):
        if self.registration.is_registered(name):
            return {
                "name": name,
                "role": self.registration.get_role(name),
                "skill": self.registration.get_skill(name)
            }
        return None
