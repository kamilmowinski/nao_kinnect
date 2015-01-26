#! /usr/bin/env python
import rospy
import tf
import math
from std_msgs.msg import Header, Float32, String
from my_kinnect.msg import SkeletonCoords, NaoCoords

class Monkey():

    def __init__(self):
	self.calibration = True
	self.vector = None
	self.rot = None
	self.msg_count = 0
        rospy.init_node('monkey_mykinect', anonymous=True)
	self.myFrame = '/nao'
	self.pub_trans = rospy.Publisher(self.myFrame, NaoCoords, queue_size=10)
        self.listener = rospy.Subscriber('/kinect_link', SkeletonCoords, self.move)
	rate = rospy.get_param('~rate', 3)
	ip = rospy.get_param('~ip', '10.104.16.141')
	port = int(rospy.get_param('~port', '9559'))

        r = rospy.Rate(rate)

        while not rospy.is_shutdown():
            r.sleep()

    def move(self, coords):
	if self.calibration:
		if self.msg_count < 5:
			self.msg_count += 1
			if self.rot:
				self.rot[0] += coords.rot.x
				self.rot[1] += coords.rot.y
				self.rot[2] += coords.rot.z
				self.rot[3] += coords.rot.w
			else:
				self.rot = list()
				self.rot.append(coords.rot.x) 
				self.rot.append(coords.rot.y) 
				self.rot.append(coords.rot.z) 
				self.rot.append(coords.rot.w) 
			if self.vector:
				self.vector[0] += coords.trans.x
				self.vector[1] += coords.trans.y
				self.vector[2] += coords.trans.z
			else:
				self.vector = list()
				self.vector.append(coords.trans.x) 
				self.vector.append(coords.trans.y) 
				self.vector.append(coords.trans.z) 
		else:
			self.calibration = False
			self.vector[0] /= 5
			self.vector[1] /= 5
			self.vector[2] /= 5
			self.rot[0] /= 5
			self.rot[1] /= 5
			self.rot[2] /= 5
			self.rot[3] /= 5
	else:
		r = coords.rot.z - self.rot[3]
		head = NaoCoords(Part=String("Head"), Angles1=Float32(100.0 * r),
				 Angles2=Float32(0))
		self.pub_trans.publish(head)
		rospy.loginfo(head)
		


if __name__ == '__main__':
    try:
        Monkey()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

