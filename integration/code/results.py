class Results:
    def __init__(self, crew, inventory):
        self.crew = crew
        self.inventory = inventory
        self.earnings = {}

    def record(self, winner, prize):
        self.earnings[winner] = self.earnings.get(winner, 0) + prize
        self.inventory.update_cash(prize)
        self.crew.add_xp(winner, 1) # 1 XP per win
