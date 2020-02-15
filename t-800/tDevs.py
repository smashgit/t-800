import glob



# device objects will hold functions to add and transfer
# files needed to configure the device type
class device:
    def __init__(self, name, os, file):
        self.name = name
        self.os = os
        self.static=''
        self.bootcfg=''
        self.xgsn=''
        self.antiACL=''
        self.acl=''
        self.OS = ''
        self.PW = 'password'
        self.ENClink=[]
        self.findFile(file)
    # findFile appends needed files to the objects list
    def findFile(self, file):

        for config in glob.glob("*" + file + '*.cfg'):
            if '_xgsn' in config:
                self.xgsn=config
            elif '_acl' in config:
                self.acl = config
            elif '.cfg' in config:
                self.bootcfg = config

        for x in glob.glob('staticRP.cfg'):
            self.static = x

        for x in glob.glob('antiacl.cfg'):
            self.antiACL = x

        for os in glob.glob(self.os + "*"):
            self.OS = os
            global newOS
            newOS=''
            if self.OS == 'boot.ppc':
                GGM_OS = open('boot.ppc', errors = 'ignore')
                for line in GGM_OS:
                    if 'GGM8000' in line:
                        splitLine = line.split(',')
                        splitLine=splitLine[-1].split(' ')
                        self.os = 'OS version: '+splitLine[0].split('\x00', 1)[0]

            elif self.OS != '':
                self.os = 'OS version: '+self.OS
                #print(self.os)



