import tkinter.ttk as ttk
from tkinter import Tk, messagebox, Frame, Menu, PhotoImage, BOTH
from tkinter.filedialog import askopenfilename
import os, socket, sys, json, time, ast

class Window(Frame):
    def __init__(self, master=None):
        """ create the master frame and class """

        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        """ declare the main window for gui drawing """

        self.master.title("PEA - Python Emulator for Audiovisual devices")
        self.pack(fill=BOTH, expand=1)
        self.colorList = ["#000000", "#991100", "#001199", "#DDEEFF"]

        # menu bar section ----------------------------------------------------
        menubar = Menu(root)
        filemenu1 = Menu(menubar, tearoff=0)
        filemenu1.add_command(label="Browse for Emulator JSON File", command=lambda i=1: self.browseFunction(i))
        filemenu1.add_separator()
        filemenu1.add_command(label="Emulator JSON Editor", command=self.hello)
        filemenu1.add_separator()
        filemenu1.add_command(label="Emulator Script Editor", command=self.hello)
        menubar.add_cascade(label="File", menu=filemenu1)

        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="HEX to ASCII Converter", command=self.hello)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.hello)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)  

    def hello(self):
        pass       

    def browseFunction(self, item):
        """ declare the function when pressed on the broswe button """
        pass     

def on_closing():
    """ closes the main window and kills the proces / task """

    if messagebox.askokcancel("Exit PEA", "Do you want to quit?"):
        root.destroy()
        num = os.getpid()
        os.system("taskkill /f /pid {}".format(num))

# run window class ------------------------------------------------------------

root = Tk()
root.geometry("1280x720")
root.resizable(width=False, height=False)
root.call("wm", "iconphoto", root._w, PhotoImage(file="icon.png"))
app = Window(root)

mystyle = ttk.Style()
mystyle.theme_use("vista")  # classic,default,clam,winnative,vista,xpnative,alt

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()