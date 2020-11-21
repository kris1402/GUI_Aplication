import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import *
import pyodbc
from time import sleep,time
from threading import Thread
import socket
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import time
############
import requests
from PIL import Image, ImageTk
#############
from matplotlib import style
from tkinter import font
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
from datetime import datetime
from matplotlib import style
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


import snap7.client as c
from snap7.util import *
from snap7.snap7types import *

def ReadMemory(plc,byte,bit,datatype):
    result = plc.read_area(areas['MK'],0,byte,datatype)
    if datatype==S7WLBit:
        return get_bool(result,0,bit)
    elif datatype==S7WLByte or datatype==S7WLWord:
        return get_int(result,0)
    elif datatype==S7WLReal:
        return get_real(result,0)
    elif datatype==S7WLDWord:
        return get_dword(result,0)
    else:
        return None

def WriteMemory(plc,byte,bit,datatype,value):
    result = plc.read_area(areas['MK'],0,byte,datatype)
    if datatype==S7WLBit:
        set_bool(result,0,bit,value)
    elif datatype==S7WLByte or datatype==S7WLWord:
        set_int(result,0,value)
    elif datatype==S7WLReal:
        set_real(result,0,value)
    elif datatype==S7WLDWord:
        set_dword(result,0,value)
    plc.write_area(areas["MK"],0,byte,result)


LARGE_FONT= ("Verdana", 10)
style.use("dark_background")

