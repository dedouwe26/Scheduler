import math

class Solver:
	activities: list[str]
	participants: dict[str, list[str]]
	maxParticipants: int
	def __init__(self, activities: list[str], participants: dict[str, list[str]]) -> None:
		self.activities = activities
		self.participants = participants
		self.maxParticipants = math.ceil(len(participants) / len(activities))
		self.solution = [0 for i in range(len(participants))]
	
	def solve(self) -> dict[str, list[str]] | None:
		self.descend()

		schedule = {a: [] for a in self.activities}
		for participantIndex in range(len(self.solution)):
			name = list(self.participants)[participantIndex]
			participant = self.participants[name]
			activity = participant[self.solution[participantIndex]]
			schedule[activity].append(name)
		return schedule

	activityCount: list[int]
	solution: list[int]
	def descend(self):
		self.activityCount = [0 for i in range(len(self.activities))]
		isValidSolution = True
		for choice in self.solution:
			if self.activityCount[choice] >= self.maxParticipants:
				isValidSolution = False
				break
			self.activityCount[choice] += 1
		
		if isValidSolution:
			return

		max_score = -1
		index = -1
		for i in range(len(self.participants)):
			score = self.rate_lowering(i)
			if score > max_score:
				max_score = score
				index = i
		
		self.lower_choice(index)

		self.descend()

	def rate_lowering(self, index) -> int:
		# TODO: Count in maxparticipants and current activity count.
		choices = self.participants[list(self.participants)[index]]
		return len(choices) - self.solution[index]
	def lower_choice(self, index):
		"""
		Lowers the choice for 1 participant at the specified index.
		"""
		self.solution[index] += 1
		choices = self.participants[list(self.participants)[index]]
		if self.solution[index] >= len(choices):
			# TODO: Choose an activity not on choice list.
			pass