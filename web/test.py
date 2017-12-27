import tkinter as tk
import threading
import time
root = tk.Tk()
canvas = tk.Canvas(root)
canvas.pack()
item = canvas.create_rectangle(50, 25, 1500, 750, fill="blue")


def fresh():
    time.sleep(1)
    while 1:
        canvas.itemconfig(item,fill='red')
        canvas.itemconfig(item,fill='blue')


t = threading.Thread(target=fresh)
t.start()
# button = tk.Button(root,text='Push me!',command=callback)
# button.pack()

root.mainloop()
