"""

callme.py is a diagnostic tool that just displays the command-line
parameters that it has been called with.

"""

import Tkinter
from Tkconstants import *

if __name__ == '__main__':

    tk = Tkinter.Tk()
    frame = Tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH,expand=1)
    label = Tkinter.Message(frame, text="\n".join(sys.argv))
    label.pack(fill=X, expand=1)
    button = Tkinter.Button(frame,text="Exit",
                  command=tk.destroy,
                  default=ACTIVE)
    button.pack(side=BOTTOM)

    tk.mainloop()

