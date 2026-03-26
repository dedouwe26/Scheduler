from solver import Solver

def ask_for_participants(activities) -> dict[str, list[str]]:
	def ask_for_choice(i, choices) -> str:
		choice = input(f"\t{i+1}e choice: ")
		if not (choice in activities):
			print(f"\tNo such activity {choice}...")
			return ask_for_choice(i, choices)
		elif choice in choices:
			print(f"\tCannot choose an activity multiple times...")
			return ask_for_choice(i, choices)

		return choice

	count = int(input("Amount of participants: "))
	choices_count = int(input("Amount of choices: "))
	
	participants = {}
	for i in range(count):
		name = input(f"{i+1}e participant's name: ")

		choices = []
		for j in range(choices_count):
			choices.append(ask_for_choice(j, choices))

		participants[name] = choices
	
	return participants

def ask_for_activities() -> list[str]:
	count = int(input("Amount of activities: "))
	activities = []
	for i in range(count):
		activities.append(input(f"{i+1}e activity's name: "))
	return activities

def main(activities: list[str], participants: dict[str, list[str]]):
	spots = int(input("Amount of spots per activity: "))
	if spots*len(activities) < len(participants):
		print("! Not enough spots for everyone.")
		exit(1)

	solver = Solver(activities, participants, spots)
	solution = solver.solve()

	if solution == None:
		print("! No solution found.")
		exit(1)
	
	schedule = {activity: [] for activity in activities}
	for i in range(len(solution)):
		name = list(participants)[i]
		choice = solution[i]
		schedule[list(schedule)[choice]].append(name)

	print("! Found a solution:")
	for activity in schedule:
		print(f"{activity}: ", end="")
		for p in schedule[activity]:
			print(f"{p}", end=", ")
		print()

if __name__ == "__main__":
	activities = ask_for_activities()
	main(activities, ask_for_participants(activities))