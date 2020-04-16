import numpy as np

class losses():
	def __init__(self):
		self.pupil_ideal_left = (310/750, 170/375)
		self.pupil_ideal_right = (420/750, 170/375)
		self.iris_ideal_left = (0.5, 0.5)
		self.iris_ideal_right = (0.65, 0.65)

	def loss(self, x, y, A = 3.5, B = 0.5):
		return A*x + B*y

	def squared(self, x, y, A = 2, B = 2):
		return (x**2 + y**2)**(1/2)

	def pupil_error(self, pupil_co, left = 1):
		if left:
			return self.loss(np.square(pupil_co[0]/750-self.pupil_ideal_left[0]), 
				np.square(pupil_co[1]/375-self.pupil_ideal_left[1]))

		return self.loss(np.square(pupil_co[0]/750-self.pupil_ideal_right[0]), 
				np.square(pupil_co[1]/375-self.pupil_ideal_right[1]))

	def iris_error(self, iris_co, left = 1):
		if left:
			return self.loss(np.square(iris_co[0]-self.iris_ideal_left[0]),
				np.square(iris_co[1]-self.iris_ideal_left[1]), A = 2.7, B = 1.3)

		return self.loss(np.square(iris_co[0]-self.iris_ideal_right[0]),
				np.square(iris_co[1]-self.iris_ideal_right[1]), A = 2.7, B = 1.3)

	def net_loss(self, pupil_co, iris_co, A = 0.2, B = 0.8, left = 1):
		L1 = self.pupil_error(pupil_co)
		L2 = self.iris_error(iris_co)
		return A*L1 + B*L2
