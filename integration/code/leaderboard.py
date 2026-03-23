class Leaderboard:
    def __init__(self, registration):
        self.registration = registration

    def display(self):
        members = self.registration.get_members()
        data = [(m, self.registration.get_skill(m)) for m in members]
        return sorted(data, key=lambda x: x[1], reverse=True)
