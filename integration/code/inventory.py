class Inventory:
    def __init__(self, cash=0):
        self.cash = cash
        self.cars = []
        self.parts_count = 0
        self.tools_count = 0

    def edit_cash(self, val): self.cash = max(0, val)
    def edit_parts(self, val): self.parts_count = max(0, val)
    def edit_tools(self, val): self.tools_count = max(0, val)
    def add_car(self, name): self.cars.append(name)

    def get_status(self):
        return {
            "cash": self.cash,
            "cars": self.cars,
            "parts": self.parts_count,
            "tools": self.tools_count
        }
