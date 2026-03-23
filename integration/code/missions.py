class MissionPlanning:
    def __init__(self, crew):
        self.crew = crew
        self.log = []

    def start_mission(self, name, mission_type):
        role = self.crew.registration.get_role(name)
        # Strict role rules
        allowed = (mission_type == "delivery" and role == "Driver") or \
                  (mission_type == "repair" and role == "Mechanic") or \
                  (mission_type == "rescue" and role == "Strategist")
        if allowed:
            self.log.append({"driver": name, "mission": mission_type})
            return True
        return False

    def get_log(self):
        return self.log
