import math

class Solver:
	activities: list[str]
	participants: dict[str, list[str]]
	maxParticipants: int
	def __init__(self, activities: list[str], participants: dict[str, list[str]]) -> None:
		self.activities = activities
		self.participants = participants
		self.maxParticipants = math.ceil(len(participants) / len(activities))
		self.activityCount = [0 for i in range(len(activities))]
	
	def solve(self) -> dict[str, list[str]] | None:
		if not self.descend():
			return None
		schedule = {a: [] for a in self.activities}
		for participantIndex in range(len(self.solutionPath)):
			name = list(self.participants)[participantIndex]
			participant = self.participants[name]
			activity = participant[self.solutionPath[participantIndex]]
			schedule[activity].append(name)
		return schedule
			
	activityCount: list[int]
	solutionPath: list[int] = []
	def descend(self) -> bool:
		"""
		Descends in the solution path.
		Returns true if it has found a valid path, otherwise false.
		"""
		currentIndex = len(self.solutionPath)
		if currentIndex == len(self.participants):
			return True

		currentParticpant = self.participants[list(self.participants)[currentIndex]]
		for choice in range(len(currentParticpant)):
			activity = currentParticpant[choice]
			activityIndex = self.activities.index(activity)
			if self.activityCount[activityIndex]+1 > self.maxParticipants:
				continue
			self.activityCount[activityIndex] += 1
			self.solutionPath.append(choice)
			if not self.descend():
				self.activityCount[activityIndex] -= 1
				self.solutionPath.pop()
				continue
			return True

		return False