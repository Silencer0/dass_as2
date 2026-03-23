class MissionPlanning:
    def __init__(self, crew):
        self.crew = crew
        self.log = []

    def start_mission(self, name, mission_type):
        raw_role = self.crew.registration.get_role(name)
        if not raw_role: return False
        
        role = raw_role.lower()
        m_type = mission_type.lower()
        
        # Strict role rules (case-insensitive)
        allowed = (m_type == "delivery" and role == "driver") or \
                  (m_type == "repair" and role == "mechanic") or \
                  (m_type == "rescue" and role == "strategist")
        
        if allowed:
            self.log.append({"driver": name, "mission": mission_type})
            return True
        return False

    def get_log(self):
        return self.log
