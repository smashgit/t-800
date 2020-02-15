




def Verify(object, IPSEC):
    if object.OS == '':
        print('No OS found')
    else:
        print(object.os)
    if object.bootcfg == '':
        print('No config found')
    else:
        print('config: '+object.bootcfg)
    if object.name == 'root':
        if object.acl == '':
            print('No acl file found')
        else:
            print('acl : '+object.acl)
        if object.static == '':
            print('No staticRP found')
        else:
            print('staticRP: '+object.static)
        if object.antiACL == '':
            print('No antiacl found')
        else:
            print('antiacl: '+object.antiACL)

    if IPSEC == 1:
        # IPsec links will be stated in config
        # following searches config for these lines containing IPIP
        # once found will split the line for the psk ip addresses
        search = open(object.bootcfg)
        for line in search:
            if 'IPIP' in line:
                print(line)
                var = line.split(' ')
                psk = str(var[-1])[:-1]
                print('psk'+psk)

                # now that the ip addresses are found
                # use them to find correct commands in
                # the psk file
                PSK = open("PSK.cfg")
                for line in PSK:
                    if psk in line:
                        link1 = line.replace('******', object.PW)
                        object.ENClink.append(link1)

        if object.ENClink == []:
            print('LINKS NOT FOUND')
        else:
            for x in object.ENClink:
                print('Link to be used: ' + x)
        search.close()
        PSK.close()


