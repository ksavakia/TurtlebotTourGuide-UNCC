from __future__ import division
import rospy
import roslib
from geometry_msgs.msg import *
#for xml parsing
from xml.dom.minidom import parse
import xml.dom.minidom

import os
import sys
import signal
from PyQt4.QtGui import *
#import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
#import PyQt4
qtCreatorFile = "tour_guide.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class landmark:
  prof_title = None
  room_no = None
  time_stamp = None
  frame_id = None
  position_x = None
  position_y = None
  position_z = None
  orientation_x = None
  orientation_y = None
  orientation_z = None
  orientation_w = None
  message = None
  flag = False
  
  def get_data(self,goal_name):
    
	DOMTree = xml.dom.minidom.parse("floor4_coordinate_data.xml")
	landmarks = DOMTree.documentElement
	goals = landmarks.getElementsByTagName("goal")
	for goal in goals:
	  if goal.hasAttribute("title"):
           room_num = goal.getElementsByTagName('room')[0].childNodes[0].data
           if goal_name.upper() in goal.getAttribute("title").upper() or goal_name.upper() in room_num.upper():
		  self.prof_title = goal.getAttribute("title")
		  self.room_no = goal.getElementsByTagName('room')[0].childNodes[0].data
		  self.time_stamp = goal.getElementsByTagName('timestamp')[0].childNodes[0].data
		  self.frame_id = goal.getElementsByTagName('frameid')[0].childNodes[0].data
		  self.position_x = goal.getElementsByTagName('position_x')[0].childNodes[0].data
		  self.position_y = goal.getElementsByTagName('position_y')[0].childNodes[0].data
		  self.position_z = goal.getElementsByTagName('position_z')[0].childNodes[0].data
		  self.orientation_x = goal.getElementsByTagName('orientation_x')[0].childNodes[0].data
		  self.orientation_y = goal.getElementsByTagName('orientation_y')[0].childNodes[0].data
		  self.orientation_z = goal.getElementsByTagName('orientation_z')[0].childNodes[0].data
		  self.orientation_w = goal.getElementsByTagName('orientation_w')[0].childNodes[0].data
                  self.message = 'Your destination is '+ str(room_num)
                  self.flag = True
                  return self
           else:
              self.flag = False
              self.message = 'Please enter a valid destination (not in XML).'
	
	return self

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_go.clicked.connect(self.PublishGoal)
       
    def PublishGoal(self):
        set_goal = str(self.location_box.toPlainText())
        rospy.init_node('pyGuide_app')
        pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        destination = landmark()
        if set_goal:
          if len(set_goal) >= 3:
            destination = destination.get_data(set_goal)
            if destination.flag:
             goal_msg=PoseStamped()
             goal_msg.header.stamp =rospy.Time.now()
             goal_msg.header.frame_id=destination.frame_id
             goal_msg.pose.position.x=float(destination.position_x)
             goal_msg.pose.position.y=float(destination.position_y)
             goal_msg.pose.position.z=float(destination.position_z)
             goal_msg.pose.orientation.x=float(destination.orientation_x)
             goal_msg.pose.orientation.y=float(destination.orientation_y)
             goal_msg.pose.orientation.z=float(destination.orientation_z)
             goal_msg.pose.orientation.w=float(destination.orientation_w)
             #rospy.loginfo('Goal_set is {}'.format(goal_msg))
             pub.publish(goal_msg)
             self.result_box.setText(str(destination.message))
             self.location_box.setText("")
            else:
             self.result_box.setText(str(destination.message))
          else:
            self.result_box.setText("Destination must be min 3 letters or numbers.")
        else:
          self.result_box.setText("Please enter a valid destination.")

if __name__ == "__main__":
    os.system("rostopic pub -1 /initialpose geometry_msgs/PoseWithCovarianceStamped '{header: {stamp: now, frame_id: map}, pose:{pose: {position: {x: 4.08812618256, y: 99.0702362061, z: 0.0}, orientation: { x: 0, y: 0, z: -0.028168847486, w: 0.999603179282 }}, covariance: [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]}}'")
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
