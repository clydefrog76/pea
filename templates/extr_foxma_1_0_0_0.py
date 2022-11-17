import re
  
print('FOX MATRIX Script Imported')

# dev stores all the attributes of the device
dev = {
    'Name' : 'Example Template'
    }

audio = []
video = []
matchStringDict = {}

def rxscript(conn, rx):
    ''' Function to deal with more complex requests '''
    for regexString, CurrentMatch in matchStringDict.items():
        result = re.search(regexString, rx)

        if result:
            OutData = CurrentMatch['callback'](result, CurrentMatch['para'])
    return OutData

def AddMatchString(regex_string, callback, arg):
    ''' Only add regex handler if not already in list '''
    #if regex_string not in matchStringDict:
    matchStringDict[regex_string] = {'callback': callback, 'para':arg}

def addMatch():
    ''' Builds all regex searches into a dict  '''
    AddMatchString(re.compile(b'w\d+cv\\r\\n'), MatchVerboseModeSet, None)
    AddMatchString(re.compile(b'\x1bEXEC\\r'), MatchExecModeSet, None)
    AddMatchString(re.compile(b'(\d+)\*(\d+)(\&|\$|\!)'), MatchMatrixTieSet, None)
    AddMatchString(re.compile(b'w0\*(\d+)\*(\d+)vc\\r'), MatchMatrixStatusRequest, None)
    #AddMatchString(re.compile(b'\x1bE(\d+)HDCP\\r'), MatchHDCPAuthRequest, None)
    #AddMatchString(re.compile(b'E(\d+)\*(\d)HDCP\\r'), MatchHDCPAuthSet, None)
    #AddMatchString(re.compile(b'wO\*HDCP\\r'), MatchHDCPRequestAll, None)
    #AddMatchString(re.compile(b'0\*\!'), MatchResetMatrix, None)
    print("Add match complete")

def MatchVerboseModeSet(match, tag):
    ''' Response to verbose mode setting from GCP diver '''
    print("VB Set")
    return "Vrb3\r\n"
    
def MatchExecModeSet(match, tag):
    ''' Respond to EXEC mode from GCP - used as heartbeat/keepalive '''
    return "Exec2\r\n"

TieTypes = {"$":"Aud", "&":"Vid", "!":"All"}
def MatchMatrixTieSet(match, tag):
    ''' Incomming tie commands from GCP. Feedback is then sent to ALL rooms/GCP '''
    In = match.group(1).decode()
    Out = match.group(2).decode()
    TieType = TieTypes[match.group(3).decode()]
    if TieType == "Aud":
        audio[int(Out) - 1] = int(In)
    if TieType == "Vid":
        video[int(Out) - 1] = int(In)
    if TieType == "All":
        audio[int(Out) - 1] = int(In)
        video[int(Out) - 1] = int(In)    
    cmd = "Out{} In{} {}\n\r".format(Out, In, TieType)
    return cmd
    
def MatchMatrixStatusRequest(match, tag):
    ''' send entire status of matrix to GCP system '''
    start = int(match.group(1).decode())
    TieTypeNum = int(match.group(2).decode())
    if TieTypeNum == 1:
        TieType = 'Aud'
        statusList = audio
    elif TieTypeNum == 2:
        TieType = 'Vid'
        statusList = video
    cmdList = []
    
    for x in range(start, start + 16):
        cmdList.append('{:02d} '.format(int(statusList[x])) )
    cmd = 'Vgp00 Out00*{}{}\r\n'.format(''.join(cmdList), TieType)
    return cmd

def initMatrix():
    ''' Sets all the status elements of the lists at startup '''
    for x in range(33):
        audio.append(0)
        video.append(0)
    print("Matrix initialized")

def HandleReceiveData(data):
    ''' Incoming XTP commands from the GCP driver in the room systems '''
        
    for regexString, CurrentMatch in matchStringDict.items():
        result = re.search(regexString, data)

        if result:
            CurrentMatch['callback'](result, CurrentMatch['para'])
            return
    print('Room: {} NO MATCH Rx: {} '.format(roomNum, data))

initMatrix()
addMatch()

''' ***************************** '''
''' Custom functions from buttons '''
''' ***************************** '''  
# Func names < 10 characters
funcName = [
    "Audio",
    "Video",
    "Func 3",
    "Func 4",
    "Func 5" ]
  
def customFunc(func):
    ''' Custom stuff in here func will be 1-6 
        place $$$ in OutData to just print out information / feedback FB
    '''

    if func == 1:
        OutData = '$$$ Audio {}'.format(audio)
    elif func == 2:
        OutData = '$$$ Video {}'.format(video)
    elif func == 3:     
        OutData = '\x81\x33\x24\x61\x23\x10\x70\x80\x90\x00\x08\x00\x00\xFF' # set color 
    elif func == 4:
        OutData = '\r\n'
    elif func == 5:     
        OutData = '\r\n'

    return OutData

print("Script Started OK")
