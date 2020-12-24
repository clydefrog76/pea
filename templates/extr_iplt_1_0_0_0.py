import re
  
print('IPL T CR48 Script Imported')

# dev stores all the attributes of the device
dev = {
    'Name' : 'IPL T CR48',
    'relayCurrentState':[0,0,0,0,0,0,0,0,0],
    'inputStatus':[0,1,0,1,0]
    }

def rxscript(conn, rx):
    ''' Function to deal with more complex requests '''
    try:
        OutData = str()
        
        relayOn = re.search(b'(\d)\*1O', bytes(rx))
        relayOff = re.search(b'(\d)\*0O', bytes(rx))
        relayStatus = re.search(b'(\d)O', bytes(rx))
        setVerboseMode = re.search(b'w3cv\|', bytes(rx))
        inputStatus = re.search(b'([1-4])(\])', bytes(rx))
        
        
        if relayOn:
            relayNum = int(relayOn.group(1))
            dev['relayCurrentState'][relayNum] = 1
            OutData = 'Cpn{} Rly1\r\n'.format(relayNum)

        elif relayOff:
            relayNum = int(relayOff.group(1))
            dev['relayCurrentState'][relayNum] = 0
            OutData = 'Cpn{} Rly0\r\n'.format(relayNum)
        
        elif relayStatus:
            relayNum = int(relayStatus.group(1))
            relayState = dev['relayCurrentState'][relayNum]
            OutData = '{}\r\n'.format(relayState)        
            
        elif setVerboseMode:
            OutData = 'Vrb3\r\n'

        elif inputStatus:
            inp = int(inputStatus.group(1))
            OutData = '{}\r\n'.format(dev['inputStatus'][inp])
            
        return OutData
        
    except Exception as e:
        raise

''' ***************************** '''
''' Custom functions from buttons '''
''' ***************************** '''
# Func names < 10 characters
funcName = [
    "Rel 1",
    "Rel 2",
    "Inp 1",
    "Inp 2",
    "Func E" ]
    
def customFunc(func):
    ''' Custom stuff in here func will be 1-5 '''
    
    # Toggle the relays
    if func == 1:
        dev['relayCurrentState'][1] ^= 1    # Toggle Rel 1
        OutData = 'Cpn1 Rly{}\r\n'.format(dev['relayCurrentState'][1]) 
    elif func == 2:
        dev['relayCurrentState'][2] ^= 1    # Toggle Rel 1
        OutData = 'Cpn2 Rly{}\r\n'.format(dev['relayCurrentState'][2]) 
    elif func == 3:     
        dev['inputStatus'][1] ^= 1    # Toggle Rel 1
        OutData = 'Cpn1 Sio{}\r\n'.format(dev['inputStatus'][1]) 
    elif func == 4:
        dev['inputStatus'][2] ^= 1    # Toggle Rel 1
        OutData = 'Cpn2 Sio{}\r\n'.format(dev['inputStatus'][2]) 
    elif func == 5:     
        OutData = '\r\n'

    return OutData

print("Script Started OK")