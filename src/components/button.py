from tkinter import *

def DefaultButton(parent):
    # Create a Frame for border
    border_color = Frame(parent, background="gray20")

    # Label Widget inside the Frame
    label = Button(border_color, text="This is a Label widget", bd=0)
    label.pack()

    border_color.pack()