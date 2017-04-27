#
# <one line to give the program's name and a brief idea of what it does.>
# Copyright (C) 2017  <copyright holder> <email>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#

class individuo():
    def __init__(self):
	self.pos = [0,0,0]
	self.predicted = False
	self.idLocal = -1
	self.idGlobal = -1 
	self.idCam = -1
    
    @classmethod
    def fromData(cls,pos,predicted,idLocal,idCam,idGlobal):
	#print cls.pos
	#print pos
	clase = cls()
	clase.pos[0] = pos.x
	clase.pos[1] = pos.y
	clase.pos[2] = pos.z
	clase.predicted = predicted
	clase.idLocal = idLocal
	clase.idCam = idCam
	clase.idGlobal = idGlobal
	return clase
	
    def __str__(self):
	return  "{\n Posicion = "+str(self.pos) + "\n Predicted = "+str(self.predicted) + "\n idGlobal = "+ str(self.idGlobal) + "\n idLocal = "+ str(self.idLocal) + "\n idCam = " + str(self.idCam) +"\n }"