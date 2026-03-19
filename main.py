import sys
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
	# TODO: Solve.
	solver = Solver(activities, participants)
	schedule = solver.solve()

	if schedule == None:
		print("! No solution found.")
		exit(1)
	
	print("! Found a solution:")
	for act, part in schedule:
		print(f"{act}: ")
		for p in part:
			print(f"{p}", end=",")
	pass

if __name__ == "__main__":
	print(sys.argv)
	if True:
		activities = ask_for_activities()
		main(activities, ask_for_participants(activities))
	else:
		# TODO: Sample data.
		pass