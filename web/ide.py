#!/usr/bin/env python
# coding: utf-8
import os
import threading
import logging
import tkinter as tk
from queue import Queue
import logutils
from layoututils import dump_nodes
import uiautomator2 as u2
from PIL import Image, ImageTk
import io
log = logutils.getLogger('tkgui')
log.setLevel(logging.DEBUG)


class CropIDE(object):
    def __init__(self, title='AirtestX Basic GUI', ratio=0.5, picture=Queue):
        self._picture = picture
        self._root = tk.Tk()
        self._root.title(title)
        self._queue = Queue()
        self._ratio = ratio

        self._image = Image.open(r'/home/cts/PycharmProjects/SmartRecord2.0/screen.png')
        self._size = (90, 90)
        self._tkimage = None
        self._uinodes = None
        self._poffset = (0, 0)
        self._color = 'red'

        self._init_items()
        self._init_thread()
        self._refresh_screen()

    def _init_items(self):
        root = self._root
        root.resizable(0, 0)

        frm_screen = tk.Frame(root, bg='#aaa')
        frm_screen.grid(column=1, row=0)

        self.canvas = tk.Canvas(frm_screen, bg="blue", bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid(column=0, row=0, padx=10, pady=10)
        self._tkimage = ImageTk.PhotoImage(self._image)
        self._test = self.canvas.create_image(0, 0, anchor=tk.NW, image=self._tkimage)
        self.canvas.bind("<Motion>", self._mouse_move)

    def _init_thread(self):
        th = threading.Thread(name='thread', target=self._worker)
        th.daemon = True
        th.start()

    def _worker(self):
        que = self._queue
        while True:
            (func, args, kwargs) = que.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                log.error(e)
            finally:
                que.task_done()

    def _run_async(self, func, args=(), kwargs={}):
        self._queue.put((func, args, kwargs))

    def _refresh_screen(self):
        def foo():
            image = Image.open(io.BytesIO(self._picture.get()))
            self.draw_image(image)
            # hierarchy_view = self._device.dump_hierarchy()
            # self._uinodes = dump_nodes(hierarchy_view)
            # print(len(layout))
        self._run_async(foo)
        self._root.after(1, self._refresh_screen)

    def draw_image(self, image):
        self._image = image
        self._size = (width, height) = image.size
        w, h = int(width*self._ratio), int(height*self._ratio)
        image = image.copy()
        image.thumbnail((w, h), Image.ANTIALIAS)
        self._tkimage = ImageTk.PhotoImage(image)
        self.canvas.config(width=w, height=h)
        self.canvas.itemconfig(self._test, anchor=tk.NW, image=self._tkimage)

    def _mouse_move(self, event):
        pass
        # c = self.canvas
        # x, y = c.canvasx(event.x), c.canvasy(event.y)
        # x, y = x/self._ratio, y/self._ratio
        # hovered_node = None
        # min_area = None
        # for node in self._uinodes:
        #     if node.bounds.is_inside(x, y):
        #         if min_area is None or node.bounds.area < min_area:
        #             hovered_node = node
        #             min_area = node.bounds.area
        # if hovered_node:
        #     self._hovered_node = hovered_node
        #     self._reset()
        #     self._draw_lines()

    def _reset(self):
        self._bounds = None
        self._offset = (0, 0)
        self._poffset = (0, 0)
        self._center = (0, 0)
        self.canvas.delete('select-bounds')
        self.canvas.delete('select-point')
        self.canvas.delete('ui-bounds')

    # def _draw_lines(self):
    #     if self._center and self._center != (0, 0):
    #         x, y = self._center
    #         self.draw_point(x, y)
    #     if self._bounds:
    #         self._draw_bounds(self._bounds)
    #     if self._hovered_node:
    #         # print self._hovered_node.bounds
    #         bounds = [v*self._ratio for v in self._hovered_node.bounds]
    #         self._draw_bounds(bounds, color='blue')

    def draw_point(self, x, y):
        self.canvas.delete('select-point')
        r = max(min(self._size)/30*self._ratio, 5)
        self.canvas.create_line(x-r, y, x+r, y, width=2, fill=self._color, tags='select-point')
        self.canvas.create_line(x, y-r, x, y+r, width=2, fill=self._color, tags='select-point')

    def _draw_bounds(self, bounds, color=None):
        if not color:
            color = self._color
        c = self.canvas
        (x0, y0, x1, y1) = bounds
        c.create_rectangle(x0, y0, x1, y1, outline=color, tags='select-bounds', width=2)

    def mainloop(self):
        self._root.mainloop()
#
#
# def main(serial, scale=0.5):
#     log.debug("gui starting(scale: {}) ...".format(scale))
#     d = u2.connect_usb(serial)
#     gui = CropIDE('GUI SN: %s' % serial, ratio=scale, device=d)
#     gui.mainloop()
#
#
# def test():
#     gui = CropIDE('AirtestX IDE')
#     image = Image.open('screen.png')
#     gui.draw_image(image)
#     # gui.refresh_screen()
#     # gui.draw_point(100, 100)
#     gui.mainloop()
#
#
# if __name__ == '__main__':
#     # test()
#     main(None)
