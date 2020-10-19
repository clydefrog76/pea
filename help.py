howtomsg = \
'''How to use PEA

Here are the steps required to create a working
TCP emulator using PEA:

1) Obtain the protocol for the device you need to emulate
2) Establish the TCP Port number (ie Telnet port 23)
3) Open the JSON editor entering all the device details
4) To add a new command line increase the number of commands
5) Add a description, query & response. Use this format

    hello\r\n   hello\x0a\x0d   \x35\x75\x0d\x0a

This methood allows simple protocols to be quickly and easily
created. If you need more complex responses, such as feedback 
from a switcher, then use an associated python script to deal
wiith more complex requirements.

To enable an associated script check the Script? box in the JSON
editor and then create (in the same folder) a .py file with the same
filename as the JSON file. This will be automatically loaded if the 
checkbox is ticked.

Look at the example for more details on how to deal with 
received and send strings.

'''