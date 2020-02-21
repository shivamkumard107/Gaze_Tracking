import numpy as np

class losses():
	def __init__(self):
		self.A = 0.5
		self.B = 0.5
		self.pupil_ideal_left = (310/750, 170/375)
		self.pupil_ideal_right = (420/750, 170/375)
		self.iris_ideal_left = (0.5, 0.5)
		self.iris_ideal_right = (0.5, 0.5)

	def mse(self, x, y):
		return (x**2 + y**2)**(1/2)

	def pupil_error(self, pupil_co, left = 1):
		if left:
			return self.mse(np.abs(pupil_co[0]/750-self.pupil_ideal_left[0]), 
				np.abs(pupil_co[1]/375-self.pupil_ideal_left[1]))

		return self.mse(np.abs(pupil_co[0]/750-self.pupil_ideal_right[0]), 
				np.abs(pupil_co[1]/375-self.pupil_ideal_right[1]))

	def iris_error(self, iris_co, left=1):
		if left:
			return self.mse(np.abs(iris_co[0]-self.iris_ideal_left[0]),
				np.abs(iris_co[1]-self.iris_ideal_left[1]))

		return self.mse(np.abs(iris_co[0]-self.iris_ideal_right[0]),
				np.abs(iris_co[1]-self.iris_ideal_right[1]))

	def net_loss(self, pupil_co, iris_co):
		L1 = self.pupil_error(pupil_co)
		L2 = self.iris_error(iris_co)
		print("calc loss: " + str(self.A*L1 + self.B*L2))
		return self.A*L1 + self.B*L2
