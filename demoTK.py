import zmq
import random
from datetime import datetime

from Tkinter import *

''' 
	Shape classes. Each one inherits from Shape and 
	implements the appropriate create function based on
	Tkinter's create_* function.
''' 

class Shape:
	def __init__(self, canvas, pos, size, color):
		self.canvas = canvas
		self.pos = pos
		self.size = size 
		self.color = color[0]
		self.dark = color[1]
		self.light = color[2]
		self.w = 3
		self.mass = 10

	def __str__(self):
		# String representation of a shape is its position and mass 
		return str(self.pos[0]) + ',' + str(self.pos[1]) + ',' + str(self.mass)


class Square(Shape):

	# pos refers to the top left corner of the square 
	def create(self):
		coords = [self.pos[0], self.pos[1], self.pos[0] + self.size, self.pos[1] + self.size]
		return self.canvas.create_rectangle(coords, width=self.w, fill=self.color, outline=self.dark, activefill=self.light)


class Circle(Shape):

	# pos refers to the center of the circle
	def create(self):
		TL = [self.pos[0] - (self.size / 2), self.pos[1] - (self.size / 2)]
		BR = [self.pos[0] + (self.size / 2), self.pos[1] + (self.size / 2)]
		coords = TL + BR
		return self.canvas.create_oval(coords, width=self.w, fill=self.color, outline=self.dark, activefill=self.light)


class Triangle(Shape):

	# pos refers to the tip of the triangle 
	def create(self):
		BL = [self.pos[0] - (self.size / 2), self.pos[1] + self.size]
		BR = [self.pos[0] + (self.size / 2), self.pos[1] + self.size]
		coords = self.pos + BL + BR + self.pos
		return self.canvas.create_polygon(coords, width=self.w, fill=self.color, outline=self.dark, activefill=self.light)