f = Figure(figsize = (2, 5), dpi = 75)
ax1 = f.add_subplot(111)
#ax2 = f1.add_subplot(212)
def Graph(i):

        """DinamiPlot"""
        graph_data = open('Zeszyt1.csv','r').read()
        lines = graph_data.split('\n')
        #xs = []
        ys = []
        y1 = []
        y2 = []
        for line in lines:
            if len(line) > 1:
                #x, y = line.split(',')
                y = line
                #xs.append(float(x))
                ys.append(float(y))
                y1.append(46)
                y2.append(51)
        ax1.clear()
        ax1.plot(ys,linewidth=3)
        ax1.plot(y1,'lime', linestyle='dotted', linewidth=2)
        ax1.plot(y2, 'lime', linestyle='dotted', linewidth=2)
        ax1.set_ylabel('Wyniki Pomiarów')
        ax1.set_xlabel('Unit[]')
        ax1.set_title('Wykres pomiarów')
        #ani = animation.FuncAnimation(fig, Graph, interval=1000)
        #plt.show(ani)
        """DinamiPlot"""

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.running = 0
        self.addr = None
        self.conn = None
        self.t = tk.Text
        self.t_1 = tk.Text
        self.e = tk.Entry
        self.p_e = tk.Entry
        #self.foo = tk.StringVar()
        #self.var = IntVar()
        self.geometry("510x450")
        self.resizable(width=FALSE, height=FALSE)
        #canvas = tk.Canvas(self, height = 550, width = 470)
        #canvas.pack()
        #self.iconbitmap('C:/Users/michal.koscisz/PycharmProjects/Projekt_int_3/icon1.ico')
        self.title('SAM dev app by KK ')
        self.iconbitmap(r'icon.ico')
        #self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        #self.show_frame("PageOne")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def naccheck(self, entry_3, entry_4, var):
        #var = tk.IntVar()
        print("check")
        if var.get() == 1:
            print("gdy 1 "+str(var.get()))
            entry_3.configure(state='disabled')
            entry_4.configure(state='disabled')
        else:
            print("gdy 0 "+str(var.get()))
            entry_3.configure(state='normal')
            entry_4.configure(state='normal')

    def connection_string(self,entry_1, entry_2, entry_3, entry_4, var):
        #self.server = str(entry_1.get())
        self.driver = '{SQL Server}'
        #self.server = 'LAP-SSEWERY'
        self.server = str(entry_1.get())
        self.db = str(entry_2.get())#'Test'
        self.uid = str(entry_3.get())
        self.pwd = str(entry_4.get())

        print(str(var.get()))
        print(self.server)
        print(self.db)

        if var.get() == 1:
            """self.connnection = pyodbc.connect('Driver={SQL Server};'
                                              'Server=LAP-SSEWERY;'
                                              #'Server=self.server;'
                                              'Database=Test;'
                                              'Trusted_Connection=yes;')"""
            self.connnection = pyodbc.connect(driver=self.driver,
                                              server=self.server,
                                              database=self.db,
                                              trusted_connection='yes')
            self.cursor = self.connnection.cursor()
            print(self.server)
            print(self.db)
            print("trusted_connection='yes'")
        else:
            self.connnection = pyodbc.connect(driver=self.driver,
                                              server=self.server,
                                              database=self.db,
                                              uid=self.uid,
                                              pwd=self.pwd)
                                              #trusted_connection='yes')
            self.cursor = self.connnection.cursor()
            print(self.server)
            print(self.db)
            print(self.uid)
            print("password")

    def socket_thread(self):
        print("thread started..")
        self.ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port =  int(self.p_e.get())#str(self.e.get()) int(self.p_e.get())9999
        self.ls.bind(('', port))
        print("Server listening on port %s" %port)
        self.ls.listen(1)
        self.ls.settimeout(5)
        self.conn=None
        while self.running != 0:
            if self.conn is None:
                try:
                    (self.conn, self.addr) = self.ls.accept()
                    print("client is at", self.addr[0], "on port", self.addr[1])
                    #self.connection_l.configure(text="CONNECTED!")
                except (socket.timeout):#,e):
                    print ("Waiting for Connection...")
                except (Exception):#,e):
                    print("Connect exception: ")#+str(e) )
            if self.conn != None:
                print ("connected to "+str(self.conn)+","+str(self.addr))
                self.conn.settimeout(5)
                self.rc = ""
                connect_start = time() # actually, I use this for a timeout timer
                while self.rc != "done":
                    self.rc=''
                    try:
                        self.rc = self.conn.recv(1024).decode()
                        self.data = str(self.rc)
                        #self.data = (self.clientsocket.recv(1024).decode())
                        self.data_1 = float(self.data)

                    except (Exception):#, e):
                        # we can wait on the line if desired
                        print ("socket error: ")#+repr(e))
                    if len(self.rc):
                        print("got data", self.rc)
                        print("A float to: ", self.data_1 + 1.0) #Moja modyfikacja
                        #self.conn.send("got data.\n")
                        self.t.insert('end', str(self.rc))
                        connect_start=time()  # reset timeout time
                    elif (self.running==0) or (time()-connect_start > 30):
                        print ("Tired of waiting on connection!")
                        self.rc = "done"
                print ("closing connection")
                #self.connection_l.configure(text="not connected.")
                self.conn.close()
                self.conn=None
                print ("connection closed.")
        print ("closing listener...")
        # self running became 0
        self.ls.close()
    def startc(self):
        if self.running == 0:
            print ("Starting thread")
            self.running = 1
            self.thread=Thread(target=self.socket_thread)
            self.thread.start()
        else:
            print ("thread already started.")
    def stopc(self):
        if self.running:
            print ("stopping thread...")
            self.running = 0
            self.thread.join()
        else:
            print ("thread not running")
    def sendtoserv(self):
        if  self.running:
            self.current = str(self.e.get())
            self.t_1.insert('end', str(self.current))
            self.conn.send(bytes(self.current, encoding='utf8'))#"Witaj", encoding='utf8'))
            self.e.delete(0, END)
        else:
            print("Blad wysylu danych")



    def inserttotable(self):
        self.cursor.execute('SELECT * FROM [Test_1].[dbo].[Dane_z_aplikacji]')
        #self.cursor.execute("INSERT INTO [Test].[dbo].[Dane_z_aplikacji] (Dane_z_portu) VALUES (?)", self.data)   #'SELECT * FROM db_name.Table')
        #cursor.execute("insert into products(id, name) values ('pyodbc', 'awesome library')")
        self.cursor.execute("INSERT INTO [Test_1].[dbo].[Dane_z_aplikacji] (ID_Referencji, ID_Stacji, Pomiar, DATA, Status) VALUES (?,?,?,?,?)",(2, 1, self.data_1, datetime.now(), 'OK'))
        self.cursor.commit()
        #'INSERT INTO [dbo].[Dane z aplikacji] VALUES (self.rc)'

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        #controller.var = IntVar()
        #controller.geometry("310x230")

        ##pyodbc
        var = IntVar()

        ##FRAME

        Frame_1 = tk.LabelFrame(self, text="SQL Server", bg="gray30",fg="white",height=10)
        Frame_1.pack(fill="both", expand=True, pady=(97, 0), padx=(2,2))

        Frame_2 = tk.LabelFrame(self, bg="gray30")
        Frame_2.pack(fill="both",  expand=True, pady=(2, 0),padx=(2,2))

        img = Image.open('1.png')
        print(img.size)
        self.tkimage = ImageTk.PhotoImage(img)
        label = tk.Label(self, text="Connect to server", font=controller.title_font,width=35, height=3,bg="gray94",anchor="n")#,borderwidth=5, relief="raised
        label.place(relx=0,rely=0)
        label1 = tk.Label(self, image = self.tkimage)
        label1.place( relx=0.1, rely=0.008)
        labelCanvas = tk.Canvas(self, height=510, width=450,bg="gray94")

        ###FOR DATABASE CONNECTION FRAME_1
        l_sname = tk.Label(Frame_1, text="Server name: ",borderwidth=4,relief="groove", font=("Arial",11), width=11, height=1,fg="dark slate gray")
        l_sname.place(x=118, y=24)

        l_dname = tk.Label(Frame_1, text="Database: ",borderwidth=4,relief="groove", font=("Arial", 11), width=11, height=1,fg="dark slate gray")
        l_dname.place(x=118, y=48)

        l_uname = tk.Label(Frame_1, text="User name: ",borderwidth=4,relief="groove", font=("Arial", 11), width=11, height=1,fg="dark slate gray")
        l_uname.place(x=118, y=72)

        l_pname = tk.Label(Frame_1, text="Password: ",borderwidth=4,relief="groove", font=("Arial", 11), width=11, height=1,fg="dark slate gray")
        l_pname.place(x=118, y=96)

        entry_1 = Entry(Frame_1, width=25, borderwidth=3)
        entry_1.place(x=225, y=24)

        entry_2 = Entry(Frame_1, width=25, borderwidth=3)
        entry_2.place(x=225, y=48)

        entry_3 = Entry(Frame_1, width=25, borderwidth=3)#, state='normal')
        entry_3.place(x=225, y=72)

        entry_4 = Entry(Frame_1, width=25, borderwidth=3, show="*")
        entry_4.place(x=225, y=96)

        ck1 = Checkbutton(Frame_1, text='Windows Authentication',variable=var, command= lambda e_3=entry_3, e_4 = entry_4, v = var: controller.naccheck(e_3, e_4, v),fg="OrangeRed4")
        ck1.place(x=225, y=120)

        ##FRAME_2

        Connect_b = tk.Button(Frame_2, text="Connect", command=lambda e_1=entry_1, e_2=entry_2, e_3=entry_3, e_4=entry_4, v = var: controller.connection_string(e_1, e_2, e_3, e_4, v),fg="#290000",bg="#A8A8A8",width="10", height="2",activebackground="red")
        Connect_b.place(x=100,y=0)

        to_p_1_b = tk.Button(Frame_2, text="Skip to page one", command=lambda: controller.show_frame("PageOne"),fg="#290000",bg="#A8A8A8",width="22", height="2")
        to_p_1_b.place(x=250, y=0)

        Cancel_b = tk.Button(Frame_2, text="Cancel", command=lambda: controller.show_frame("PageOne"),fg="#290000",bg="#A8A8A8",width="10", height="2")
        Cancel_b.place(x=180, y=0)





