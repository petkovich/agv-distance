#!/usr/bin/env python

import time
import rospy
from agv_distance.msg import RobotDistance
import rospkg
import serial

def list_to_int(data):
    output = []
    try:
        converted_item = int(data[0]+data[1], 16)
        output.append(converted_item)
        converted_item = int(data[5], 16)
        output.append(converted_item)   
    except:
        pass

    for i in range(6, len(data), 2):
        item = data[i]+data[i+1]
        try:
            converted_item = int(item,16)
            output.append(converted_item)
        except:
            pass
    return output

def decode_input(data):
    data = data.encode('hex')

def talker():

    rospy.init_node('AGV_distance_publisher')
    #published_msg = PoseArray()
    pub = rospy.Publisher('robot_distances', RobotDistance)
    r = rospy.Rate(10)
    aRobot = RobotDistance()
    rospack = rospkg.RosPack()
    #f = open(rospack.get_path('agv_distance')+"/data/NUCprotocol2.txt")
    #line = f.readline()
    ser = serial.Serial('/dev/ttyUSB0', 115000)
    #while line:
    while True:
        character1 = ser.read()
        character1 = character1.encode('hex')
        if character1!='ff':
            continue
        character1 = ser.read()
        character1 = character1.encode('hex')
        if character1!='ff':
            continue
        print "FFFF pass check"
        dummy = ser.read()
        dummy = ser.read()
        dummy = ser.read()
        print "Discarded dummies"
        robot_num = ser.read()
        robot_num = robot_num.encode('hex')
        robot_num = int(robot_num,16)

        print "Number of AGVs is", robot_num

        for i in range(robot_num):
            agv_id1 = ser.read()
            agv_id2 = ser.read()
            agv_id = agv_id1.encode('hex') + agv_id2.encode('hex')
                  
            print "AGV id:", int(agv_id,16)

            agv_range1 = ser.read()
            agv_range2 = ser.read()
            agv_range = agv_range1.encode('hex') + agv_range2.encode('hex')

            print "AGV range:", int(agv_range,16)
            aRobot.header.stamp = rospy.Time.now()
            aRobot.header.seq = aRobot.header.seq + 1
            aRobot.id = int(agv_id,16)
            aRobot.distance = int(agv_range,16)
            pub.publish(aRobot)
            #r.sleep()

        character1 = ser.read()

        character2 = ser.read()


        #line = f.readline()


if __name__ == '__main__':
    try:
         talker()
    except rospy.ROSInterruptException:
         pass