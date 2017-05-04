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

from individuo import *
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
		self.Period = 1000
		self.timer.start(self.Period)
		self.idGlobal = 0
		self.listaPersonas = []
		self.multiDelete = False
		

	def setParams(self, params):
		self.multiDelete = params["mask"]
		self.dist=params["distRec"]
		#try:
		#	self.innermodel = InnerModel(params["InnerModelPath"])
		#except:
		#	traceback.print_exc()
		#	print "Error reading config params"
		return True

	@QtCore.Slot()
	def compute(self):
		halldata =  self.peoplehall_proxy.getData()
		nuevaLista = halldata.data
		for persona in self.listaPersonas:
			persona.update(nuevaLista)
			persona.updateKalman()
			if persona.kill():
				self.listaPersonas.remove(persona)
		for nPersona in nuevaLista:
			self.listaPersonas.append(individuo.fromData(nPersona.pos,
						nPersona.predicted,
						nPersona.id,
						nPersona.idCam,
						self.idGlobal,
						nPersona.vol,
						multiDelete=self.multiDelete,
						distancia=self.distRec))
			self.idGlobal= (self.idGlobal +1 ) % sys.maxint
		
		
		
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


	#
	# getHall
	#
	def getHall(self):
		hallpersons = hallPersons()
		hallpersons.data = []
		for person in self.listaPersonas:
			persona = PersonInfo()
			persona.pos.x = person.pos[0]
			persona.pos.y = person.pos[1]
			persona.pos.z = 0
			persona.id = person.idGlobal
			hallpersons.data.append(persona)
		ret = hallpersons
		#
		#implementCODE
		#
		return ret