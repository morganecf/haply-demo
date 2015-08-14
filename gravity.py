
import zmq
import sys

from random import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle


class GravitySimulation(Widget):

	''' 
	The gravity simulation. Contains the canvas 
	on which the balls are created and fall. 
	'''

	# Will contain all the balls the user creates 
	balls = []
	gravity = NumericProperty(9.81)

	# The user cursor (haptic avatar)
	cursor = None

	# Will contain all the obstacles the user can create
	obstacles = []

	# For testing
	n = 0

	# Set up the TCP subscriber client
	# context = zmq.Context()
	# socket = context.socket(zmq.SUB)
	# socket.connect("tcp://localhost:5556")
	# socket.setsockopt_string(zmq.SUBSCRIBE, u"pos")

	# Set up the TCP client 
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://localhost:5556")

	# When the user clicks, a ball is formed 
	def on_touch_down(self, touch):
		# Initialize a random circle
		color = (random(), 1., 1.)

		# The with statement allows all subsequent actions to occur on the canvas
		with self.canvas:
			# Only the hue changes, so will have equally bright colors
			Color(*color, mode='hsv')		
			d = 50.
			
			# ball = Ellipse(pos = (touch.x - d/2, touch.y - d / 2), size = (d, d))
			# self.balls.append(ball)

			obst = Rectangle(pos = (touch.x - d / 2, touch.y - d / 2), size = (d, d))
			self.obstacles.append(obst)

			# Send information to socket 
			self.socket.send_string("rect");

	# Add a red cursor to the screen
	def add_cursor(self):
		with self.canvas:
			Color(1., 0, 0)
			self.cursor = Ellipse(pos = (100, 50), size = (10, 10))


	# Balls should fall under the force of gravity (-9.81*t^2)
	def update(self, timestep):
		self.n += 1

		# Listen for position information 
		position = self.socket.recv_string().split()

		# Ignore header information 
		if position[0] == 'pos':
			return

		# Update the cursor
		self.cursor.pos = (int(position[0]), int(position[1]))

		# Update balls
		# for ball in self.balls:
		# 	print 'gravity', self.gravity
		# 	ball.pos = (ball.pos[0], ball.pos[1] - (timestep * self.gravity))
			

class GravityApp(App):

	''' The gravity app ''' 

	def build(self):
		# The parent widget that will hold everything 
		parent = Widget() 

		# Create the simulation 
		self.simulation = GravitySimulation()

		# Add the haptic mouse avatar
		self.simulation.add_cursor()

		# Schedule a simulation update every 100 hz
		Clock.schedule_interval(self.simulation.update, 1.0 / 100.0)

		# This button will clear the canvas of any circles
		clear = Button(text='clear')
		clear.bind(on_release=self.clear_canvas)

		# This button will increase the force of gravity 
		increase = Button(text='+')
		increase.bind(on_release=self.increase_gravity)

		# This button will decrease the force of gravity 
		decrease = Button(text='-')
		decrease.bind(on_release=self.decrease_gravity)

		# Position the buttons
		increase.set_center_y(150)
		decrease.set_center_y(250)

		# Add widgets to the main parent widget
		parent.add_widget(self.simulation)
		parent.add_widget(clear)
		parent.add_widget(increase)
		parent.add_widget(decrease)

		# Tell server we're ready 
		self.simulation.socket.send_string("ready")

		return parent

	def clear_canvas(self, obj):
		self.simulation.canvas.clear()

	def increase_gravity(self, obj):
		self.simulation.gravity += 10.0

	def decrease_gravity(self, obj):
		self.simulation.gravity -= 10.0

if __name__ == '__main__':
	GravityApp().run()
