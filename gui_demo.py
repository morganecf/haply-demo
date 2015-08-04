from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle

class MyPaintWidget(Widget):
	 
	def on_touch_down(self, touch):
		color = (random(), 1., 1.)
		# with statement allows all subsequent actions to occur on the canvas,
		# and after the actions are executed everything will be cleaned up 
		with self.canvas:
			Color(*color, mode='hsv')		# only the hue changes, so will have equally bright colors
			# Diameter of circle
			d = 30.
			# Draw the ellipse 
			Ellipse(pos = (touch.x - d/2, touch.y - d / 2), size = (d, d))
			# touch.ud is dictionary - stores custom attributes for a touch event 
			touch.ud['line'] = Line(points = (touch.x, touch.y))
		# When a motion event occurs, print its information
		print(touch)

	def on_touch_move(self, touch):
		# touch is the same motion event as before, but w/ updated attributes
		touch.ud['line'].points += [touch.x, touch.y]

	def add_circle(self, obj):
		color = (random(), 1., 1.)
		# with statement allows all subsequent actions to occur on the canvas,
		# and after the actions are executed everything will be cleaned up 
		with self.canvas:
			Color(*color, mode='hsv')		# only the hue changes, so will have equally bright colors
			# Diameter of circle
			d = 30.
			# Draw the ellipse 
			Ellipse(pos = (200, 200), size = (d, d))

	def add_rect(self, obj):
		color = (random(), 1., 1.)
		with self.canvas:
			Color(*color, mode='hsv')
			Rectangle(pos = (300, 300), size = (30, 30))

	def add_triangle(self, obj):
		color = (random(), 1., 1.)
		with self.canvas:
			Color(*color, mode='hsv')
			Triangle(pos = (200, 200), size = (30, 30))

class MyPaintApp(App):
	def build(self):
		# Will hold the painting canvas and the buttons (could also use layout)
		parent = Widget()
		self.painter = MyPaintWidget()

		# Create the necessary buttons 
		circle = Button(text='Circle')
		rect = Button(text='Rectangle')
		triangle = Button(text='Triangle')
		clear = Button(text='Clear')

		circle.set_center_y(150)
		rect.set_center_y(250)
		triangle.set_center_y(350)

		# Bind the buttons' on release events to callback functions
		circle.bind(on_release=self.painter.add_circle)
		rect.bind(on_release=self.painter.add_rect)
		triangle.bind(on_release=self.painter.add_triangle)
		clear.bind(on_release=self.clear_canvas)

		# Make the canvas and the button children of the dummy widget
		parent.add_widget(self.painter)
		parent.add_widget(circle)
		parent.add_widget(rect)
		parent.add_widget(triangle)
		parent.add_widget(clear)

		return parent

	# Clear canvas callback function 
	def clear_canvas(self, obj):
		self.painter.canvas.clear()

if __name__ == '__main__':
	MyPaintApp().run()


''' 
Useful examples 
- custom collide 
- everything in canvas
- everything in widgets
	color picker => for dragging and picking color 
- action bar 
- pop up (for instructions)
''' 
