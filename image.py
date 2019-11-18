import tkinter as tk
from PIL import Image, ImageTk
def on_click(event=None):
    # `command=` calls function without argument
    # `bind` calls functio n with one argument
    print("image clicked")
root = tk.Tk()

# load image
image = Image.open("image.png")
photo = ImageTk.PhotoImage(image)

# label with image
l = tk.Label(root, image=photo)
l.pack()

# bind click event to image
l.bind('<Button-1>', on_click)

# button with image binded to the same function
b = tk.Button(root, image=photo, command=on_click)
b.pack()

# button with text closing window
b = tk.Button(root, text="Close", command=root.destroy)
b.pack()

# "start the engine"
root.mainloop()


