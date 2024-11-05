import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()


def hello():
    label = tk.Label(root, text="Hello world", fg='green',
                     font=('helvetica', 12, 'bold'))
    canvas.create_window(150, 200, window=label)


button = tk.Button(text="Click me", fg='black', command=hello)
canvas.create_window(150, 150, window=button)

root.mainloop()
