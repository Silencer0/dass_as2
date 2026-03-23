import pytest
import sys
import os

# Add 'code' directory to path for imports
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code"))

from registration import Registration
from crew_management import CrewManagement
from inventory import Inventory
from race import RaceManagement
from missions import MissionPlanning
from garage import Garage
from leaderboard import Leaderboard

@pytest.fixture
def setup_system():
    reg = Registration()
    inv = Inventory(1000)
    crew = CrewManagement(reg)
    racing = RaceManagement(crew)
    miss = MissionPlanning(crew)
    gar = Garage(inv)
    lb = Leaderboard(reg)
    return reg, inv, crew, racing, miss, gar, lb

# 1. Registration + Crew Details Integration
def test_register_and_get_details(setup_system):
    reg, _, crew, _, _, _, _ = setup_system
    reg.register("Dom", "Driver", 10)
    details = crew.get_member_details("Dom")
    assert details["name"] == "Dom"
    assert details["skill"] == 10

# 2. Skill Editing Integration
def test_edit_skill_updates_registry(setup_system):
    reg, _, crew, _, _, _, _ = setup_system
    reg.register("Dom", "Driver", 10)
    crew.edit_skill("Dom", 15)
    assert reg.get_skill("Dom") == 15

# 3. Role Changing Integration
def test_change_role_updates_registry(setup_system):
    reg, _, crew, _, _, _, _ = setup_system
    reg.register("Dom", "Driver", 10)
    crew.change_role("Dom", "Mechanic")
    assert reg.get_role("Dom") == "Mechanic"

# 4. Inventory Car Addition
def test_inventory_car_tracking(setup_system):
    _, inv, _, _, _, _, _ = setup_system
    inv.add_car("Charger")
    assert "Charger" in inv.cars

# 5. Race Winner Skill Increase
def test_race_updates_winner_skill(setup_system):
    reg, _, crew, racing, _, _, _ = setup_system
    reg.register("Dom", "Driver", 10)
    reg.register("Brian", "Driver", 10)
    racing.record_race("Dom", "Charger", "Brian", "Supra", "Dom")
    assert reg.get_skill("Dom") == 11

# 6. Multiple Races Skill Accumulation
def test_multiple_races_skill_accumulation(setup_system):
    reg, _, _, racing, _, _, _ = setup_system
    reg.register("Dom", "Driver", 10)
    reg.register("Brian", "Driver", 10)
    racing.record_race("Dom", "C1", "Brian", "C2", "Dom")
    racing.record_race("Dom", "C1", "Brian", "C2", "Dom")
    assert reg.get_skill("Dom") == 12

# 7. Driver (Role: Driver) -> Delivery Mission (Allowed)
def test_driver_delivery_mission_allowed(setup_system):
    reg, _, _, _, miss, _, _ = setup_system
    reg.register("Dom", "Driver", 5)
    assert miss.start_mission("Dom", "delivery") is True

# 8. Driver (Role: Driver) -> Rescue Mission (Blocked)
def test_driver_rescue_mission_blocked(setup_system):
    reg, _, _, _, miss, _, _ = setup_system
    reg.register("Dom", "Driver", 5)
    assert miss.start_mission("Dom", "rescue") is False

# 9. Mechanic (Role: Mechanic) -> Repair Mission (Allowed)
def test_mechanic_repair_mission_allowed(setup_system):
    reg, _, _, _, miss, _, _ = setup_system
    reg.register("Letty", "Mechanic", 5)
    assert miss.start_mission("Letty", "repair") is True

# 10. Strategist (Role: Strategist) -> Rescue Mission (Allowed)
def test_strategist_rescue_mission_allowed(setup_system):
    reg, _, _, _, miss, _, _ = setup_system
    reg.register("Tej", "Strategist", 5)
    assert miss.start_mission("Tej", "rescue") is True

# 11. Mission History Integration
def test_mission_history_log(setup_system):
    reg, _, _, _, miss, _, _ = setup_system
    reg.register("Dom", "Driver", 5)
    miss.start_mission("Dom", "delivery")
    log = miss.get_log()
    assert len(log) == 1
    assert log[0]["driver"] == "Dom"

# 12. Leaderboard Sorting (2 members)
def test_leaderboard_sorting(setup_system):
    reg, _, _, _, _, _, lb = setup_system
    reg.register("LowSkill", "Driver", 1)
    reg.register("HighSkill", "Driver", 100)
    ranking = lb.display()
    assert ranking[0][0] == "HighSkill"
    assert ranking[1][0] == "LowSkill"

# 13. Leaderboard Updates After Race
def test_leaderboard_updates_after_race(setup_system):
    reg, _, _, racing, _, _, lb = setup_system
    reg.register("Member1", "Driver", 10)
    reg.register("Member2", "Driver", 10)
    # Member 2 wins
    racing.record_race("Member1", "C1", "Member2", "C2", "Member2")
    ranking = lb.display()
    assert ranking[0][0] == "Member2"
    assert ranking[0][1] == 11

# 14. Garage Repair Resource Consumption (Tools)
def test_garage_consumes_tools(setup_system):
    _, inv, _, _, _, gar, _ = setup_system
    inv.add_car("Charger")
    inv.edit_tools(10)
    gar.record_repair("Charger", 5, 0, 0)
    assert inv.get_status()["tools"] == 5

# 15. Garage Repair Resource Consumption (Parts)
def test_garage_consumes_parts(setup_system):
    _, inv, _, _, _, gar, _ = setup_system
    inv.add_car("Charger")
    inv.edit_parts(10)
    gar.record_repair("Charger", 0, 3, 0)
    assert inv.get_status()["parts"] == 7

