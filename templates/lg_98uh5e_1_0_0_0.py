import re
  
print('LG Script Imported')

# dev stores all the attributes of the device
dev = {
    'Name' : 'LG 98',
    'MuteState' : 'Off'
    }
MuteStates = {
    '00':'Off',
    '01':'On'
    }
MuteFeedback = {
    'Off':'00',
    'On':'01'
    }

def rxscript(conn, rx):
    ''' Function to deal with more complex requests '''
    try:
        OutData = str()
        
        Mute = re.search(b'kd 01 (0[01])', bytes(rx))
        MuteStatus = re.search(b'kd 01 FF', bytes(rx))
        
        if Mute:
            #print("Mute", Mute.group(1))
            dev['MuteState'] = MuteStates[Mute.group(1).decode()]
            OutData = 'd 01 OK{}x\r'.format(MuteFeedback[dev['MuteState']])

        elif MuteStatus:
                OutData = 'd 01 OK{}x\r'.format(MuteFeedback[dev['MuteState']])

        return OutData
        
    except Exception as e:
        print('Script:',e)
        raise

''' ***************************** '''
''' Custom functions from buttons '''
''' ***************************** '''
# Func names < 10 characters
funcName = [
    "Mute On",
    "Mute Off",
    "F3",
    "F4",
    "F5" ]
    
def customFunc(func):
    ''' Custom stuff in here func will be 1-5 '''
    
    # Toggle the relays
    if func == 1:
        OutData = 'd 01 OK01x\r'
        dev['MuteState'] = 'On'
    elif func == 2:
        OutData = 'd 01 OK00x\r'
        dev['MuteState'] = 'Off'
    elif func == 3:     
        OutData = '' 
    elif func == 4:
        OutData = ''
    elif func == 5:     
        OutData = ''

    return OutData

print("LG Script Started OK")