class DemoApp(Tk):

	''' Where the canvas drawing happens ''' 

	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent

		# Keeps track of all the created shapes 
		self.shapes = {}

		# Factory of shape types 
		self.factory = {
			'square': Square,
			'circle': Circle,
			'triangle': Triangle
		}

		# The default shape size 
		self.d = 50

		# Default colors - (regular, dark, light)
		self.colors = {
			'jigsaw': ('#F1DF9D', '#C1B27E', '#F9F2D8'),
			'summer': ('#8CC9C2', '#70A19B', '#D1E9E7'),
			'lullaby': ('#F54F51', '#C43F41', '#FBB9B9'),
			'blue': ('#334377', '#29365F', '#ADB4C9'),
			'macaroni': ('#FA982D', '#C87A24', '#FDD6AB'),
			'emerald': ('#198C55', '#147044', '#A3D1BB'),
			'purple': ('#702566', '#5A1E52', '#B892B2')
		}

		# Default name prompt and string
		self.name_prompt = "What's your name?"
		self.name_str = "Anonymous"

		# The canvas size 
		self.width = 700
		self.height = 500

		# Keeps track of what the mouse is doing 
		self.moving = None
		self.mouse = None

		# Tells us if we're in haptic mode or not
		self.hapified = False

		# Set up the TCP client 
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REQ)
		self.socket.connect("tcp://localhost:5556")

		# Initialize the canvas 
		self.initialize()


	def initialize(self):
		# Initialize the work area 
		self.grid()

		# Create the shape buttons
		square = Button(self, text='Square', command=lambda: self.add_shape('square'))
		circle = Button(self, text='Circle', command=lambda: self.add_shape('circle'))
		triangle = Button(self, text='Triangle', command=lambda: self.add_shape('triangle'))

		# Add them to the grid
		square.grid(row=0, column=0)
		circle.grid(row=0, column=1)
		triangle.grid(row=0, column=2)

		# Add placeholder text to keep the width the same
		self.ptitle = Text(self, height=0, width=30)
		self.ptitle.insert(END, self.name_str + "'s 2D haptic world!")
		self.ptitle.grid(row=0, column=4)

		# Add a clear canvas button 
		clear = Button(self, text='Clear', command=self.clear)
		clear.grid(row=0, column=5)

		# Add a "hapify" button to haptically enable the shapes
		self.hapifyBtn = Button(self, text='Hapify', command=self.hapify)
		self.hapifyBtn.grid(row=0, column=6)

		# Create the canvas on which shapes will be drawn
		self.canvas = Canvas(self, width=self.width, height=self.height)
		self.canvas.grid(row=1, columnspan=7)

		# Listen to mouse click + drag events 
		self.canvas.bind("<Button-1>", self.click)
		self.canvas.bind("<B1-Motion>", self.move)
		self.canvas.bind("<ButtonRelease-1>", self.up)
		self.canvas.bind("<Double-Button-1>", self.double_click)

		# Place the canvas in the middle of the screen
		ws = self.winfo_screenwidth()
		sx = (ws / 2) - (self.width / 2)
		self.geometry('%dx%d+%d+%d' % (self.width, self.height, sx, 0))

		# Initialize the welcome message
		top = Toplevel()
		top.title("Welcome!")
		msg_image = PhotoImage(file="demo-welcome-message.gif")
		msg = Label(top, image=msg_image)
		msg.image = msg_image
		msg.pack()

		# Get the player's name 
		name = Entry(top)
		name.insert(0, self.name_prompt)
		name.pack()
		button = Button(top, text="Let's start!", command=lambda: self.get_name(top, name))
		button.pack()
		
		# Make sure the welcome message appears in front of the app
		top.attributes("-topmost", True)
		top.geometry('%dx%d+%d+%d' % (self.width, self.height, sx, 0))


	def get_name(self, top, name):
		# Get the user's name from the welcome instructions
		self.user = name.get()
		if self.user == self.name_prompt:
			self.user = self.name_str

		# Destroy the dialog box 
		top.destroy()

		# Add a personalized title to the canvas 
		self.ptitle.grid_forget()
		self.ptitle = Text(self, height=0, width=30)
		self.ptitle.insert(END, self.user + "'s 2D haptic world!")
		self.ptitle.grid(row=0, column=4)

		# Save name + time played to file 
		f = open('x1-demo-users.txt', 'a')
		f.write(self.user + '\t' + str(datetime.now()) + '\n')
		f.close()


	def clear(self):
		# Only allow editing if not in haptic mode
		if self.hapified: 
			return 

		self.shapes = {}
		self.canvas.delete("all")


	def add_shape(self, typ):
		# Only allow editing if not in haptic mode
		if self.hapified: 
			return 

		# Find a random position on the canvas 
		p = [random.random() * (self.width - 100), random.random() * (self.height - 100)]

		# Pick a random color
		color = self.colors[random.choice(self.colors.keys())]

		# Create the correct shape 
		shape = self.factory[typ](canvas=self.canvas, pos=p, size=self.d, color=color)
		sid = shape.create()

		# Save it 
		self.shapes[sid] = shape


	def click(self, event):
		# Only allow editing if not in haptic mode
		if self.hapified: 
			return 

		shape = self.canvas.find_withtag("current")
		if shape:
			self.moving = shape
			self.mouse = [event.x, event.y]
	

	def double_click(self, event):
		# Only allow editing if not in haptic mode
		if self.hapified: 
			return 

		shape = self.canvas.find_withtag("current")
		if shape:
			# Find the corresponding shape object 
			shape_obj = self.shapes[shape[0]]

			# Open a dialog box to edit shape's mass
			dialog = Toplevel()
			dialog.title("Edit mass")
			mass = Entry(dialog)
			mass.insert(0, shape_obj.mass)
			mass.pack()
			button = Button(dialog, text="Done", command=lambda: self.on_mass_change(shape_obj, mass, dialog))
			button.pack()
			dialog.geometry('%dx%d+%d+%d' % (180, 55, event.x + 150, event.y))


	def on_mass_change(self, shape, mass, dialog):
		# Change the shape's mass 
		shape.mass = int(mass.get())
		dialog.destroy()


	def move(self, event):
		# Only allow editing if not in haptic mode
		if self.hapified: 
			return 

		# Find the mouse displacement 
		dx = event.x - self.mouse[0]
		dy = event.y - self.mouse[1]

		# Move the clicked shape 
		self.canvas.move(self.moving, dx, dy)
		coords = self.canvas.coords(self.moving)

		# Update the shape's coordinates 
		new_coords = [coords[0] + dx, coords[1] + dy, coords[2] + dx, coords[3] + dy]
		self.canvas.coords(self.moving, *new_coords)

		# Update the last mouse position
		self.mouse = [event.x, event.y]


	def up(self, event):
		# Only allow editing if not in haptic mode
		if self.hapified: 
			return 

		self.moving = None
		self.mouse = None


	# Haptically enable/disable all of the shapes 
	def hapify(self):
		if self.hapified:
			self.hapified = False 

			# Hapify button 
			self.hapifyBtn.grid_forget()
			self.hapifyBtn = Button(self, text='Hapify', command=self.hapify)
			self.hapifyBtn.grid(row=0, column=6)

			# Send dehapify request to the server
			self.socket.send("dehapify")
			print self.socket.recv()

		else:
			self.hapified = True 

			# Dehapify button 
			self.hapifyBtn.grid_forget()
			self.hapifyBtn = Button(self, text='Dehapify', command=self.hapify)
			self.hapifyBtn.grid(row=0, column=6)

			# Send hapify request to the server
			self.socket.send("hapify")
			print self.socket.recv()

			# Send shape information over to the server
			# Format: sid,posx,posy,mass
			shape_info = '\t'.join([str(s) + ',' + str(self.shapes[s]) for s in self.shapes.keys()])
			self.socket.send(shape_info)

			# Listen for server-side information
			self.update()


	# Listen for positional information from backend 
	def update(self):
		# Don't update if hapify mode is disabled
		if not self.hapified:
			return

		# Otherwise listen every 1 s 
		positions = self.socket.recv()

		# Only for the sample simulation, not for the real demo
		if positions == 'simulation done':
			return
		
		self.socket.send('received positions')

		# Update the shapes' positions 
		positions = positions.strip().split('\t')
		for position in positions:
			# Update the object
			sid, x, y, m = position.split(',')
			sid = int(sid)
			shape = self.shapes[sid]
			shape.pos = [float(x), float(y)]

			# Move the canvas shape -- TODO: THIS IS ONLY FOR THE EXAMPLE SIMULATION
			# WILL NEED TO CALCULATE DISPLACEMENT IN BACKEND AND SEND IT OVER
			dx = 5
			dy = 5 
			self.canvas.move(sid, dx, dy)
			coords = self.canvas.coords(sid)

			# Update the shape's coordinates 
			new_coords = [coords[0] + dx, coords[1] + dy, coords[2] + dx, coords[3] + dy]
			self.canvas.coords(sid, *new_coords)

		self.after(1, self.update)



if __name__ == "__main__":
	# Run the app 
	app = DemoApp(None)
	app.title('Haplet Desktop Demo')
	app.mainloop()


