import math
import main
import solver
import sample as sample

if __name__ == "__main__":
	recommendedCount = math.ceil(len(sample.participants) / len(sample.activities))
	solver = solver.Solver(sample.activities, sample.participants, recommendedCount)
	main.present_result(solver.solve(), sample.participants, sample.activities)