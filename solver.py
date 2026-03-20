class Solver:
	activities: int
	participants: list[list[int]]
	maxSpots: int
	def __init__(self, activities: list[str], participants: dict[str, list[str]], maxSpots: int) -> None:
		self.activities = len(activities)
		self.participants = [[activities.index(choice) for choice in participants[name]] for name in participants]
		self.maxSpots = maxSpots
		self.solution = [0 for i in range(len(participants))]
	
	def solve(self) -> list[int]:
		self.descend()
		return self.solution

	occupancy: list[int]
	solution: list[int]
	def descend(self):
		# Check if the current solution is valid.
		self.occupancy = [0 for i in range(self.activities)]
		isValidSolution = True
		for choice in self.solution:
			if self.occupancy[choice] >= self.maxSpots:
				isValidSolution = False
				break
			self.occupancy[choice] += 1
		
		if isValidSolution:
			return

		# Search the highest lowering score.
		max_score = -1
		index = -1
		for i in range(len(self.participants)):
			score = self.rate_lowering(i)
			if score > max_score:
				max_score = score
				index = i
		
		# Lower that one.
		self.lower_choice(index)

		# Recurse and check for valid solution.
		self.descend()

	def rate_lowering(self, index) -> int:
		currentChoice =  self.solution[index]
		choices = self.participants[index]
		# Calculate base score.
		# Lowering one to 2nd scores higher than lowering one to 3rd.
		score = len(choices) - currentChoice

		# Add some points if the next choice is one with a lot of occupancy.
		try:
			if self.occupancy[choices[currentChoice+1]] >= self.maxSpots:
				score += 1 # NOTE: Perhaps this still needs to be balanced.
		except:
			pass
		return score
	def lower_choice(self, index):
		"""
		Lowers the choice for 1 participant at the specified index.
		"""
		self.solution[index] += 1

		choices = self.participants[list(self.participants)[index]]
		# Lowering beyond its choices.
		if self.solution[index] >= len(choices):
			# Chooses an activity the participant did not have on his list. Change this if you want.
			# Currently chooses the least busy activity.
			self.solution[index] = self.occupancy.index(min(self.occupancy))
			return