"""
    #PEA

    PEA is a Python Emulator for Audiovisual devices written to aid
    in the develpment and testing of Audiovisual control projects.

    Code by: 
        Alex Teusch - alexander.teusch@gmail.com
        Rupert Powell - rupert@astronoscope.eu

    Version controlled here:
        https://github.com/clydefrog76/pea
"""

from threading import Thread
import tkinter.ttk as ttk
from tkinter import Tk, messagebox, Text, Frame, Menu, PhotoImage, BOTH, LEFT, RIGHT, END, TOP, BOTTOM, Toplevel, StringVar, TclError
from tkinter.filedialog import askopenfilename
import os, socket, sys, json, time, ast, datetime, binascii

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
        self.colorList = ["#FF0000", "#00FF00", "#DDEEFF", "#009900", "#000099"]
        self.terminalrunning = True
        self.commandsList = None
        self.devscript = None

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
        menubar.add_cascade(label="Edit", menu=editmenu)        

        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="ASCII - HEX Conversion", command=lambda: self.asciihexWindow())
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

        sendframe = ttk.LabelFrame(mainframe2, text="Send Quick Command",)
        sendframe.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        sendlabel = ttk.Label(sendframe, text="String")
        sendlabel.pack(padx=5, pady=5, side=LEFT)
        self.sendentry = ttk.Entry(sendframe, width=50)
        self.sendentry.insert(0, "Replace this with ASCII or HEX bytes with prefix \\x")
        self.sendentry.bind("<Button-1>", self.sendentry_click)
        self.sendentry.bind("<FocusIn>", self.sendentry_click)
        self.sendentry.pack(padx=5, pady=5, side=LEFT)        
        self.sendbutton = ttk.Button(sendframe,
            text="Send", width=13,
            command=lambda: self.sendFunction(),
        )
        self.sendbutton.pack(padx=5, pady=5, side=LEFT)

        scriptframe = ttk.LabelFrame(mainframe2, text="Script Function Buttons",)
        scriptframe.grid(row=0, column=1, padx=8, pady=8, sticky='nsew')
        self.scriptbutton1 = ttk.Button(scriptframe,
            text="Func 1", width=11,
            command=lambda i=1: self.callCustomFunc(i),
        )
        self.scriptbutton1.pack(padx=5, pady=5, side=LEFT)
        self.scriptbutton2 = ttk.Button(scriptframe,
            text="Func 2", width=11,
            command=lambda i=2: self.callCustomFunc(i),
        )
        self.scriptbutton2.pack(padx=5, pady=5, side=LEFT)
        self.scriptbutton3 = ttk.Button(scriptframe,
            text="Func 3", width=11,
            command=lambda i=3: self.callCustomFunc(i),
        )
        self.scriptbutton3.pack(padx=5, pady=5, side=LEFT)
        self.scriptbutton4 = ttk.Button(scriptframe,
            text="Func4", width=11,
            command=lambda i=4: self.callCustomFunc(i),
        )
        self.scriptbutton4.pack(padx=5, pady=5, side=LEFT)
        self.scriptbutton5 = ttk.Button(scriptframe,
            text="Func 5", width=11,
            command=lambda i=5: self.callCustomFunc(i),
        )
        self.scriptbutton5.pack(padx=5, pady=5, side=LEFT)                              

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

                    if data[6]["Script"]:  # If a script is specified then also open that
                        msg = "Importing Script file: {}.py".format(scriptName)
                        self.terminalFunction("--", None, msg)
                        sys.path.append("{}".format(path))
                        try:
                            self.devscript = __import__(scriptName)
                        except Exception as e:
                            msg = "Script import failed: {}.py".format(e)
                            self.terminalFunction("--", None, msg)
                    else:
                        self.devscript = None
        except Exception as e:
            print("Error opening sim file:", e) 

    def disconnectFunction(self):
        """ declare the function when pressed on the disconnect button """

        self.buffer = b""
        if self.conn:
            self.conn.close()
            self.conn = None

    def sendentry_click(self, event):
        if self.sendentry.get() == "Replace this with ASCII or HEX bytes with prefix \\x":
            event.widget.delete(0, END)

    def sendFunction(self):
        """ sends a custom string defined in the code entry field """

        if self.sendentry.get() != "Replace this with ASCII or HEX bytes with prefix \\x":
            sendbyte = ast.literal_eval(f'b"{self.sendentry.get()}"')

            if self.conn:
                port = self.port["connected"]
                self.terminalFunction("OU", port, sendbyte)
                self.conn.send(sendbyte)
            else:
                msg = "No TCP connection detected"
                self.terminalFunction("--", None, msg)            

    def callCustomFunc(self, func):
        """ sends a custom data function """

        byteresponse = None
        
        if self.devscript:
            try:
                byteresponse = self.devscript.customFunc(func)
            except Exception as e:
                print('Exception occured in customFunc', e)            

            if byteresponse and self.conn:
                byteresponsesend = (
                    byteresponse.encode("latin-1")
                    .decode("unicode_escape")
                    .encode("latin-1")
                )

                port = self.port["connected"]
                self.terminalFunction("OU", port, byteresponsesend)
                self.conn.send(byteresponsesend)
            else:
                msg = "No TCP connection detected"
                self.terminalFunction("--", None, msg)                           
        else:
            msg = "No script functions are loaded"
            self.terminalFunction("--", None, msg)                      

    def terminalFunction(self, direction, port, data):
        """ function for printing to the terminal window """

        if self.terminalrunning:
            msgdir = str(direction)
            #msgport = str(port)
            now = datetime.datetime.now()
            msgnow = str(now.strftime("%H:%M:%S.%f")[:-3])
            msgdata = str(data)

            if direction == "--":  # info lines
                color = 0
                msg = "{} | {} | {}\n".format(msgdir, msgnow, msgdata)
                self.terminalbox.tag_config(
                    str(self.colorList[color]), foreground=self.colorList[color]
                )
                self.terminalbox.insert(END, msg, str(self.colorList[color]))
                self.terminalbox.see(END)
            else:  # lines for incoming or outgoing data
                if port == self.port["connected"]:
                    if direction == "IN":
                        color = 3                    
                    else:
                        color = 4
                    msg = "{} | {} | {}\n".format(msgdir, msgnow, msgdata)
                    self.terminalbox.tag_config(str(self.colorList[color]), foreground=self.colorList[color])
                    self.terminalbox.insert(END, msg, str(self.colorList[color]))
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

    def filterWindow(self):
        """ opens a new filter window """

        self.filterbutton.config(state="disabled")

        def on_filterclosing():
            """ kills the filter window """

            self.filterbutton.config(state="normal")
            filterWindow.destroy()

        filterWindow = Toplevel()
        filterWindow.wm_title("Filter")
        filterWindow.pack_propagate(True)
        filterWindow.protocol("WM_DELETE_WINDOW", on_filterclosing)

        functionframe = ttk.LabelFrame(filterWindow, text="Filter Setup")
        functionframe.pack(fill=BOTH, padx=5, pady=5, side=TOP)

        resetfilterbutton = ttk.Button(
            functionframe, text="Reset", width=10, command=self.resetfilterFunction
        )
        resetfilterbutton.pack(padx=5, pady=5, side=LEFT)

        self.filterentry1 = ttk.Entry(functionframe, width=49)
        self.filterentry1.insert(0, "")
        self.filterentry1.pack(padx=5, pady=5, side=LEFT)

        self.filtervar = StringVar()
        filteroptions = ["AND", "OR"]
        self.filterword = ttk.OptionMenu(
            functionframe, self.filtervar, filteroptions[0], *filteroptions
        )
        self.filterword.config(width=7)
        self.filterword.pack(padx=5, pady=5, side=LEFT)

        self.filterentry2 = ttk.Entry(functionframe, width=49)
        self.filterentry2.insert(0, "")
        self.filterentry2.pack(padx=5, pady=5, side=LEFT)

        refreshbutton = ttk.Button(
            functionframe, text="Apply", width=10, command=self.refreshFunction
        )
        refreshbutton.pack(padx=5, pady=5, side=LEFT)

        filterframe = ttk.LabelFrame(filterWindow, text="Filtered Terminal")
        filterframe.pack(fill=BOTH, padx=5, pady=5, side=BOTTOM)

        self.filterbox = Text(filterframe, width=120, height=20)
        self.filterbox.config(font=("consolas", 10), undo=True, wrap="word")
        self.filterbox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.filterbox.bind("<Button-3>", self.rClicker, add="")

        filterscrollb = ttk.Scrollbar(filterframe, command=self.filterbox.yview)
        filterscrollb.grid(row=0, column=1, sticky="nsew")
        self.filterbox["yscrollcommand"] = filterscrollb.set

        filterWindow.resizable(width=False, height=False)

        self.refreshFunction()   

    def resetfilterFunction(self):
        """ clears the filter entry field """

        self.filterentry1.delete(0, END)
        self.filterentry2.delete(0, END)
        self.filtervar.set("AND")
        self.refreshFunction()

    def refreshFunction(self):
        """ refresh the filter box """

        self.filterbox.delete(1.0, END)

        filterword1 = self.filterentry1.get()
        filterword2 = self.filterentry2.get()

        if len(filterword1) > 0 and len(filterword2) == 0:
            for line in self.terminalbox.get("1.0", "end-1c").splitlines():
                if filterword1 in line:
                    self.filterbox.insert(END, "{}\n".format(line))
        elif len(filterword1) > 0 and len(filterword2) > 0:
            for line in self.terminalbox.get("1.0", "end-1c").splitlines():
                if self.filtervar.get() == "AND":
                    if filterword1 in line and filterword2 in line:
                        self.filterbox.insert(END, "{}\n".format(line))
                elif self.filtervar.get() == "OR":
                    if filterword1 in line or filterword2 in line:
                        self.filterbox.insert(END, "{}\n".format(line))
        else:
            for line in self.terminalbox.get("1.0", "end-1c").splitlines():
                self.filterbox.insert(END, "{}\n".format(line))

    def listenFunction(self):
        """ gets trigger from Open Port button or the file loader """

        if str(self.portbutton["text"]) == "Open Port":
            if self.commandsList:
                self.portbutton.config(text="Close Port")
                
                newport = int(self.portentry.get())
                self.port["listen"] = newport

                msg = "Port {} is open".format(newport)
                self.terminalFunction("--", None, msg)

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
            msg = "Port is closed"
            self.terminalFunction("--", None, msg)            

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
                    self.conn, addr = self.socket.accept()
                    listen = self.socket.getsockname()[1]
                except:
                    raise

                if listen == self.port["listen"]:
                    self.port["connected"] = addr[1]

                self.buffer = b""
                self.disconnectbutton.config(state="active")

                msg = "Client {} connected".format(addr[0])
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

    def asciihexWindow(self):
        """ opens a new ASCII HEX window """
         
        def on_asciihexclosing():
            """ kills the ASCII HEX window """

            asciihexWindow.destroy()

        def asciihexFunction():
            hexvar = "".join("{:02x}".format(ord(c)) for c in asciientry.get())
            hexoutput.delete(0, END)
            hexoutput.insert(0, hexvar)   

        def hexasciiFunction():
            if len(hexentry.get()) in range(2,200,2):
                asciivar = binascii.unhexlify(hexentry.get())
                asciioutput.delete(0, END)
                asciioutput.insert(0, asciivar)                   

        asciihexWindow = Toplevel()
        asciihexWindow.wm_title("ASCII - HEX Conversion")
        asciihexWindow.pack_propagate(True)
        asciihexWindow.protocol("WM_DELETE_WINDOW", on_asciihexclosing)

        convframe1 = ttk.LabelFrame(asciihexWindow, text="ASCII to HEX",)
        convframe1.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')       
        asciientry = ttk.Entry(convframe1, width=20, justify='center')
        asciientry.pack(padx=5, pady=5, side=LEFT) 
        hexoutput = ttk.Entry(convframe1, width=20, justify='center')
        hexoutput.pack(padx=5, pady=5, side=LEFT) 
        convbutton1 = ttk.Button(convframe1,
            text="Convert", width=13,
            command=lambda: asciihexFunction(),
        )
        convbutton1.pack(padx=5, pady=5, side=LEFT)       

        convframe2 = ttk.LabelFrame(asciihexWindow, text="HEX to ASCII",)
        convframe2.grid(row=1, column=0, padx=8, pady=8, sticky='nsew')       
        hexentry = ttk.Entry(convframe2, width=20, justify='center')
        hexentry.pack(padx=5, pady=5, side=LEFT) 
        asciioutput = ttk.Entry(convframe2, width=20, justify='center')
        asciioutput.pack(padx=5, pady=5, side=LEFT) 
        convbutton2 = ttk.Button(convframe2,
            text="Convert", width=13,
            command=lambda: hexasciiFunction(),
        )
        convbutton2.pack(padx=5, pady=5, side=LEFT)                   

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