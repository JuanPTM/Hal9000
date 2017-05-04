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


transition_matrix = [[1, 0 , 1.5, 0],[0, 1 ,0 , 1.5], [0,0, 1,0],[0,0,0,1]]
transition_offset = [0, 0, 0, 0]
observation_matrix = [[1, 0 ,0 , 0],[0, 1 ,0 , 0], [0,0, 1,0],[0,0,0,1]] #np.eye(4) #+ random_state.randn(2, 2) * 0.1
observation_offset = [0, 0, 0, 0]
mask = [True, True, True, True]
n_timesteps = 30
n_dim_state = 4

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
			transition_matrices=transition_matrix,
			observation_matrices=observation_matrix,
			transition_offsets=transition_offset,
			observation_offsets=observation_offset,
			random_state=0
		  )
		self.Vx = 0
		self.Vy = 0
		self.maskMultiDel = False
		self.distancia = 0
		
    
	@classmethod
	def fromData(cls,pos,predicted,idLocal,idCam,idGlobal,vol, multiDelete=False, distancia=5000):
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
		clase.filtered_state_means = [ pos.x, pos.y, clase.Vx, clase.Vy]
		clase.filtered_state_covariances = np.eye(4)
		clase.Vx = 0
		clase.Vy = 0
		clase.distancia = distancia
		clase.maskMultiDel = multiDelete
		return clase
    
	def update(self, listaPersonas):
		nonLocalDel = True
		maskToErase = mask
		self.seen = False
		print "Actualizando id = ", self.idGlobal , "idLocal = ", self.idLocal
		print self.vol ,self.pos ,self.idCam
		print "-----------------------------"
		print len(listaPersonas)
		listaBorrar = []
		for index in range(len(listaPersonas)):
			print listaPersonas[index].id , self.distancia(listaPersonas[index].pos), listaPersonas[index].idCam, listaPersonas[index].pos
			if self.idCam == listaPersonas[index].idCam: #  Es mi cam
				if self.idLocal == listaPersonas[index].id: # id Local
					
					#ACTUALIZAR PERSONA - CODIGO DE ABAJO
					
					listaBorrar.append(index)
					maskToErase[listaPersonas[index].idCam] = False
					
					if not self.maskMultiDel:
						break
					print "-----------------------------"
					#return
			else: # No es mi cam
				if maskToErase[listaPersonas[index].idCam]: # Compruebo si puedo borrar
					if True: #abs(self.vol - (listaPersonas[index].vol.x * listaPersonas[index].vol.y * listaPersonas[index].vol.z)) < (0.25 * self.vol): #  Vol 
						if self.distancia(listaPersonas[index].pos) <= self.distancia: # Coor
							
							#ACTUALIZAR PERSONA - CODIGO DE ABAJO
							
							listaBorrar.append(index)
							#nonLocalDel = False  # NOT USED IN THIS VERSION
							maskToErase[listaPersonas[index].idCam] = False
							
							if not self.maskMultiDel:
								break
							print "-----------------------------"
							#return
		print "-----------------------------"
		count = 0
		for i in listaBorrar:
			print i-count
			
			timeRead = time()
			self.Vx = (listaPersonas[i-count].pos.x - self.pos[0] ) / ( timeRead - self.timestamp )
			self.Vy = (listaPersonas[i-count].pos.y - self.pos[1] ) / ( timeRead - self.timestamp )
			self.pos[0] = listaPersonas[i-count].pos.x
			self.pos[1] = listaPersonas[i-count].pos.y
			self.pos[2] = listaPersonas[i-count].pos.z
			self.vol = listaPersonas[i-count].vol.x * listaPersonas[i-count].vol.y * listaPersonas[i-count].vol.z
			self.predicted = listaPersonas[i-count].predicted
			self.timestamp = timeRead
			self.idCam = listaPersonas[i-count].idCam
			self.idLocal = listaPersonas[i-count].id
			self.seen = True
			
			listaPersonas.pop(i-count)
			count += 1
	      
	
	def distancia(self,pos):
	  return np.sqrt((self.pos[0] - pos.x)**2 + (self.pos[1]-pos.y)**2)
	
	def updateKalman(self):
		if self.seen:
			self.filtered_state_means, self.filtered_state_covariances = (self.kf.filter_update(self.filtered_state_means,self.filtered_state_covariances,[self.pos[0],self.pos[1],self.Vx,self.Vy],))
		else:
			self.filtered_state_means, self.filtered_state_covariances = (self.kf.filter_update(self.filtered_state_means,self.filtered_state_covariances,None,))
			self.pos[0] = self.filtered_state_means[0]
			self.pos[1] = self.filtered_state_means[1]
			self.Vx = self.filtered_state_means[2]
			self.Vy = self.filtered_state_means[3]
			self.seen = False
			self.predicted = True
		return
    
	def kill(self):
		return (time() - self.timestamp) > 10
	
	def __repr__(self):
		return str(self)

	def __str__(self):
		return  "{\n Posicion = "+str(self.pos) + "\n Predicted = "+str(self.predicted) + "\n idGlobal = "+ str(self.idGlobal) + "\n idLocal = "+ str(self.idLocal) + "\n idCam = " + str(self.idCam) +"\n timestamp = " + str(self.timestamp)+"\n }"