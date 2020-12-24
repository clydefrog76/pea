# PEA
Python Emulator for Audiovisual devices

PEA is a python written ethernet device emulator.
It can be used to create a virtual ethernet device for testing audiovisual code without having the actual hardware.

PEA uses sockets to open a TCP port for you to connect to. You will be able to use the popular JSON format to setup your virtual device.
Parameters include manufacturer, model, category, version number, and a reply delay for each command.
Also you will be able to add a description, a query and response command to simulate the individual device commands.
For the JSON template there is a very handy editor included so you don't have to struggle with the JSON formatting.

As an addition, PEA has the possibility to use a python script for more complicated feedback to the control system, for example increasing counters or more precise feedback.

Included in PEA are several tools to aid in your coding such as a hex-ascii converter and ascii tables.

Please use the HELP popup for a more precise description of the individual features.

To install pea either download the zip or use git clone. Using git clone will allow easy updates and you can even help contribute to the project with features and improvements.

See this video for a quick git clone how-to: https://youtu.be/DmbzwYdzh3M

![Screenshot](screenshot.png)
