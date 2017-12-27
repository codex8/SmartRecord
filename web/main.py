#!/usr/bin/env python
# coding: utf-8
from ide import CropIDE
from minicap import Stream
from queue import Queue
import logutils
import logging
log = logutils.getLogger('tkgui')
log.setLevel(logging.DEBUG)


def main(serial=None, scale=0.5):
    log.debug("gui starting(scale: {}) ...".format(scale))
    # d = u2.connect_usb(serial)
    # gui = CropIDE('GUI SN: %s' % serial, ratio=scale, device=d)
    # gui.mainloop()

    q = Queue()
    a = Stream.getBuilder(ip='127.0.0.1', port=1313, queue=q)
    a.run()
    gui = CropIDE(title='SmartRecord', picture=q)
    gui.mainloop()


if __name__ == '__main__':
    main()

def test():
    gui = CropIDE('AirtestX IDE')
    image = Image.open('screen.png')
    gui.draw_image(image)
    # gui.refresh_screen()
    # gui.draw_point(100, 100)
    gui.mainloop()


if __name__ == '__main__':
    # test()
    main(None)
