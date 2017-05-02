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
from time import time
import numpy as np
from pykalman import KalmanFilter


class individuo():
	def __init__(self):
		self.pos = [0,0,0]
		self.predicted = False
		self.idLocal = -1
		self.idGlobal = -1 
		self.timestamp = time()
		self.idCam = -1
		self.vol = -1 # Volumen
		self.seen = False # Flag update kalman
		self.kf = KalmanFilter(
		  
		  
		  )
    
	@classmethod
	def fromData(cls,pos,predicted,idLocal,idCam,idGlobal,vol):
		clase = cls()
		clase.pos[0] = pos.x
		clase.pos[1] = pos.y
		clase.pos[2] = pos.z
		clase.vol = vol.x * vol.y * vol.z
		clase.predicted = predicted
		clase.idLocal = idLocal
		clase.idCam = idCam
		clase.idGlobal = idGlobal
		clase.seen = True
		return clase
    
	def update(self, listaPersonas):
		nonLocalDel = True
		for persona in listaPersonas:
			if self.idCam == persona.idCam: # ¿ Es mi cam?
				if self.idLocal == persona.id: # ¿id Local?
					listaPersonas.remove(persona)
					self.pos[0] = persona.pos.x
					self.pos[1] = persona.pos.y
					self.pos[2] = persona.pos.z
					self.predicted = persona.predicted
					self.timestamp = time()
					self.seen = True
					return
			else: # No es mi cam
				if nonLocalDel:
					if abs(self.vol - (persona.vol.x * persona.vol.y *persona.vol.z)) < (0.1 * self.vol): # ¿ Vol ?
						if self.distancia(persona.pos) < 500: # ¿Coor?
							listaPersonas.remove(persona)
							self.pos[0] = persona.pos.x
							self.pos[1] = persona.pos.y
							self.pos[2] = persona.pos.z
							self.predicted = persona.predicted
							self.timestamp = time()
							self.seen = True
							nonLocalDel = False
							return
							
	      
	
	def distancia(self,pos):
	  return np.sqrt((self.pos[0] - pos.x)**2 + (self.pos[1]-pos.y)**2)
	
	def updateKalman(self):
		
		return
    
	def kill(self):
		return (time() - self.timestamp) > 30
	
	def __repr__(self):
		return str(self)

	def __str__(self):
		return  "{\n Posicion = "+str(self.pos) + "\n Predicted = "+str(self.predicted) + "\n idGlobal = "+ str(self.idGlobal) + "\n idLocal = "+ str(self.idLocal) + "\n idCam = " + str(self.idCam) +"\n timestamp = " + str(self.timestamp)+"\n }"