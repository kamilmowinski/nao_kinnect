#!/usr/bin/env python
import rospy
from naoqi import ALProxy
from my_kinnect.msg import NaoCoords


class NaoMonkey:
	PART = {
		'LShoulder': ['LShoulderPitch', 'LShoulderRoll'],
		'RShoulder': ['RShoulderPitch', 'RShoulderRoll'],
		'LElbow': ['LElbowYaw', 'LElbowRoll'],
		'RElbow': ['RElbowYaw', 'RElbowRoll'],
		'Head': ['HeadYaw', 'HeadPitch'],
	}
	LIMITS = {
		'Head': [[-2.0, 2.0], [-0.67, 0.51]],
		'LShoulder': [[-2.0, 2.0], [-0.31, 1.32]],
		'RShoulder': [[-2.0, 2.0], [-1.32, 0.31]],
		'LElbow': [[-2.0, 2.0], [-1.54, -0.03]],
		'RElbow': [[-2.0, 2.0], [0.03, 1.54]],
	}

	def __init__(self):
		rospy.init_node('nao_mykinect', anonymous=True)

		self.listener = rospy.Subscriber('nao', NaoCoords, self.move)
                ip = rospy.get_param('~ip', '10.104.16.9')
		port = int(rospy.get_param('~port', '9559'))

		self.al = ALProxy("ALAutonomousLife", ip, port)
		self.postureProxy = ALProxy("ALRobotPosture", ip, port)
		self.motionProxy = ALProxy("ALMotion", ip, port)
		
		self.al.setState("disabled")
		self.postureProxy.goToPosture("StandInit", 0.5)
		for part in ["Head", "LArm", "RArm"]:
			self.motionProxy.setStiffnesses(part, 1.0)
		rospy.loginfo(self.motionProxy.getSummary())

	def move(self, coords):
		rospy.loginfo(coords)
		part = coords.Part
		angles = coords.Angles
		speed = 1.0
		if part not in NaoMonkey.PART:
			error_msg = 'Wat? I Do not have ' + str(part)
			self.tts.say(error_msg)
			raise TypeError(error_msg)
		if len(NaoMonkey.PART[part]) != len(angles):
			error_msg = 'Wat? What shall i do with rest joint?'
			self.tts.say(error_msg)
			raise TypeError(error_msg)
		angles = map(lambda x: float(x)*math.pi/180.0, angles)
		for limit, angle in zip(NaoMonkey.LIMITS[part], angles):
			if angle < limit[0] or angle > limit[1]:
				error_msg = 'Wat? Limits man!'
				self.tts.say(error_msg)
				raise TypeError(error_msg)
		self.motionProxy.setAngles(NaoMonkey.PART[part], angles, speed);


if __name__ == '__main__':
	try:
		NaoMonkey()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass	
