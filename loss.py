import numpy as np

class losses():
	def __init__(self):
		self.pupil_ideal_left = (230, 230)
		self.pupil_ideal_right = (310, 230)
		self.iris_ideal_left = (0.5, 0.5)
		self.iris_ideal_right = (0.5, 0.5)

	def mse(self, x, y):
		return (x**2 - y**2)**(1/2)

	def pupil_error(self, pupil_co, left = 1):
		if left:
			return mse(np.abs(pupil_co.x-self.pupil_ideal_left.x), 
				np.abs(pupil_co.y-self.pupil_ideal_left.y))

		return mse(np.abs(pupil_co.x-self.pupil_ideal_right.x), 
				np.abs(pupil_co.y-self.pupil_ideal_right.y))


	def iris_error(self, iris_co, left = 1):
		if left:
			return mse(np.abs(iris_co.x-self.iris_ideal_left.x),
				np.abs(iris_co.y-self.iris_ideal_left.y))

		return mse(np.abs(iris_co.x-self.iris_ideal_right.x),
				np.abs(iris_co.y-self.iris_ideal_right.y))
