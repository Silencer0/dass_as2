class Garage:
    def __init__(self, inventory):
        self.inventory = inventory
        self.history = []

    def record_repair(self, car_name, tools, parts, cash):
        if car_name in self.inventory.cars and \
           self.inventory.tools_count >= tools and \
           self.inventory.parts_count >= parts and \
           self.inventory.cash >= cash:
            
            self.inventory.edit_tools(self.inventory.tools_count - tools)
            self.inventory.edit_parts(self.inventory.parts_count - parts)
            self.inventory.edit_cash(self.inventory.cash - cash)
            
            self.history.append({
                "car": car_name,
                "tools": tools,
                "parts": parts,
                "cash": cash
            })
            return True
        return False

    def get_history(self):
        return self.history
