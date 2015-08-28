
#import zmq

from random import random
from functools import partial 

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics.vertex_instructions import Triangle


class DTriangle(Triangle):

	''' Triangle class just for the demo ''' 

	def __init__(self, pos, size):
		d = size[0]
		p1 = pos 
		p2 = (pos[0] + (d / 2), pos[1] + d)
		p3 = (pos[0] + d, pos[1])
		Triangle.__init__(self, points=[p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]])


class Simulation(Widget):

	''' 
	Contains the interaction canvas on which the shapes are placed.
	'''

	# Will contain all the shapes the user creates 
	shapes = {
		'rect': [],
		'triangle': [],
		'circle': []
	}

	# Factory of shapes
	factory = {
		'rect': Rectangle,
		'circle': Ellipse,
		'triangle': DTriangle
	}

	# Automatic diameter of a shape
	d = 50.

	def add_shape(self, typ):
		# Initialize a random circle
		color = (random(), 1., 1.)

		# Initialize a random spot on the canvas
		p = (100 + random() * 600, 100 + random() * 600)

		# The with statement allows all subsequent actions to occur on the canvas
		with self.canvas:
			# Only the hue changes, so will have equally bright colors
			Color(*color, mode='hsv')		
			
			shape = self.factory[typ](pos = p, size = (self.d, self.d))
			self.shapes[typ].append(shape)

	# Listen for position information from backend 
	def update(self, timestep):
		pass
			

class DemoApp(App):

	''' The gravity app ''' 

	def build(self):
		# The parent widget that will hold everything 
		parent = Widget() 

		# Create the canvas simulation 
		self.simulation = Simulation()

		# Schedule a simulation update every 100 hz
		Clock.schedule_interval(self.simulation.update, 1.0 / 100.0)

		# This button will clear the canvas of any circles
		clear = Button(text='clear')
		clear.bind(on_release=self.clear_canvas)

		# This button will add a rectangle
		rect = Button(text='rect')
		rect.bind(on_release=lambda s: self.simulation.add_shape('rect'))

		# This button will add a circle
		circle = Button(text='circle')
		circle.bind(on_release=lambda s: self.simulation.add_shape('circle'))

		# This button will add a triangle 
		triangle = Button(text='triangle')
		triangle.bind(on_release=lambda s: self.simulation.add_shape('triangle'))

		# Position the buttons
		rect.set_center_y(150)
		circle.set_center_y(250)
		triangle.set_center_y(350)

		# Add widgets to the main parent widget
		parent.add_widget(self.simulation)
		parent.add_widget(clear)
		parent.add_widget(rect)
		parent.add_widget(circle)
		parent.add_widget(triangle)

		# Tell server we're ready 
		#self.simulation.socket.send_string("ready")

		return parent

	def clear_canvas(self, obj):
		self.simulation.canvas.clear()
		self.simulation.shapes = []


if __name__ == '__main__':
	DemoApp().run()
