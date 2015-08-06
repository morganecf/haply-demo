from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle

class AnimationWidget(Widget):
	 
	def on_touch_down(self, touch):
		color = (random(), 1., 1.)
		# with statement allows all subsequent actions to occur on the canvas
		with self.canvas:
			Color(*color, mode='hsv')		# only the hue changes, so will have equally bright colors
			d = 50.
			Ellipse(pos = (touch.x - d/2, touch.y - d / 2), size = (d, d))


class BallApp(App):
	def build(self):
		# Will hold the painting canvas and the buttons (could also use layout)
		parent = Widget()
		self.animation = AnimationWidget()

		# Add a clear button that access clear callback function 
		clear = Button(text='clear')
		clear.bind(on_release=self.clear_canvas)

		# Make the canvas and the button children of the dummy widget
		parent.add_widget(self.animation)
		parent.add_widget(clear)

		return parent

	# Clear canvas callback function 
	def clear_canvas(self, obj):
		self.animation.canvas.clear()

if __name__ == '__main__':
	BallApp().run()
