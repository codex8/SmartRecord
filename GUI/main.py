# -*- coding: utf-8 -*-
from queue import Queue
from minicap import Stream
from Ide import IDE


def main():
#    q = Queue()
#    
#    a = Stream.getBuilder(ip='127.0.0.1', port=1313, queue=q)
#    
#    a.run()
    gui = IDE(title='SmartRecord', pic=Queue())
    gui.mainloop()


if __name__ == '__main__':
    main()