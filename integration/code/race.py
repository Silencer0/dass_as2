class RaceManagement:
    def __init__(self, crew):
        self.crew = crew

    def record_race(self, d1, c1, d2, c2, winner_name):
        curr_skill = self.crew.registration.get_skill(winner_name)
        if curr_skill is not None:
            self.crew.registration.set_skill(winner_name, curr_skill + 1)
        return winner_name
