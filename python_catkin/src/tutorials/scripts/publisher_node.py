#!/usr/bin/env python

import rospy, time, pigpio
from std_msgs.msg import Float32

G = int(rospy.get_param('~pin_num', '18'))
f = int(rospy.get_param('~frequency', '100'))
mx = int(rospy.get_param('~max_pulse_width_us', '2400'))
mn = int(rospy.get_param('~min_pulse_width_us', '600'))

pi = pigpio.pi()
pi.set_PWM_frequency(G, f)
pi.set_PWM_range(G, 1000000/f)

def callback():
    if not pi.connected:
        rospy.logerror('pigpio not connected')
    else:
        rospy.loginfo('Setting ON')
        pi.set_PWM_dutycycle(G, 0)
        while True:
            pi.set_PWM_dutycycle(G, 1000)
            time.sleep(0.5)
            pi.set_PWM_dutycycle(G, 1500)
            time.sleep(0.5)


def on_shutdown():
    rospy.loginfo('Stopping servo')
    pi.set_PWM_dutycycle(G, 0)
    pi.stop()

def listener():
    rospy.init_node('servo_node', anonymous=True)
    rospy.Subscriber('servo_angle', Float32, callback())
    rospy.on_shutdown(on_shutdown)
    rospy.spin()

if __name__ == '__main__':
    listener()