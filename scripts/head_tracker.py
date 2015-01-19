#! /usr/bin/env python
import rospy
import tf
import math
from std_msgs.msg import Header
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
from my_kinnect.msg import Head

class HeadTracker():

    def __init__(self):
        rospy.init_node('head_kinect', anonymous=True)
	self.myFrame = 'kinect_link'
	self.pub_trans = rospy.Publisher(self.myFrame, Head, queue_size=10)
        rate = rospy.get_param('~rate', 3)
        r = rospy.Rate(rate)
        self.target_joint = rospy.get_param('~target_joint', '/head')
        # ramka ktorej transformacji poszykujemy to /head + _nrUzytkownika, tu head_1
	self.target_joint += '_1'

	# Zainicjalizuj TransformListener
        self.tf = tf.TransformListener()
        rospy.loginfo("Rozpoczynam sledzenia uzytkownika za 5s...")

        # Zaczekaj 5s aby bufor TransformListenera sie zapelnil
        rospy.sleep(5.0)
        rospy.loginfo("Sledzenie rozpoczete!")
	
        while not rospy.is_shutdown():
	    trans, rot = self.tf.lookupTransform('/openni_depth_frame', self.target_joint, rospy.Duration())
            vec = Vector3(*trans)
            rt = Quaternion(*rot)
            h = Header(stamp=rospy.Time.now())
            head = Head(trans=vec, rot=rt, header=h)
            self.pub_trans.publish(head)
            r.sleep()

if __name__ == '__main__':
    try:
        HeadTracker()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
