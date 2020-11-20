import re
  
print('Template Script Imported')

# dev stores all the attributes of the device
dev = {
    'Name' : 'Example Template'
    }

def rxscript(conn, rx):
    ''' Function to deal with more complex requests '''

    OutData = str()

    query_result = re.search(b'\x81\x8A\x8B[\x00-\xFF]', bytes(rx))
    power_result = re.search(b'\x71([\x23-\x24])\x0F[\x00-\xFF]', bytes(rx))
    rgb_result = re.search(b'\x31([\x00-\xFF])([\x00-\xFF])([\x00-\xFF])\x00\x00[\x00-\xFF]', bytes(rx))

    if query_result:
        head = '\x81\x33\x23\x61\x23\x10'
        r = '\x70'
        g = '\x80'
        b = '\x90'
        end = '\x00\x08\x00\x00\xDD'
        OutData += '{}{}{}{}{}'.format(head,r,g,b,end)        

    if power_result:
        powertype = {
            b'\x24':'\xF0\x71\x24\x85',
            b'\x23':'\xF0\x71\x23\x84'
            }
        OutData += '{}'.format(powertype[power_result.group(1)])

    if rgb_result:
        head = '\x81\x33\x23\x61\x23\x10'
        r = rgb_result.group(1).decode('latin-1')
        g = rgb_result.group(2).decode('latin-1')
        b = rgb_result.group(3).decode('latin-1')
        end = '\x00\x08\x00\x00\xDD'
        OutData += '{}{}{}{}{}'.format(head,r,g,b,end)
            
    return OutData

''' ***************************** '''
''' Custom functions from buttons '''
''' ***************************** '''  
# Func names < 10 characters
funcName = [
    "Func A",
    "Func B",
    "Func C",
    "Func D",
    "Func E" ]
  
def customFunc(func):
    ''' Custom stuff in here func will be 1-6 '''

    if func == 1:
        OutData = '\xF0\x71\x24\x85' # power on
    elif func == 2:
        OutData = '\xF0\x71\x23\x84' # power off
    elif func == 3:     
        OutData = '\x81\x33\x24\x61\x23\x10\x70\x80\x90\x00\x08\x00\x00\xFF' # set color 
    elif func == 4:
        OutData = '\r\n'
    elif func == 5:     
        OutData = '\r\n'

    return OutData

print("Script Started OK")