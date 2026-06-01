# class Modification:
# 	participant: int
# 	previous_choice: int
# 	next_choice: int
# 	previous_iteration: int
# 	def __init__(self, participant, previous_choice, next_choice, previous_iteration) -> None:
# 		self.participant = participant
# 		self.previous_choice = previous_choice
# 		self.next_choice = next_choice
# 		self.previous_iteration = previous_iteration
# 	def revert(self, solution) -> int:
# 		solution[self.participant] = self.previous_choice
# 		return self.previous_iteration

class State:
	state: list[int] # The current scheduled activity per participant.
	occupancy: list[int] # The occupancy per activity.

	def __init__(self, state) -> None:
		self.state = state
		self.occupancy = []

class Solver:
	activities: int # Amount of activities.
	participants: list[list[int]] # The participants with their choice list.
	max_spots: int # The max spots per activity.
	max_branches: int
	def __init__(self, activities: list[str], participants: dict[str, list[str]], max_spots: int, max_branches: int = 2) -> None:
		self.activities = len(activities)
		self.participants = [[activities.index(choice) for choice in participants[name]] for name in participants]
		self.max_spots = max_spots
		self.max_branches = max_branches
		# self.state() = [i[0] for i in self.participants]
		self.queue.append(State(
			[i[0] for i in self.participants],

		))
	
	# solution: list[int]
	# occupancy: list[int]
	# modifications: list[Modification] = [] # Represents depth.
	# iteration: int = 0 # Represents breadth.

	# # breadth control
	# def breadth_next(self):
	# 	self.iteration += 1
	# def breadth_reset(self):
	# 	self.iteration = 0

	# # Depth control
	# def ascend(self):
	# 	self.iteration = self.modifications.pop().revert(self.state()) + 1

	# def descend(self, participant: int, next_choice: int):
	# 	mod = Modification(participant, self.state()[participant], next_choice, self.iteration)
	# 	self.state()[participant] = mod.next_choice
	# 	self.iteration = 0
	# 	self.modifications.append(mod)

	queue: list[State] = []

	def state(self) -> list[int]: return self.queue[0].state
	def occupancy(self) -> list[int]: return self.queue[0].occupancy

	def solve(self) -> list[int] | None:
		# Descend most prominent solutions, depth-first like a tree.
		while self.is_not_solved():
			# Search the highest scores.
			scores = [self.rate_lowering(i) for i in range(len(self.participants))]
			max_score = max(scores)

			if max_score == -1:
				self.queue.pop(0)
				continue
			
			count = 0
			for i in range(len(scores)):
				if scores[i] == max_score:
					count += 1
					self.lower_choice(i)
					if count == self.max_branches:
						break

			self.queue.pop(0)

		if len(self.queue) > 0:
			# Ladies and gentlemen, we got him.
			return self.state()
		else: return None # :(

	def is_not_solved(self) -> bool:
		if len(self.queue) == 0:
			return False
		# Check if the current solution is valid and generate occupancies.
		self.queue[0].occupancy = [0 for _ in range(self.activities)]
		is_invalid = False
		for choice in self.state():
			if self.occupancy()[choice] >= self.max_spots:
				is_invalid = True
			self.occupancy()[choice] += 1

		return is_invalid

	# Choice rating and lowering.
	def get_choice_index(self, index):
		current_choice = self.state()[index]
		choices: list[int] = self.participants[index]
		if current_choice in choices:
			return choices.index(current_choice)
		else: return -1

	def rate_lowering(self, index) -> float:
		choices = self.participants[index]
		current_choice_index = self.get_choice_index(index)
		current_choice = self.state()[index]

		# Lowering one to 2nd scores higher than lowering one to 3rd.
		if 0 >= current_choice_index+1 or current_choice_index+1 >= len(choices):
			score = -1 # NOTE: Perhaps this needs to be balanced
		else:
			score =  (1 / (current_choice_index+1)) * len(choices) * 5

		# Add some points if the current choice is one with a high occupancy.
		if self.occupancy()[current_choice] > self.max_spots:
			score += 1 # NOTE: Perhaps this needs to be balanced.
		
		next_choice = self.get_lowered_choice(index, current_choice_index)

		# Remove some points if the next choice is one with a high occupancy.
		if self.occupancy()[next_choice] >= self.max_spots:
			score -= 1 # NOTE: Perhaps this needs to be balanced.
		
		return score

	def get_lowered_choice(self, index, current_choice_index):
		choices = self.participants[index]
		# Lowering beyond its choices.
		if 0 >= current_choice_index+1 or current_choice_index+1 >= len(choices):
			# Chooses an activity the participant did not have on his list. Change this if you want.
			# Currently chooses the least busy activity.
			raise Exception("not supported")
			# nextChoice = self.occupancy().index(min(self.occupancy()))
			# return nextChoice
		next_choice = choices[current_choice_index+1]
		return next_choice

	def lower_choice(self, index):
		"""
		Lowers the choice for 1 participant at the specified index.
		"""
		new_state = self.state().copy()
		new_state[index] = self.get_lowered_choice(index, self.get_choice_index(index))
		self.queue.append(State(
			new_state
		))