class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #controller.geometry("510x400")

        ##POLOZENIE ELEMENTOW W APLIKACJI

        ##LABEL
        #l_1 = tk.Label(self, text="", bg="light grey",height=-10)
        #l_1.pack(fill="both", expand=True, pady=(0,0))

        #l_1 = tk.Frame(self,bg="light grey")
        #l_1.pack(fill="both", expand=True,pady=(0,0))

        ####LABEL FRAMES
        # lF = tk.LabelFrame(self,bg="blue")
        # lF.pack(fill="both", expand=True)

        lF_2 = tk.LabelFrame(self, bg="gray94")
        lF_2.pack(fill="both", expand=True,pady=(0, 0))

        lF_3 = tk.LabelFrame(lF_2,  bg="gray30",borderwidth=5, relief="raised")#, height=100)
        lF_3.pack(fill="both", expand=True, pady=(30, 0))

        #lF_6 = tk.LabelFrame(lF_3, text="Ramka obok", bg="green")
        #lF_6.pack(fill="both", expand=True, pady=(0, 0), padx=(0, 180))

        lF_4 = tk.LabelFrame(lF_3, text="TCP Options", bg="gray30",height=310, fg="white")
        lF_4.pack(fill="both", expand=True, padx=(330, 10), pady=(0, 0))

        lF_5 = tk.LabelFrame(lF_3, text="Send Data", bg="gray94",fg="black")
        lF_5.pack(fill="both", expand=True,pady=(0,0), padx=(0, 0))#, pady=(120, 40))



        ####BUTTONS
        b_33 = tk.Button(lF_2, text='Prev ', command=lambda: controller.show_frame("StartPage"), fg="black",
                         bg="grey80", width="10", height="1", highlightthickness=2)
        b_33.place(x=3, y=0)
        b_4 = tk.Button(lF_2, text='Menu ',command=lambda: controller.show_frame("StartPage"),fg="black",bg="grey80",width="10", height="1",highlightthickness=2)
        b_4.place(x=86, y=0)

        b = tk.Button(lF_2, text='Next', command=lambda: controller.show_frame("PageTwo"),fg="black",bg="grey80",width="10",highlightthickness=2)
        b.place(x=169, y=0)

        button1 = tk.Button(lF_3, text="Go to Page One", command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(lF_3, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
        #button1.place(x=110, y=220)
        #button2.place(x=205, y=220)

        przycisk = tk.Button(lF_5, text="Send", width=20,fg="orange4",bg="gray10",highlightthickness=3,highlightcolor="red", command=controller.sendtoserv,
                      #highlightbackground="#37d3ff",
                      borderwidth=3)
        # self.przycisk.pack(side="bottom")
        przycisk.place(x=330,y=-3)

        #b2 = tk.Button(lF_3, text="Listen", width=10, command=controller.startc)


        b3 = tk.Button(lF_4, text="Stop Listening", width=20,borderwidth=3,fg="orange4",bg="gray10", command=controller.stopc)
        b3.place(x=3, y=60)

        b3 = tk.Button(lF_4, text="Insert Data to DB", width=20,borderwidth=3,fg="orange4",bg="gray10", command=controller.inserttotable)
        b3.place(x=3, y=120)

        b10 = tk.Button(lF_4, text="Download From DB", width=20,borderwidth=3,fg="orange4",bg="gray10", command=controller.stopc)
        b10.place(x=3, y=155)

        ###TEKST
        controller.t = tk.Text(lF_3, height=9, width=40,bd=3,bg="gray50",fg="red")#, pady=5)
        controller.t.place(x=0, y=20)


        controller.t_1 = tk.Text(lF_3, height=9, width=40, pady=5,bd=3,bg="gray50",fg="red")
        controller.t_1.place(x=0, y=200)



        ##ENTRY
        controller.e = Entry(lF_5, width=53, borderwidth=3,bg="gray50")
        controller.e.place(x=0, y=1)

        controller.p_e = Entry(lF_4, width=10, borderwidth=3,bg="gray50")
        controller.p_e.place(x=0, y=24)

        b2 = tk.Button(lF_4, text="Listen", width=10,borderwidth=3,fg="orange4",bg="gray10",command= controller.startc)
        b2.place(x=70, y=22)

        ####LABEL
        #label = tk.Label(lF_2, text="This is the start page", bg="light blue", font=controller.title_font)
        #label.place(x=0, y=40)

        label = tk.Label(lF_4, text="Port", font=("Arial", 10), bg="gray10",fg="white", width=8, borderwidth=2, relief="groove")
        label.place(x=0, y=0)

        l_2 = tk.Label(lF_3, text="Sended Data", font=("Font.TLabelframe", 9), bg="grey30", fg="white")  # , width=35)
        l_2.place(x=5, y=175)

        l_2 = tk.Label(lF_3, text="Received Data", font=("Font.TLabelframe", 9), bg="grey30", fg="white")  # , width=35)
        l_2.place(x=5, y=0)

        # can = tk.Canvas(frame_3, width=250, height=40, bg="#F0F0F0",highlightbackground="black")  # , highlightbackground="black",bd=None)
        # can.place(x=0, y=0)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lF_23 = tk.LabelFrame(self, bg="gray94")
        lF_23.pack(fill="both", expand=True, pady=(0, 0))

        lF_31 = tk.LabelFrame(lF_23, bg="gray30", borderwidth=5, relief="raised")  # , height=100)
        lF_31.pack(fill="both", expand=True, pady=(30, 0))
        #center gry
        Frame_2_3 = tk.LabelFrame(lF_31, bg="grey60",text="Control")
        Frame_2_3.pack(fill="both", expand=True, pady=(80, 0), padx=(2, 2))
        #center row1
        Frame_2_5 = tk.LabelFrame(Frame_2_3, bg="grey50")
        Frame_2_5.pack(fill="both", expand=True, pady=2, padx=2)
        Frame_2_6 = tk.LabelFrame(Frame_2_3, bg="grey50")
        Frame_2_6.pack(fill="both", expand=True, pady=2, padx=2)
        Frame_2_7 = tk.LabelFrame(Frame_2_3, bg="grey50")
        Frame_2_7.pack(fill="both", expand=True, pady=2, padx=2)

        IF_32 = tk.LabelFrame(lF_31, bg="red",borderwidth=5, relief="raised")
        IF_32.place(relx=5, rely=5)

        Frame_2_4 = tk.LabelFrame(lF_31, bg="grey60", text="Option")
        Frame_2_4.pack(fill="both", expand=True, pady=(10, 10), padx=(2, 2))

        # lF_6 = tk.LabelFrame(lF_3, text="Ramka obok", bg="green")
        # lF_6.pack(fill="both", expand=True, pady=(0, 0), padx=(0, 180))

        #lF_41 = tk.LabelFrame(lF_31, text="TCP Options", bg="red", height=310, fg="white")
        #lF_41.pack(fill="both", expand=True, padx=(330, 10), pady=(0, 0))

        #lF_51 = tk.LabelFrame(lF_31, bg="gray94", fg="black")
        #lF_51.pack(fill="both", expand=True, pady=(0, 0), padx=(0, 0))  # , pady=(120, 40))

        b_41 = tk.Button(lF_23, text='Menu ', command=lambda: controller.show_frame("StartPage"), fg="black",
                        bg="grey80", width="10", height="1", highlightthickness=2)
        b_41.place(x=86, y=0)
        b_42 = tk.Button(lF_23, text='Prev ', command=lambda: controller.show_frame("PageOne"), fg="black",
                         bg="grey80", width="10", height="1", highlightthickness=2)
        b_42.place(x=3, y=0)

        #PAge Threee
        b_43 = tk.Button(lF_23, text="Next", command=lambda: controller.show_frame("PageThree"),
                             fg="black", bg="grey80", width="10", height="1", highlightthickness=2)
        b_43.place(x=169, y=0)


        #label = tk.Label(lF_31, text="Panel\n Operatorski", font=('Courier',22),bg="grey30",fg="black")
        #label.place(relx=0.5,rely=0.1, anchor="center")

        #labelka pod przycisk
        Frame_3_1 = tk.LabelFrame(lF_31, bg="grey50")
        Frame_3_1.place(relx=0, rely=0,relheight=0.19, relwidth=0.49)

        Frame_3_2 = tk.LabelFrame(lF_31, bg="grey30")
        Frame_3_2.place(relx=0.5, rely=0, relheight=0.19, relwidth=0.27)

        Frame_3_3 = tk.LabelFrame(lF_31, bg="grey50")
        Frame_3_3.place(relx=0.78, rely=0, relheight=0.19, relwidth=0.21)
#Przycisk configuration
        size = int(Frame_3_2.winfo_height()*50)
        print(Frame_3_2.winfo_height())
        #img = ImageTk.PhotoImage(Image.open('HMI.png').resize((size, size)))
        img = Image.open('HMI.png')
        img = img.resize((30,28), Image.ANTIALIAS)
        self.pic = ImageTk.PhotoImage(img)
        #self.tkimage = ImageTk.PhotoImage(img)
        label1 = tk.Label(Frame_3_2, image=self.pic, bg="grey50")
        btn = Button(Frame_3_2,text="Config",image=self.pic, compound="bottom",bg="grey50")
        btn.place(relx=0.35, rely=0)
#chart Button
        img2 = Image.open('chart.png')
        img2 = img2.resize((38, 28), Image.ANTIALIAS)
        self.pic2 = ImageTk.PhotoImage(img2)
        # self.tkimage = ImageTk.PhotoImage(img)
        label1 = tk.Label(Frame_3_2, image=self.pic2, bg="grey50")
        btn2 = Button(Frame_3_2, text="Chart", image=self.pic2, compound="bottom", bg="grey50")
        btn2.place(relx=0, rely=0)
#chart mail
        img4 = Image.open('mail.png')
        img4 = img4.resize((32, 28), Image.ANTIALIAS)
        self.pic4 = ImageTk.PhotoImage(img4)
        # self.tkimage = ImageTk.PhotoImage(img)
        label1 = tk.Label(Frame_3_2, image=self.pic4, bg="grey50")
        btn4 = Button(Frame_3_2, text="Mail", image=self.pic4, compound="bottom", bg="grey50")
        btn4.place(relx=0.7, rely=0)
# Label
        label_1 = tk.Label(Frame_3_2, text='More options',compound="bottom", bg="grey30")
        label_1.place(relx=0.2, rely=0.73)

        #----------------weather---------------
#weather and labe;
        def format_response(weather_json):
            try:
                city = weather_json['name']
                conditions = weather_json['weather'][0]['description']
                temp = weather_json['main']['temp']
                final_str = 'City: %s \nConditions: %s \nTemperature (°C): %s' % (city, conditions, temp)
            except:
                final_str = 'There was a problem retrieving that information'
            # final_str = 'hello'
            return final_str

        def get_weather(city):
            weather_key = '16344ab7408758e805713bfdc9c5bf8f'
            url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {'APPID': '16344ab7408758e805713bfdc9c5bf8f', 'q': city, 'units': 'metric'}
            response = requests.get(url, params=params)
            print(response.json())
            weather_json = response.json()
            results['text'] = format_response(response.json())
            icon_name = weather_json['weather'][0]['icon']
            open_image(icon_name)

        def open_image(icon):
            size = int(lF_31.winfo_height())
            print(size)
            img1 = ImageTk.PhotoImage(Image.open('./img/' + icon + '.png').resize((60, 60)),Image.ANTIALIAS)
            weather_icon.delete("all")
            weather_icon.create_image(53, 5, anchor='ne', image=img1)
            weather_icon.image = img1

        bg_color = 'white'
        results = tk.Label(Frame_3_1, anchor='nw', justify='left', bd=1)
        results.config(font=20, bg='grey50')
        results.place(relx=0.005, rely=0.02)
        weather_icon = tk.Canvas(Frame_3_1, bg='grey50', bd=0, highlightthickness=0)
        weather_icon.place(relx=0.8, rely=0.1, relwidth=0.2, relheight=0.7)

        #weather_icon = tk.Label(results, bg="grey50")
        #label12.place(relx=0.0, rely=0.1)

        get_weather('Krakow')


        ##########
        #TIME-----------

        #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             def times():
            #current_time = time.strftime("%H:%M:%S")
            #clock_label.config(text=current_time)
            #clock_label.after(200, times)


        clock_label = tk.Label(Frame_3_3, font=("times", 12, "bold"),text='2:09 PM \n 15-Aug-20', bg="grey50")
        clock_label.place(relx=0.05, rely=0.05)
        #times()
        # przycisk calender
        img3 = Image.open('date1.png')
        img3 = img3.resize((20, 20), Image.ANTIALIAS)
        self.pic3 = ImageTk.PhotoImage(img3)
        # self.tkimage = ImageTk.PhotoImage(img)
        label1 = tk.Label(Frame_3_3, image=self.pic3,compound="bottom", bg="grey50")
        #btn3 = Button(Frame_3_3, image=self.pic3, compound="bottom", bg="grey50")
        label1.place(relx=0.4, rely=0.6)


        '''def graph():
            #plt.style.use('ggplot')

            """Cyberpunk GRAPH"""

            x,y = np.loadtxt('Zeszyt1.csv',
                             unpack = True,
                             delimiter = ',')

            """fig, ax = plt.subplots()
            colors = [
                '#08F7FE',  # teal/cyan
                '#FE53BB',  # pink
                '#F5D300',  # yellow
                '#00ff41',  # matrix green#
            ]

            for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
                plt.rcParams[param] = '#212946'  # bluish dark grey
            for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
                plt.rcParams[param] = '0.9'  # very light grey
            ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background"""

            plt.plot(x, y)
            """Cyber punk style graph"""
            plt.title('EpicGame')
            plt.ylabel('Y axis')
            plt.xlabel('X label')
            plt.show()'''



#______________________________________-------------------------


        def open_image_on(icon):
            img2 = ImageTk.PhotoImage(Image.open('./img1/' + icon + '.png').resize((40, 40)),Image.ANTIALIAS)
            status1.delete("all")
            status1.create_image(40, 0, anchor='ne', image=img2)
            status1.image = img2

        def open_image_off(icon):
            img1 = ImageTk.PhotoImage(Image.open('./img1/' + icon + '.png').resize((40, 40)),Image.ANTIALIAS)
            status2.delete("all")
            status3.delete("all")
            status4.delete("all")
            status2.create_image(40, 0, anchor='ne', image=img1)
            status3.create_image(40, 0, anchor='ne', image=img1)
            status4.create_image(40, 0, anchor='ne', image=img1)
            status2.image = img1
            status3.image = img1
            status4.image = img1


        def onClick(arg):
            if arg == 1:
                open_image_on('off')
                open_image_off('on')
            if arg == 2:
                open_image_on('on')
                open_image_off('off')

        status1 = tk.Canvas(Frame_2_5, bg='grey50', bd=0, highlightthickness=0)
        status1.place(relx=0.35, rely=0, relwidth=0.12, relheight=1)
        status2 = tk.Canvas(Frame_2_6, bg='grey50', bd=0, highlightthickness=0)
        status2.place(relx=0.35, rely=0, relwidth=0.12, relheight=1)
        status3 = tk.Canvas(Frame_2_5, bg='grey50', bd=0, highlightthickness=0)
        status3.place(relx=0.83, rely=0, relwidth=0.12, relheight=1)
        status4 = tk.Canvas(Frame_2_6, bg='grey50', bd=0, highlightthickness=0)
        status4.place(relx=0.83, rely=0, relwidth=0.12, relheight=1)
        open_image_on('off')
        open_image_off('off')
        # fig = plt.figure()
        my_button2 = tk.Button(Frame_2_5, text="START", command=lambda: [WriteMemory(plc, 1, 6, S7WLBit, 1),onClick(2)], width=20,
                               height=2, borderwidth=3, fg="orange4", bg="gray10")
        my_button2.place(relx=0.17, rely=0, anchor='n')
        my_button3 = tk.Button(Frame_2_6, text="STOP", command=lambda: [WriteMemory(plc, 1, 6, S7WLBit, 0),onClick(1)], width=20,
                               height=2, borderwidth=3, fg="orange4", bg="gray10")
        my_button3.place(relx=0.17, rely=0, anchor='n')
        my_button1 = tk.Button(Frame_2_6, text="ESTOP", command=lambda: [controller.show_frame("PageThree"),onClick(2)], width=20,
                               height=2, borderwidth=3, fg="orange4", bg="gray10")
        my_button1.place(relx=0.65, rely=0.5, anchor='center')
        '''def graph():
            house_price = np.random.normal(2000000,25000,5000)
            plt.hist(house_price,50)
            plt.show()'''
        my_button = tk.Button(Frame_2_5,text="BAZOWANIE", command=lambda: onClick(2), width=20,height=2,borderwidth=3,fg="orange4",bg="gray10")
        my_button.place(relx=0.65, rely=0, anchor='n')
        plt.style.use('fivethirtyeight')

        ck2 = Checkbutton(Frame_2_7, text='Windows Authentication',anchor='center',realheight = 10, realwidth = 10 )
        ck2.place(x=10, y=0)

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lF_33 = tk.LabelFrame(self, bg="gray94")
        lF_33.pack(fill="both", expand=True, pady=(0, 0))

        lF_41 = tk.LabelFrame(lF_33, bg="gray30", borderwidth=5, relief="raised")  # , height=100)
        lF_41.pack(fill="both", expand=True, pady=(30, 0))

        #Button
        b_51 = tk.Button(lF_33, text='Menu ', command=lambda: controller.show_frame("StartPage"), fg="black",
                         bg="grey80", width="10", height="1", highlightthickness=2)
        b_51.place(x=86, y=0)
        b_52 = tk.Button(lF_33, text='Prev ', command=lambda: controller.show_frame("PageTwo"), fg="black",
                         bg="grey80", width="10", height="1", highlightthickness=2)
        b_52.place(x=3, y=0)
        b_51 = tk.Button(lF_33, text='Next ', command=lambda: controller.show_frame("StartPage"), fg="black",
                         bg="grey80", width="10", height="1", highlightthickness=2)
        b_51.place(x=169, y=0)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    plc = c.Client()
    plc.connect('192.168.0.250', 0, 1)
    app = SampleApp()
    ani = animation.FuncAnimation(f, Graph, interval=1000)
    print()
    app.mainloop()