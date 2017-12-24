# -*- coding: utf-8 -*-
import tkinter as tk
from queue import Queue
from PIL import Image, ImageTk
import threading
import io


class IDE(object):
    def __init__(self, title='GUI', ratio=0.5, pic=Queue()):
        self._ratio = ratio
        self._queue = Queue()
        self._pic = pic
        self._root = tk.Tk()
        self._root.resizable(0, 0)
        self._root.title(title)
        frm_screen = tk.Frame(self._root, bg='#aaa')
        self.canvas = tk.Canvas(frm_screen, bg="blue", bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(column=0, row=0, padx=10, pady=10)
        self._image = None
        
        self._init_thread()
        
#        self._refresh()
#        self.canvas.bind("<Button-1>", self._stroke_start)
#        self.canvas.bind("<B1-Motion>", self._stroke_move)
#        self.canvas.bind("<B1-ButtonRelease>", self._stroke_done)
#        self.canvas.bind("<Motion>", self._mouse_move)
    def _worker(self):
        while True:
            (func, args, kwargs) = self._queue.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                self._queue.task_done()

    def _init_thread(self):
        th = threading.Thread(name='thread', target=self._worker)
        th.daemon = True
        th.start()
                
    def _run_async(self, func, args=(), kwargs={}):
        self._queue.put((func, args, kwargs))

    def _refresh(self):
        def foo():
            print('refresh')
            image = Image.open(io.BytesIO(self._pic.get()))
            print(type(image))
            self._pic.get()
            print('refresh...')
            self.draw_image(image)
        self._run_async(foo)
        self._root.after(10, self._refresh)        


    def draw_image(self, image):
        self._image = image
        self._size = (width, height) = image.size
        w, h = int(width*self._ratio), int(height*self._ratio)
        # print w, h
        image = image.copy()
        image.thumbnail((w, h), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(image)
        self._tkimage = tkimage # keep a reference
        self.canvas.config(width=w, height=h)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tkimage)

    def mainloop(self):
        self._root.mainloop()
