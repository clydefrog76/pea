from threading import Thread
import tkinter.ttk as ttk
from tkinter import Tk, messagebox, Text, Frame, Menu, PhotoImage, BOTH, LEFT, RIGHT, END
from tkinter.filedialog import askopenfilename
import os, socket, sys, json, time, ast, datetime

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
        self.colorList = ["#FF0000", "#00FF00", "#DDEEFF", "#000000"]  
        self.terminalrunning = True
        self.commandsList = None

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

        mainframe1 = ttk.Frame(self)
        mainframe1.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

        fileframe = ttk.LabelFrame(mainframe1, text="Emulator JSON File",)
        fileframe.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        self.filelabel = ttk.Label(fileframe, width=90)
        self.filelabel.config(text="No JSON file loaded", background=self.colorList[2], 
           borderwidth=1, relief="solid", anchor="center")
        self.filelabel.pack(padx=5, pady=5, side=LEFT)

        portframe = ttk.LabelFrame(mainframe1, text="TCP Port",)
        portframe.grid(row=0, column=1, padx=8, pady=8, sticky='nsew')
        portlabel = ttk.Label(portframe, text="Port")
        portlabel.pack(padx=5, pady=5, side=LEFT)
        self.portentry = ttk.Entry(portframe, width=6)
        self.portentry.insert(0, "0")
        self.portentry.pack(padx=5, pady=5, side=LEFT)        
        self.portbutton = ttk.Button(portframe,
            text="Open Port", width=13,
            command=lambda: self.listenFunction(),
        )
        self.portbutton.pack(padx=5, pady=5, side=LEFT)

        connectionframe = ttk.LabelFrame(mainframe1, text="TCP Connection",)
        connectionframe.grid(row=0, column=2, padx=8, pady=8, sticky='nsew')
        self.colorlabel = ttk.Label(connectionframe, width=3, text="")
        self.colorlabel.pack(padx=5, pady=5, side=LEFT)
        self.colorlabel.config(background=self.colorList[0])  
        self.disconnectbutton = ttk.Button(connectionframe,
            text="Disconnect", width=13,
            command=lambda: self.disconnectFunction()
        )
        self.disconnectbutton.pack(padx=5, pady=5, side=LEFT)
        self.disconnectbutton.config(state="disabled")

        # send grid section --------------------------------------------------

        mainframe2 = ttk.Frame(self)
        mainframe2.grid(row=1, column=0, padx=0, pady=0, sticky='nsew')

        sendframe = ttk.LabelFrame(mainframe2, text="Send Command",)
        sendframe.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        sendlabel = ttk.Label(sendframe, text="String")
        sendlabel.pack(padx=5, pady=5, side=LEFT)
        self.sendentry = ttk.Entry(sendframe, width=50)
        self.sendentry.insert(0, "Enter ASCII direct or HEX strings with prefix \\\\x")
        self.sendentry.pack(padx=5, pady=5, side=LEFT)        
        self.sendbutton = ttk.Button(sendframe,
            text="Send", width=13,
            command=lambda: self.sendFunction(),
        )
        self.sendbutton.pack(padx=5, pady=5, side=LEFT)
        self.sendbutton.config(state="disabled")

        # terminal commands grid section --------------------------------------

        mainframe3 = ttk.Frame(self)
        mainframe3.grid(row=2, column=0, padx=0, pady=0, sticky='nsew')

        terminalfuncframe = ttk.LabelFrame(mainframe3, text="Terminal Functions",)
        terminalfuncframe.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')

        startbutton = ttk.Button(
            terminalfuncframe,
            text="Run",
            width=13,
            command=lambda i=1: self.runstopFunction(i)
        )
        startbutton.pack(padx=5, pady=5, side=LEFT)

        stopbutton = ttk.Button(
            terminalfuncframe,
            text="Stop",
            width=13,
            command=lambda i=2: self.runstopFunction(i),
        )
        stopbutton.pack(padx=5, pady=5, side=LEFT)

        clearbutton = ttk.Button(
            terminalfuncframe, 
            text="Clear", 
            width=13, 
            command=lambda: self.clearFunction()
        )
        clearbutton.pack(padx=5, pady=5, side=LEFT) 

        spacerlabel = ttk.Label(terminalfuncframe, text="")
        spacerlabel.pack(padx=223, pady=5, side=LEFT)        

        self.linelabel = ttk.Label(terminalfuncframe, text="000000")
        self.linelabel.config(font=("consolas", 12))
        self.linelabel.pack(padx=5, pady=5, side=LEFT) 

        self.filterbutton = ttk.Button(
            terminalfuncframe, 
            text="Filter", 
            width=13, 
            command=lambda: self.filterWindow()
        )
        self.filterbutton.pack(padx=5, pady=5, side=RIGHT)
        self.filterbutton.config(state="normal")             

        # terminal grid section ----------------------------------------------

        mainframe4 = ttk.Frame(self)
        mainframe4.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')        

        self.terminalbox = Text(mainframe4, width=127, height=31)
        self.terminalbox.config(font=("consolas", 10), undo=True, wrap="word")
        self.terminalbox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.terminalbox.bind("<Button-3>", self.rClicker, add="")

        terminalscrollb = ttk.Scrollbar(mainframe4, command=self.terminalbox.yview)
        terminalscrollb.grid(row=0, column=1, sticky="nsew")
        self.terminalbox["yscrollcommand"] = terminalscrollb.set

        self.master.bind("<Alt-c>", self.clearFunction)
        self.initialize()


    # main functions ---------------------------------------------------

    def hello(self):
        pass       

    def browseFunction(self):
        """ declare the function when pressed on the broswe button """

        fname = askopenfilename(
            filetypes=(
                ("Sim files", "*.JSON"),
                ("Extron Em files", "*.dpro"),
                ("All files", "*.*"),
            )
        )

        path = os.path.dirname(os.path.abspath(fname))
        scriptName = os.path.basename(fname)[:-5]

        if fname:
            try:
                msg = "Loading {}".format(fname)
                self.terminalFunction("--", None, msg)
            except:
                print("Failed to read file\n'%s'" % fname)

        """ Open the simulation json file """
        try:
            with open(fname) as data_file:
                data = json.load(data_file)

                loadedManufacturer = ""
                loadedModel = ""
                loadedPort = 0
                loadedDelay = ""

                if data:
                    self.commandsList = data

                    loadedManufacturer = data[0]["Manufacturer"]
                    loadedModel = data[1]["Model"]
                    loadedPort = data[4]["Port"]
                    loadedDelay = data[5]["Delay"]

                    self.portentry.delete(0, END)
                    self.portentry.insert(0, loadedPort)
                    self.filelabel.config(text="{} - {}".format(loadedManufacturer, loadedModel))

                    msg = "{} - {} loaded with a Response Delay of {}s".format(
                        loadedManufacturer, loadedModel, loadedDelay
                    )
                    self.terminalFunction("--", None, msg)

                    if data[6][
                        "Script"
                    ]:  # If a script is specified then also open that

                        print(scriptName)
                        msg = "Importing Script file: {}.py".format(scriptName)
                        self.terminalFunction("--", None, msg)
                        sys.path.append("{}".format(path))
                        try:
                            self.devscript = __import__(scriptName)
                        except Exception as e:
                            msg = "Script Import Failled: {}.py".format(e)
                            self.terminalFunction("--", None, msg)
                    else:
                        self.devscript = None

                    print(self.commandsList)

        except Exception as e:
            print("Error opening sim file:", e) 
   
    def sendFunction(self):
        """ sends a custom string defined in the code entry field """

        sendbyte = ast.literal_eval(f'b"{self.sendentry.get()}"')

        if self.conn:
            port = self.port["connected"]
            self.terminalFunction("OU", port, sendbyte)
            self.conn.send(sendbyte)

    def disconnectFunction(self):
        """ declare the function when pressed on the disconnect button """

        self.buffer = b""
        if self.conn:
            self.conn.close()
            self.conn = None

    def terminalFunction(self, direction, port, data):
        """ function for printing to the terminal window """

        if self.terminalrunning:
            msgdir = str(direction)
            msgport = str(port)
            now = datetime.datetime.now()
            msgnow = str(now.strftime("%H:%M:%S.%f")[:-3])
            msgdata = str(data)

            if direction == "--":  # info lines
                index = 0  # always show in black
                msg = "{} | {} | {} | {}\n".format(msgdir, msgport, msgnow, msgdata)
                self.terminalbox.tag_config(
                    str(self.colorList[index]), foreground=self.colorList[index]
                )
                self.terminalbox.insert(END, msg, str(self.colorList[index]))
                self.terminalbox.see(END)
            else:  # lines for incoming or outgoing data
                if port == self.port["connected"]:
                    msg = "{} | {} | {} | {}\n".format(
                        msgdir, msgport, msgnow, msgdata
                    )
                    self.terminalbox.tag_config(
                        str(self.colorList[3]),
                        foreground=self.colorList[3],
                    )
                    self.terminalbox.insert(
                        END, msg, str(self.colorList[3])
                    )
                    self.terminalbox.see(END)

        self.terminallengthFunction()

    def terminallengthFunction(self):
        """ displays the total number of lines in the terminal """

        self.linelabel.config(
            text="{:06d}".format(
                int(self.terminalbox.index("end-1c").split(".")[0]) - 1
            )
        )

    def runstopFunction(self, index):
        """ starts/stops/clears the terminal box """

        if index == 1:
            self.terminalrunning = True
        else:
            self.terminalrunning = False

        self.terminallengthFunction()

    def clearFunction(self):
        """ clears the terminal box """

        self.terminalbox.delete(1.0, END)
        self.terminallengthFunction()

    def rClicker(self, e):
        """ right click context menu for all Tk Entry and Text widgets"""

        try:

            def rClick_All(e, apnd=0):
                e.widget.event_generate("<Control-a>")

            def rClick_Copy(e, apnd=0):
                e.widget.event_generate("<Control-c>")

            def rClick_Cut(e):
                e.widget.event_generate("<Control-x>")

            e.widget.focus()

            nclst = [
                (" Select All", lambda e=e: rClick_All(e)),
                (" Cut", lambda e=e: rClick_Cut(e)),
                (" Copy", lambda e=e: rClick_Copy(e)),
            ]

            rmenu = Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")
        except TclError:
            print(" - rClick menu, something wrong")
        return "break"

    def rClickbinder(self, r):
        """ binder for the right click menu """

        try:
            for b in ["Text", "Entry", "Listbox", "Label"]:  #
                r.bind_class(b, sequence="<Button-3>", func=self.rClicker, add="")
        except TclError:
            print(" - rClickbinder, something wrong")














    def listenFunction(self):
        """ gets trigger from Open Port button or the file loader """

        if str(self.portbutton["text"]) == "Open Port":
            if self.commandsList:
                self.portbutton.config(text="Close Port")

                newport = int(self.portentry.get())
                self.port["listen"] = newport

                self.portentry.delete(0, END)
                self.portentry.insert(0, str(self.port["listen"]))
                self.portentry.config(state="disabled")

                mySocket = socket.socket()
                mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                mySocket.bind((self.host, self.port["listen"]))
                mySocket.listen()
                self.socket = mySocket

                Thread(target=self.client_thread).start()

            else:
                msg = "Port not openend, please load a file first!"
                self.terminalFunction("--", None, msg)

        elif str(self.portbutton["text"]) == "Close Port":
            self.portentry.config(state="normal")
            self.portbutton.config(text="Open Port")
            self.socket.close()
            self.port["listen"] = 0

            if self.conn:
                self.buffer = b""
                self.conn.close()
                self.conn = None
                self.socket.close()

    def client_thread(self, action=None):
        """ a threaded function for individual sockets and their connections """

        addr = []

        while self.running:
            if self.conn == None:  # no connection, open a new one

                try:
                    try:
                        self.conn, addr = self.socket.accept()
                        listen = self.socket.getsockname()[1]
                    except:
                        raise

                    if listen == self.port["listen"]:
                        self.port["connected"] = addr[1]

                    self.buffer = b""
                    self.disconnectbutton.config(state="active")
                    
                    if self.devscript:
                        pass

                    msg = "Client {} connected".format(addr[0])
                    self.sendbutton.config(state="enabled")
                    self.colorlabel.config(background=self.colorList[1])
                    self.terminalFunction("--", addr[1], msg)

                    if self.commandsList:
                        if "ON_CONNECT" in self.commandsList[7][0]["Query"]:
                            byteresponse = "{}".format(
                                self.commandsList[7][0]["Response"]
                            )
                            time.sleep(0.25)
                            byteresponsesend = (
                                byteresponse.encode("latin-1")
                                .decode("unicode_escape")
                                .encode("latin-1")
                            )
                            self.terminalFunction("OU", addr[1], byteresponsesend)
                            try:
                                self.conn.send(byteresponsesend)
                            except:
                                print('Error sending bytes')
                except:
                    raise

            else:  # a connection exists
                try:
                    self.buffer = self.conn.recv(1024)
                except ConnectionAbortedError:
                    self.terminalFunction("--", addr[1], "Disconnecting")
                except OSError as o:
                    print("OSError", o)
                finally:
                    if not self.buffer:
                        self.disconnectbutton.config(state="disabled")
                        if addr:
                            msg = "Client {} disconnected".format(addr[0])
                            self.sendbutton.config(state="disabled")
                            self.colorlabel.config(background=self.colorList[0])
                            self.terminalFunction("--", addr[1], msg)

                        if self.conn:
                            self.conn.close()
                            self.conn = None
                    else:
                        if addr:
                            self.terminalFunction(
                                "IN", addr[1], str(self.buffer)
                            )
                            self.data_function(addr[1], self.buffer)

    def data_function(self, port, data):
        """ function to return data via script or json responses """

        self.idx = 0

        if self.commandsList:
            result = any(
                str(x["Query"])
                .encode("latin-1")
                .decode("unicode_escape")
                .encode("latin-1")
                == data
                for self.idx, x in enumerate(self.commandsList[7])
            )

            if result:  # command found in query
                delay = float(self.commandsList[5]["Delay"])
                byteresponse = "{}".format(
                    self.commandsList[7][self.idx]["Response"]
                )
                time.sleep(delay)
                byteresponsesend = (
                    byteresponse.encode("latin-1")
                    .decode("unicode_escape")
                    .encode("latin-1")
                )
                self.terminalFunction("OU", port, byteresponsesend)
                try:
                    self.conn.send(byteresponsesend)
                except:
                    pass
            else:  # command not found in query, trying script

                if self.devscript:  # invoke the script (if there is one)
                    try:
                        byteresponse = self.devscript.rxscript(
                            self.conn, self.buffer
                        )
                    except Exception as e:
                        print('Exception occured in devscript', e)

                    if byteresponse:
                        byteresponsesend = (
                            byteresponse.encode("latin-1")
                            .decode("unicode_escape")
                            .encode("latin-1")
                        )
                        self.conn.send(byteresponsesend)
                        self.terminalFunction("OU", port, byteresponsesend)
                    else:  # Nothing found in query or script
                        byteresponse = "Error - no match found in query or script"
                        self.terminalFunction("ER", port, byteresponse)
                        try:
                            self.conn.send(bytes(byteresponse, "utf-8"))
                        except Exception as e:
                            print('Exception occured in sending', e)

                else:  # Nothing found in query
                    byteresponse = "Error - no match found with query"
                    self.terminalFunction("ER", port, byteresponse)
                    self.conn.send(bytes(byteresponse, "utf-8"))
        else:
            self.terminalFunction(
                "--", port, "Error - no device emulator file has been loaded"
            )  

    def initialize(self):
        """ initialization of main objects """

        self.host = ""
        self.port = {"listen": 0, "connected": 0}

        self.conn = None
        self.buffer = None
        self.socket = None

        self.running = True

def on_closing():
    """ closes the main window and kills the proces / task """

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