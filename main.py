import tkinter.ttk as ttk
from tkinter import Tk, messagebox, Frame, Menu, PhotoImage, BOTH, LEFT
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
        self.colorList = ["#FF0000", "#00FF00", "#DDEEFF"]  

        # menu bar section ----------------------------------------------------
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Browse for Emulator JSON File", command=lambda: self.browseFunction())
        filemenu.add_separator()
        filemenu.add_command(label="Exit PEA", command=lambda: on_closing())
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Emulator JSON Editor", command=self.hello)
        editmenu.add_separator()
        editmenu.add_command(label="Emulator Script Editor", command=self.hello)
        menubar.add_cascade(label="File", menu=editmenu)        

        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="HEX - ASCII Converter", command=self.hello)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About PEA", command=self.hello)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)  

        # top grid section --------------------------------------------------

        fileframe = ttk.LabelFrame(self, text="Emulator JSON File",)
        fileframe.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        filelabel = ttk.Label(fileframe, width=90)
        filelabel.config(text="No JSON file loaded", background=self.colorList[2], 
           borderwidth=1, relief="solid", anchor="center")
        filelabel.pack(padx=5, pady=5, side=LEFT)

        portframe = ttk.LabelFrame(self, text="TCP Port",)
        portframe.grid(row=0, column=1, padx=8, pady=8, sticky='nsew')
        portlabel = ttk.Label(portframe, text="Port")
        portlabel.pack(padx=5, pady=5, side=LEFT)
        portentry = ttk.Entry(portframe, width=6)
        portentry.insert(0, "0")
        portentry.pack(padx=5, pady=5, side=LEFT)        
        portbutton = ttk.Button(portframe,
            text="Open Port", width=13,
            command=lambda: self.listenFunction(),
        )
        portbutton.pack(padx=5, pady=5, side=LEFT)

        connectionframe = ttk.LabelFrame(self, text="TCP Connection",)
        connectionframe.grid(row=0, column=2, padx=8, pady=8, sticky='nsew')
        self.colorlabel = ttk.Label(connectionframe, width=3, text="")
        self.colorlabel.pack(padx=5, pady=5, side=LEFT)
        self.colorlabel.config(background=self.colorList[0])  
        connectbutton = ttk.Button(connectionframe,
            text="Connect", width=13,
            command=lambda: self.connectFunction()
        )
        connectbutton.pack(padx=5, pady=5, side=LEFT)
        connectbutton.config(state="disabled")

        # send grid section --------------------------------------------------

        sendframe = ttk.LabelFrame(self, text="Send Command",)
        sendframe.grid(row=1, column=0, padx=8, pady=8, sticky='nsew')
        sendlabel = ttk.Label(sendframe, text="String")
        sendlabel.pack(padx=5, pady=5, side=LEFT)
        sendentry = ttk.Entry(sendframe, width=66)
        sendentry.insert(0, "Enter ASCII direct or HEX strings with prefix \\\\x")
        sendentry.pack(padx=5, pady=5, side=LEFT)        
        sendbutton = ttk.Button(sendframe,
            text="Send", width=13,
            command=lambda: self.sendFunction(),
        )
        sendbutton.pack(padx=5, pady=5, side=LEFT)
        sendbutton.config(state="disabled")




    def hello(self):
        pass       

    def browseFunction(self):
        """ declare the function when pressed on the browse button """
        pass     

    def listenFunction(self):
        """ declare the function when pressed on the port button """
        pass     

    def connectFunction(self):
        """ declare the function when pressed on the connect button """
        pass             

    def sendFunction(self):
        """ declare the function when pressed on the connect button """
        pass  

def on_closing():
    """ closes the main window and kills the proces / task """
    print('exit')

    if messagebox.askokcancel("Exit PEA", "Do you want to quit?"):
        root.destroy()
        num = os.getpid()
        os.system("taskkill /f /pid {}".format(num))


root = Tk()
root.geometry("930x720")
root.resizable(width=False, height=False)
root.call("wm", "iconphoto", root._w, PhotoImage(file="icon.png"))
app = Window(root)

mystyle = ttk.Style()
mystyle.theme_use("vista")  # classic,default,clam,winnative,vista,xpnative,alt

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()