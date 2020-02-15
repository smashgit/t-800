from time import sleep
import serial



class tSer:
    def __init__(self, object):
        self.s = ''
    #Function to start a serial connection
    def comset(self):
        try:
            self.s = serial.Serial(port=object.port,baudrate=9600)
        except (OSError, serial.SerialException):
            print('Are you using a COM port?')
            pass

    #function that returns a list of ports available
    def serial_ports():
        global ports
        ports = ['Com%s' % (i+1) for i in range(256)]
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    # mini function for serial writing
    def SWR(self, string, nap):
        #self.s.write(string.encode())
        #self.s.write(b'\r\n')
        print(string)
        print(nap)
        #sleep(nap)

    # Load function is command flow to program devices
    def Load(self,tobject, object):
        print(object)
        if object.name == 'root':

            # wake up GGM
            for x in range(4):
                self.SWR('',0.15)
            # login
            self.SWR('root',0.05)
            self.SWR('',0.05)

            # set IP address for tftp
            self.SWR('setd !4 -ip net = 10.1.1.1 255.255.255.0', 0.15)

            # set new PW
            PW_New = 'SETD -SYS NMPassWord = "" "' + object.PW + '" "' + object.PW + '"'
            self.SWR(PW_New, 0.05)

            #set ac secret
            AC_secret = 'setd -ac secret = ' + object.PW
            self.SWR(AC_secret, 0.05)


            # transfer files into GGM primary dir
            # OS
            self.SWR('co 10.1.1.2:boot.ppc a:/primary/boot.ppc',40)
            # config file
            bootNOW1 = 'co 10.1.1.2:' + object.bootcfg + ' a:/primary/boot.cfg'
            self.SWR(bootNOW1, 1)
            # acl file
            aclNOW1 = 'co 10.1.1.2:' + object.acl + ' a:/primary/acl.cfg'
            self.SWR(aclNOW1, 1)
            # static
            self.SWR('co 10.1.1.2:staticRP.cfg a:/primary/staticRP.cfg', 1)
            # antiacl
            if object.antiACL != '':
                self.SWR('co 10.1.1.2:antiacl.cfg a:/primary/antiacl.cfg', 1)
            # xgsn
            if object.xgsn != '':
                xgsnNOW1 = 'co 10.1.1.2:' + object.xgsn + '  a:/primary/xgsn.cfg'
                self.SWR(xgsnNOW1, 1)



            # transfer files into GGM secondar dir
            # OS
            self.SWR('co 10.1.1.2:boot.ppc a:/secondar/boot.ppc', 40)
            # config file
            bootNOW1 = 'co 10.1.1.2:' + object.bootcfg + ' a:/secondar/boot.cfg'
            self.SWR(bootNOW1, 1)
            # acl file
            aclNOW1 = 'co 10.1.1.2:' + object.acl + ' a:/secondar/acl.cfg'
            self.SWR(aclNOW1, 1)
            # static
            self.SWR('co 10.1.1.2:staticRP.cfg a:/secondar/staticRP.cfg', 1)
            # antiacl
            if object.antiACL != '':
                self.SWR('co 10.1.1.2:antiacl.cfg a:/secondar/antiacl.cfg', 1)
            # xgsn
            if object.xgsn != '':
                xgsnNOW1 = 'co 10.1.1.2:' + object.xgsn + '  a:/secondar/xgsn.cfg'
                self.SWR(xgsnNOW1, 1)

            ####  INSERT  SSH Criteria
            if tobject.varSSH.get() == 1:
                # SSH commands
                self.SWR('gensshkey rsa 1024', 10)
                self.SWR('gensshkey dsa 1024', 10)

            #### INSERT IPSEC Criteria
            if tobject.varIPSEC.get() == 1:
                for x in object.ENClink:
                    self.SWR(x, 1)

            self.SWR('reboot', 0.05)

        elif object.name == 'manager':
            # wake up switch
            for x in range(4):
                self.SWR('', 0.15)
            sleep(7)

            # set up ip address for tftp
            self.SWR('con', 0.05)
            self.SWR('vlan 1 ip addr 10.1.1.1 255.255.255.0', 0.05)
            self.SWR('ex', 0.05)

            # transfer OS
            swOS = 'copy tftp flash 10.1.1.2 ' + object.OS
            self.SWR(swOS, 0.05)
            self.SWR('y', 30)

            # set switch password
            self.SWR('con', 0.05)
            self.SWR('password all', 0.05)
            for x in range(4):
                self.SWR(object.PW, 0.15)
            sleep(1)

            # transfer config
            swCFG = 'copy tftp startup-config 10.1.1.2 ' + object.bootcfg
            self.SWR(swCFG, 0.05)
            self.SWR('y', 0.05)