# 16. Garage Repair Resource Consumption (Cash)
def test_garage_consumes_cash(setup_system):
    _, inv, _, _, _, gar, _ = setup_system
    inv.add_car("Charger")
    inv.edit_cash(1000)
    gar.record_repair("Charger", 0, 0, 200)
    assert inv.get_status()["cash"] == 800

# 17. Garage Repair Insufficient Resources (Fail)
def test_garage_insufficient_resources(setup_system):
    _, inv, _, _, _, gar, _ = setup_system
    inv.add_car("Charger")
    inv.edit_cash(50)
    success = gar.record_repair("Charger", 0, 0, 100)
    assert success is False
    assert inv.get_status()["cash"] == 50

# 18. Garage Repair History Integration
def test_repair_history_log(setup_system):
    _, inv, _, _, _, gar, _ = setup_system
    inv.add_car("SuperCar")
    inv.edit_tools(10)
    inv.edit_parts(10)
    inv.edit_cash(1000)
    gar.record_repair("SuperCar", 1, 1, 1)
    history = gar.get_history()
    assert len(history) == 1
    assert history[0]["car"] == "SuperCar"

# 19. Inventory Status Integration
def test_inventory_full_status(setup_system):
    _, inv, _, _, _, _, _ = setup_system
    inv.edit_cash(100)
    inv.edit_parts(5)
    inv.edit_tools(2)
    inv.add_car("GTR")
    status = inv.get_status()
    assert status["cash"] == 100
    assert "GTR" in status["cars"]

# 20. Skill Level Bounds (No upper limit check)
def test_skill_level_no_limit(setup_system):
    reg, _, crew, _, _, _, _ = setup_system
    reg.register("Expert", "Driver", 999)
    crew.edit_skill("Expert", 1000)
    assert reg.get_skill("Expert") == 1000

# 21. Multi-step Workflow: Register -> Race -> Leaderboard
def test_workflow_register_race_leaderboard(setup_system):
    reg, _, _, racing, _, _, lb = setup_system
    reg.register("A", "Driver", 5)
    reg.register("B", "Driver", 5)
    racing.record_race("A", "C1", "B", "C2", "A") # A wins -> Skill 6
    ranking = lb.display()
    assert ranking[0] == ("A", 6)

# 23. Race with non-existent Driver (Should it crash or handle?)
def test_race_unregistered_driver(setup_system):
    reg, _, crew, racing, _, _, _ = setup_system
    reg.register("Dom", "Driver", 10)
    # If the system crashes here, Pytest will show it as a FAIL
    racing.record_race("Dom", "C1", "Ghost", "C2", "Ghost")

# 24. Negative Skill Level Injection
def test_negative_skill_injection(setup_system):
    reg, _, crew, _, _, _, _ = setup_system
    reg.register("Dom", "Driver", 10)
    crew.edit_skill("Dom", -100)
    # System should NOT allow negative skill level
    assert reg.get_skill("Dom") >= 0, "Security Failure: Negative skill allowed!"

# 25. Negative Inventory Balances
def test_negative_inventory_injection(setup_system):
    _, inv, _, _, _, _, _ = setup_system
    inv.edit_cash(-5000)
    # System should NOT allow negative cash balance
    assert inv.get_status()["cash"] >= 0, "Financial Failure: Negative cash allowed!"

# 26. Duplicate Registration Conflict
def test_duplicate_registration_logic(setup_system):
    reg, _, _, _, _, _, _ = setup_system
    reg.register("Dom", "Driver", 10)
    result = reg.register("Dom", "Mechanic", 50)
    assert result is False, "Integrity Failure: Duplicate registration overwrite allowed!"
    assert reg.get_role("Dom") == "Driver"
    assert reg.get_skill("Dom") == 10

# 27. Mission For Non-Existent Member
def test_mission_non_existent_member(setup_system):
    _, _, _, _, miss, _, _ = setup_system
    assert miss.start_mission("NoOne", "delivery") is False

# 28. Repair with Non-Existent Car
def test_repair_non_existent_car(setup_system):
    _, inv, _, _, _, gar, _ = setup_system
    inv.edit_cash(1000)
    inv.edit_tools(10)
    # System should REFUSE repairs for non-existent cars
    result = gar.record_repair("ImaginaryCar", 1, 0, 100)
    assert result is False, "Integrity Failure: Repair logged for non-existent vehicle!"

# 29. Empty Name Registration
def test_empty_name_registration(setup_system):
    reg, _, _, _, _, _, _ = setup_system
    assert reg.register("", "Driver", 10) is False

# 30. Leaderboard with Zero Members
def test_leaderboard_empty(setup_system):
    _, _, _, _, _, _, lb = setup_system
    assert lb.display() == []

# 31. Race with Shared Car Reference (Mutations)
def test_car_data_mutation_isolation(setup_system):
    _, inv, _, _, _, _, _ = setup_system
    inv.add_car("Charger")
    status = inv.get_status()
    # If the system is secure, mutating the report should NOT leak into the fleet
    status["cars"].append("LeakedCar")
    assert "LeakedCar" not in inv.cars, "Memory Leak: Internal state modified via status report!"

# 32. Missions - Case Sensitivity Robustness
def test_role_case_sensitivity(setup_system):
    reg, _, _, _, miss, _, _ = setup_system
    reg.register("Lower", "driver", 10)
    # If the system is robust, it should handle casing (Driver == driver)
    assert miss.start_mission("Lower", "delivery") is True, "Logic Failure: Mission rejected due to case sensitivity!"
