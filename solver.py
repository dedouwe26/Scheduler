class Solver:
	activities: int
	participants: list[list[int]]
	maxSpots: int
	def __init__(self, activities: list[str], participants: dict[str, list[str]], maxSpots: int) -> None:
		self.activities = len(activities)
		self.participants = [[activities.index(choice) for choice in participants[name]] for name in participants]
		self.maxSpots = maxSpots
		self.solution = [i[0] for i in self.participants]
	
	def solve(self) -> list[int]:
		while self.is_not_solved():
			# Search the highest lowering score.
			max_score = None
			index = -1
			for i in range(len(self.participants)):
				score = self.rate_lowering(i)
				if max_score == None or score > max_score:
					max_score = score
					index = i
			
			# Lower that one.
			self.lower_choice(index)

		return self.solution

	occupancy: list[int]
	solution: list[int]
	def is_not_solved(self):
		# Check if the current solution is valid.
		self.occupancy = [0 for i in range(self.activities)]
		isValidSolution = True
		for choice in self.solution:
			if self.occupancy[choice] >= self.maxSpots:
				isValidSolution = False
			self.occupancy[choice] += 1
		
		return not isValidSolution

	def rate_lowering(self, index) -> int:
		currentChoice = self.solution[index]
		choices = self.participants[index]
		try:
			currentChoiceIndex = choices.index(currentChoice)
		except:
			currentChoiceIndex = -1
		# Calculate base score.
		# Lowering one to 2nd scores higher than lowering one to 3rd.
		if currentChoiceIndex != -1:
			score = len(choices) - currentChoiceIndex
		else: # Is already beyond choices.
			score = 1 # NOTE: Perhaps this needs to be balanced.

		# Add some points if the current choice is one with a lot of occupancy.
		if self.occupancy[currentChoice] > self.maxSpots:
			score += 1 # NOTE: Perhaps this needs to be balanced.
		if currentChoiceIndex+1 < len(choices) and self.occupancy[choices[currentChoiceIndex+1]] >= self.maxSpots:
			score -= 1 # NOTE: Perhaps this needs to be balanced.

		return score
	def lower_choice(self, index):
		"""
		Lowers the choice for 1 participant at the specified index.
		"""
		choices = self.participants[index]
		# Lowering beyond its choices.
		if self.solution[index]+1 >= len(choices):
			# Chooses an activity the participant did not have on his list. Change this if you want.
			# Currently chooses the least busy activity.
			self.solution[index] = self.occupancy.index(min(self.occupancy))
			return
		self.solution[index] = choices[self.solution[index]+1]
