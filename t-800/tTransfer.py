from tVerify import Verify as Ver
from tDevs import device
from tSerial import tSer
import tkinter as tk
from tkinter import ttk
from tkinter import *




class tTrans:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title('T-800')
        self.name = ''
        self.OS = ''
        self.file = ''
        self.unit = ''
        self.defV = StringVar(self.app)
        self.defV.set('Set Com port')
        self.ComNum = OptionMenu(self.app, self.defV, *tSer.serial_ports())
        self.devList = ("GGM8000", "HP-2620", "HP-3800", "ARUBA-2930")
        self.devListVar = StringVar()
        self.devListVar.set("Set Type")
        self.devices = OptionMenu(self.app, self.devListVar, *self.devList, command=self.device_type)
        self.fileType = ttk.Entry(self.app, width=20)
        self.fileType.insert(0, '10.1.235.252')
        self.verify = ttk.Button(self.app, text='Verify', command=self.Verify)
        self.transfer=ttk.Button(self.app,text='Transfer',command=self.tLoad)
        self.reset = ttk.Button(self.app, text='Reset', command=self.Reset)
        self.varSSH = IntVar()
        self.SSH = Checkbutton(self.app, text="SSH", variable=self.varSSH)
        self.varIPSEC = IntVar()
        self.IPSEC = Checkbutton(self.app, text="Encrypt Links", variable=self.varIPSEC)

    def Reset(self):
        self.fileType.delete(0, 'end')

    def Verify(self):
        self.file = str(self.fileType.get())
        print(self.file)
        self.unit = device(self.name, self.OS, self.file)
        Ver(self.unit, self.varIPSEC.get())

    def tLoad(self):
        global transfer
        new = tSer(transfer)
        new.Load(transfer, transfer.unit)


    def device_type(self, object):
        if self.devListVar.get() == 'GGM8000':
            self.name = 'root'
            self.OS = 'boot.ppc'

        elif self.devListVar.get() == 'HP-2620':
            self.name = 'manager'
            self.OS = 'RA'

        elif self.devListVar.get() == 'HP-3800':
            self.name = 'manager'
            self.OS = 'KA'

        elif self.devListVar.get() == 'ARUBA-2930':
            self.name = 'manager'
            self.OS = 'WC'


transfer = tTrans()

#Comport functions
# function creates device object {login name, OS, ip address}
transfer.ComNum.grid(row = 0, column = 0)
#Spinbox with devices to destroy
transfer.devices.grid(row = 0, column = 1)

#Entry field for config file
transfer.fileType.grid(row=0,column=2)

#Button used to verify
transfer.verify.grid(row=0,column=3)

transfer.transfer.grid(row=1,column=3)

transfer.reset.grid(row=2,column=3)

transfer.SSH.grid(row=2, column=0)


transfer.IPSEC.grid(row=2, column=1)

transfer.app.mainloop()