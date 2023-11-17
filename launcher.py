import tkinter as tk

# Create the main application window
app = tk.Tk()
app.title("Simple Tkinter GUI")

# Create and add a label to the window
label = tk.Label(app, text="Hello, Tkinter!")
label.pack()  # Pack the label into the window

# Create a function to be triggered when the button is clicked


def on_button_click():
    label.config(text="Button clicked!")


# Create and add a button to the window
button = tk.Button(app, text="Click me!", command=on_button_click)
button.pack()  # Pack the button into the window

# Start the main event loop
app.mainloop()
