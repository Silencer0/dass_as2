from registration import Registration
from crew_management import CrewManagement
from inventory import Inventory
from race import RaceManagement
from missions import MissionPlanning
from leaderboard import Leaderboard
from garage import Garage

def get_choice(options, prompt):
    for i, opt in enumerate(options):
        print(f"  {i+1}. {opt}")
    while True:
        try:
            val = int(input(prompt))
            if 1 <= val <= len(options): return options[val-1]
        except ValueError: pass
        print("Invalid choice.")

def main():
    print("\n--- STREETRACE MANAGEER---")
    reg, inv = Registration(), Inventory(0)
    crew = CrewManagement(reg)
    racing, miss, lb, gar = RaceManagement(crew), MissionPlanning(crew), Leaderboard(reg), Garage(inv)
    
    while True:
        m = ["Registration", "Crew Management", "Inventory", "Race", "Missions", "Leaderboard", "Repairs", "Exit"]
        cmd = get_choice(m, "\nAction: ")
        if cmd == "Exit": break
        
        if cmd == "Registration":
            name = input("Name: ")
            role = get_choice(["Driver", "Mechanic", "Strategist"], "Role: ")
            skill = int(input("Initial Skill Level: "))
            reg.register(name, role, skill)
            
        elif cmd == "Crew Management":
            mem = reg.get_members()
            if not mem:
                print("No members found.")
                continue
            while True:
                scmd = get_choice(["Driver Details", "Edit Skill Level", "Change Role", "Back"], "\nCrew Action: ")
                if scmd == "Back": break
                name = get_choice(mem, "Member: ")
                if scmd == "Driver Details": print(crew.get_member_details(name))
                elif scmd == "Edit Skill Level":
                    reg.set_skill(name, int(input("New Skill Level: ")))
                elif scmd == "Change Role":
                    reg.set_role(name, get_choice(["Driver", "Mechanic", "Strategist"], "New Role: "))

        elif cmd == "Inventory":
            while True:
                ic = ["Add Car", "Edit Cash", "Edit Parts Count", "Edit Tools Count", "View Status", "Back"]
                scmd = get_choice(ic, "\nInventory Action: ")
                if scmd == "Back": break
                if scmd == "Add Car": inv.add_car(input("Car Name: "))
                elif scmd == "Edit Cash": inv.edit_cash(int(input("New Cash Balance: ")))
                elif scmd == "Edit Parts Count": inv.edit_parts(int(input("New Parts Count: ")))
                elif scmd == "Edit Tools Count": inv.edit_tools(int(input("New Tools Count: ")))
                elif scmd == "View Status": print(inv.get_status())

        elif cmd == "Race":
            mem, cars = reg.get_members(), inv.cars
            if len(mem) >= 2 and len(cars) >= 1:
                d1 = get_choice(mem, "Driver 1: ")
                c1 = get_choice(cars, "Car 1: ")
                d2 = get_choice([m for m in mem if m != d1], "Driver 2: ")
                c2 = get_choice(cars, "Car 2: ")
                winner = get_choice([d1, d2], "Winner (1 or 2): ")
                racing.record_race(d1, c1, d2, c2, winner)
                print(f"Result recorded. {winner}'s skill level has increased.")
            else: print("Need at least 2 members and 1 car (available to both).")

        elif cmd == "Missions":
            while True:
                scmd = get_choice(["Log New Mission", "View Mission History", "Back"], "\nMission Action: ")
                if scmd == "Back": break
                if scmd == "Log New Mission":
                    name = get_choice(reg.get_members(), "Who: ")
                    m_type = get_choice(["rescue", "delivery", "repair"], "Mission Type: ")
                    if miss.start_mission(name, m_type): print("Mission logged successfully.")
                    else: print("Role mismatch! Operation aborted.")
                elif scmd == "View Mission History":
                    for entry in miss.get_log(): print(entry)

        elif cmd == "Leaderboard":
            print("\nRANKINGS (Member, Skill Level):")
            for entry in lb.display(): print(entry)

        elif cmd == "Repairs":
            while True:
                scmd = get_choice(["Record New Repair", "View Repair History", "Back"], "\nRepair Action: ")
                if scmd == "Back": break
                if scmd == "Record New Repair":
                    if not inv.cars:
                        print("No cars available.")
                        continue
                    car = get_choice(inv.cars, "Car: ")
                    t = int(input("Tools to use: "))
                    p = int(input("Parts to use: "))
                    c = int(input("Cash to use: "))
                    if gar.record_repair(car, t, p, c): print("Repair recorded and inventory updated.")
                    else: print("Insufficient resources!")
                elif scmd == "View Repair History":
                    for entry in gar.get_history(): print(entry)

if __name__ == "__main__":
    main()
