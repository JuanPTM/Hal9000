#
# Copyright (C) 2017 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, os, traceback, time

from PySide import *
from genericworker import *

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 200
		self.timer.start(self.Period)
		self.halldata = hallData()
		self.camaras = [self.peopletrackerCam22_proxy,self.peopletrackerCam23_proxy,self.peopletrackerCam24_proxy,self.peopletrackerCam25_proxy]

	def setParams(self, params):
		#try:
		#	self.innermodel = InnerModel(params["InnerModelPath"])
		#except:
		#	traceback.print_exc()
		#	print "Error reading config params"
		return True

	@QtCore.Slot()
	def compute(self):
#		print 'SpecificWorker.compute...'
		self.halldata.data = []
		for c in range(len(self.camaras)):
			if c == 1:
				continue
			self.halldata.data += self.filterData(self.camaras[c].getData(),c)

		#computeCODE
		#try:
		#	self.differentialrobot_proxy.setSpeedBase(100, 0)
		#except Ice.Exception, e:
		#	traceback.print_exc()
		#	print e

		# The API of python-innermodel is not exactly the same as the C++ version
		# self.innermodel.updateTransformValues("head_rot_tilt_pose", 0, 0, 0, 1.3, 0, 0)
		# z = librobocomp_qmat.QVec(3,0)
		# r = self.innermodel.transform("rgbd", z, "laser")
		# r.printvector("d")
		# print r[0], r[1], r[2]

		return True
	
	
	def filterData(self, peopledata, idCam):
		peopleList = []
		for people in peopledata.data:
			nPeople = PersonInfo()
			nPeople.pos = PlayerPos()
			nPeople.pos.x = 0
			nPeople.pos.y = 0
			nPeople.pos.z = 0
			for pos in people.pos:
			  nPeople.pos.x += pos.x
			  nPeople.pos.y += pos.y
			  nPeople.pos.z += pos.z 
			nPeople.pos.x = nPeople.pos.x / len(people.pos)
			nPeople.pos.y = nPeople.pos.y / len(people.pos)
			nPeople.pos.z = nPeople.pos.z / len(people.pos)
		
			nPeople.pos.x = people.pos[-1].x
			nPeople.pos.y = people.pos[-1].y
			nPeople.pos.z = people.pos[-1].z
		
			nPeople.idCam = idCam
			nPeople.id = people.id
			nPeople.predicted = people.predicted
			nPeople.vol.x = people.size.x
			nPeople.vol.y = people.size.y
			nPeople.vol.z = people.size.z
			peopleList.append(nPeople)
		return peopleList

####### INTERFACE METHOD

	#
	# getData
	#
	def getData(self):
		#
		#implementCODE
		#
		return self.halldata
