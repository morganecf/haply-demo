from Tkinter import *

root = Tk()

# Initialize the welcome message
top = Toplevel()
top.title("Welcome!")
msg_image = PhotoImage(file="demo-welcome-message.gif")
msg = Label(top, image=msg_image)
#msg.image = msg_image
msg.pack()
button = Button(top, text="Got it!", command=top.destroy)
button.pack()

# def key(event):
#     print "pressed", repr(event.char)

# def callback(event):
#     frame.focus_set()
#     print "clicked at", event.x, event.y

# frame = Frame(root, width=100, height=100)
# frame.bind("<Key>", key)
# frame.bind("<Button-1>", callback)
# frame.pack()

root.mainloop()