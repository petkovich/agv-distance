Simple parser and publisher of data received on serial port from the ranging sensor.

clone, make

sudo chmod 777 /dev/ttyUSB0 #maybe some other port, check line 41

roscore #new terminal

rosrun agv_distance AGVread.py
