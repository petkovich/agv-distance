#!/usr/bin/env python

import time
import rospy
from agv_distance.msg import RobotDistance
import rospkg

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

def talker():

    rospy.init_node('AGV_distance_publisher')
    #published_msg = PoseArray()
    pub = rospy.Publisher('robot_distances', RobotDistance)
    r = rospy.Rate(10)
    aRobot = RobotDistance()
    rospack = rospkg.RosPack()
    f = open(rospack.get_path('agv_distance')+"/data/NUCprotocol2.txt")
    line = f.readline()

    while line:
        print "At", time.time(), "received", len(line), "chars."
        print line
        data = line.split(" ")
        data = list_to_int(data)
        if data[0]==65535:
            print "Header is FFFF, check passed."
        else:
            print "Error in data, skipping."
            print line
            line = f.readline()
            continue

        print "Number of AGVs is", data[1]

        for i in range(data[1]):
            print "AGV id:", data[2*i+2]
            print "AGV range:", data[2*i+3]
            aRobot.header.stamp = rospy.Time.now()
            aRobot.header.seq = aRobot.header.seq + 1
            aRobot.id = data[2*i+2]
            aRobot.distance = data[2*i+3]
            pub.publish(aRobot)
            r.sleep()

        if data[-1]==3338:
            print "Endmark reached"
        else:
            print "Wrong endmark:", data[-1], "exiting."
            break

        line = f.readline()


if __name__ == '__main__':
    try:
         talker()
    except rospy.ROSInterruptException:
         pass