#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
import itertools as itera
from random import random

plantillas = open('/home/gonthalo/Desktop/Github/Krypto_Kakuro/mapas.txt', 'r')
lineas = plantillas.read().split('\n')
plantillas.close()
plantillas = [lineas[:7], lineas[7:15], lineas[15:22], lineas[22:30], lineas[30:37], lineas[37:45], lineas[45:52], lineas[52:60]]

def gentext(matriz):
	plantilla = [[el for el in elem] for elem in matriz]
	texto = ''
	for ii in range(len(plantilla)):
		for jj in range(len(plantilla[0])):
			if plantilla[ii][jj] == ' ':
				check = True
				while check:
					rr = str(int(1+random()*9))
					check = False
					for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
						i, j = ii - di, jj - dj
						while plantilla[i][j] != '#':
							if plantilla[i][j] == rr:
								check = True
								break
							i, j = i - di, j - dj
						if check:
							break
				plantilla[ii][jj] = rr
				texto = texto + rr
	letras = ''
	while len(letras)<10:
		rr = 'QWERTYUIOPLJKHGFDSAZXCVBNM'[int(random()*26)]
		if rr not in letras:
			letras = letras + rr
	return ''.join([letras[int(num)] for num in texto])

def crear(texto = '', pistas = 7, plantilla = 'r'):
	plantillas = open('/home/gonthalo/Desktop/Github/Krypto_Kakuro/mapas.txt', 'r')
	lineas = plantillas.read().split('\n')
	plantillas.close()
	plantillas = [lineas[:7], lineas[7:15], lineas[15:22], lineas[22:30], lineas[30:37], lineas[37:45], lineas[45:52], lineas[52:60]]
	matriz = 0
	if plantilla == 'r':
		plantilla = int(7*random())
	matriz = [[el for el in elem] for elem in plantillas[plantilla]]
	if texto == '':
		texto = gentext(matriz)
	cc = 0
	letras = list(set([el for el in texto]))
	area = 0
	while len(letras)<9:
		letras = list(set(letras + ['ABCDEFGHIJK'[cc]]))
		cc += 1
	letras = ''.join(letras)
	cc = 0
	for ii in range(len(matriz)):
		for jj in range(len(matriz[0])):
			if matriz[ii][jj] == ' ':
				area += 1
				if cc < len(texto):
					matriz[ii][jj] = texto[cc]
					cc += 1
				else:
					cc = 10001
					while cc > 10000:
						cc = 10000
						matriz[ii][jj] = letras[int(random()*9)]
						dd = 1
						while matriz[ii+dd][jj]!= '#':
							if matriz[ii+dd][jj] == matriz[ii][jj]:
								cc += 1
							dd += 1
						dd = 1
						while matriz[ii][jj-dd]!= '#':
							if matriz[ii][jj-dd] == matriz[ii][jj]:
								cc += 1
							dd += 1
						dd = 1
						while matriz[ii][jj+dd]!= '#':
							if matriz[ii][jj+dd] == matriz[ii][jj]:
								cc += 1
							dd += 1
						dd = 1
						while matriz[ii-dd][jj]!= '#':
							if matriz[ii-dd][jj] == matriz[ii][jj]:
								cc += 1
							dd += 1
	#print 'Area:', area
	while 'ABCDEFGHIJ'[cc%10] in letras:
		cc += 1
	letras = letras + 'ABCDEFGHIJ'[cc%10]
	#print letras
	for solintentos in range(20):
		pnum = [el for el in '123456789']
		num = ''
		for ii in range(9, 0, -1):
			rr = int(random()*ii)
			num = num + pnum.pop(rr)
		num = num + '0'
		#print num
		dic = {}
		for ii in range(10):
			dic[letras[ii]] = num[ii]
			dic[num[ii]] = letras[ii]
		sumas = []
		counting = 0
		for ii in range(len(matriz)):
			for jj in range(len(matriz[0])):
				if matriz[ii][jj] == '#' and counting>0:
					sumas.append(''.join([dic[char] for char in str(counting)]))
					counting = 0
				if matriz[ii][jj] != '#':
					counting += int(dic[matriz[ii][jj]])
		for jj in range(len(matriz)):
			for ii in range(len(matriz[0])):
				if matriz[ii][jj] == '#' and counting>0:
					sumas.append(''.join([dic[char] for char in str(counting)]))
					counting = 0
				if matriz[ii][jj] != '#':
					counting += int(dic[matriz[ii][jj]])
		for intentos in range(10):
			lis = range(area)
			clues = []
			for jj in range(pistas):
				rr = int(random()*len(lis))
				clues.append(lis.pop(rr))
			newm = [[el for el in elem] for elem in plantillas[plantilla]]
			cc = 0
			for ii in range(len(matriz)):
				for jj in range(len(matriz[0])):
					if newm[ii][jj] == ' ':
						if cc in clues:
							newm[ii][jj] = matriz[ii][jj]
						cc += 1
			newkk = Kakuro(newm, sumas)
			sol = newkk.solucion()
			#print 'Soluciones:', sol, '\n\n~~~~~\n'
			if sol == 1:
				print 'Generacion completada:'
				print newkk
				return newkk

def cargar(archivo):
	a = open(archivo, 'r')
	lines = a.read().split('\n')
	a.close()
	return Kakuro([[el for el in line] for line in lines[1:]], lines[0].split(','))

def deducir(suma, lis):
	if 0 in lis:
		return 'E'
	if lis.count(' ')==1:
		iii = lis.index(' ')
		num = suma-sum(lis[:iii])-sum(lis[iii+1:])
		if num>0 and num<10:
			return [(iii, num)]
		else:
			return 'E'
	if ' ' not in lis:
		if len(set(lis))!=len(lis) or sum(lis)!= suma:
			return 'E'
		return 'C'
	if lis.count(' ')+len(set(lis))<len(lis)+1:
		return 'E'
	par = 0.0 + suma - sum([0 if el == ' ' else el for el in lis])
	if abs(par/lis.count(' ')-5)>3.6:
		return 'E'
	return '?'

def sumas_con(suma, free):
	if free == 1:
		return [[suma]]
	if suma > (19-free)*free/2:
		return []
	if suma < (free+1)*free/2:
		return []
	res = []
	for ii in range(max(1, suma-(20-free)*(free-1)/2), min(9, suma-(free-1)*free/2)+1):
		for item in sumas_con(suma-ii, free-1):
			res.append([ii]+item)
	return res

def resolver(nm, nsum, n_iter, printing = False):
	sumind = range(len(nsum))
	bucle = 1
	while bucle==1:
		bucle = 0
		for ind in sumind:
			ded = deducir(nsum[ind][0], [nm[xx][yy] for xx, yy in nsum[ind][1]])
			if ded == 'E':
				bucle = 2
				break
			if ded == 'C':
				bucle = 1
				sumind.pop(sumind.index(ind))
				break
			elif ded != '?':
				bucle = 1
				for pos, val in ded:
					xx, yy = nsum[ind][1][pos]
					nm[xx][yy] = val
		if len(sumind)==0:
			bucle = -1
	if bucle == 0:
		if n_iter==0:
			return 0
		mini = -1
		record = 1000
		for ii in range(len(nsum)):
			suma, pos = nsum[ii]
			free = 0
			for xx, yy in pos:
				if nm[xx][yy] == ' ':
					free += 1
				else:
					suma -= nm[xx][yy]
			formas = 100
			if free == 2:
				formas = 4-abs(suma-10)//2
			if free == 3:
				formas = len(sumas_con(suma, 3))
			if formas<record:
				record=formas
				mini = (ii, suma, free)
		#print 'Chose minimum:', mini
		if mini == -1:
			return '?'
		spots = []
		for xx, yy in nsum[mini[0]][1]:
			if nm[xx][yy]==' ':
				spots.append((xx, yy))
		#print 'Spots:', spots
		res = 2
		for lis in sumas_con(mini[1], mini[2]):
			#print 'Trying sum:', lis
			for ii in range(len(spots)):
				nm[spots[ii][0]][spots[ii][1]] = lis[ii]
			newres = resolver([[el for el in elem] for elem in nm], nsum, n_iter-1, printing)
			if newres < 0:
				res = newres + min(res, 0)
			else:
				res = min(res, newres)
		for ii in range(len(spots)):
			nm[spots[ii][0]][spots[ii][1]] = ' '
		return res
	if bucle < 0 and printing:
		#print 'SOLVED!'
		for line in nm:
			print ''.join([{'#':' ', ' ':'?'}[max(el, ' ')] if (el=='#' or el==' ') else str(el) for el in line])
	return bucle

class Kakuro:
	def __init__(self, matriz, sumas):
		self.m = matriz
		self.sumas = []
		counting = []
		cc = 0
		for ii in range(len(matriz)):
			for jj in range(len(matriz[0])):
				if matriz[ii][jj] == '#' and len(counting)>0:
					self.sumas.append((sumas[cc], counting))
					counting = []
					cc += 1
				if matriz[ii][jj] != '#':
					counting.append((ii, jj))
		for jj in range(len(matriz)):
			for ii in range(len(matriz[0])):
				if matriz[ii][jj] == '#' and len(counting)>0:
					self.sumas.append((sumas[cc], counting))
					counting = []
					cc += 1
				if matriz[ii][jj] != '#':
					counting.append((ii, jj))
		print 'Creado kakuro:'
		print self
	def guardar(self, filename):
		arch = open(filename, 'w')
		arch.write('\n'.join([''.join(line) for line in self.m])+'\n'+','.join([el[0] for el in self.sumas]))
		arch.close()
	def __str__(self):
		res = '\n'.join([''.join([{'#':' ', ' ':'?'}[el] if el in '# ' else el for el in line]) for line in self.m])
		split = len(self.sumas)//2
		res=res+'\n'+', '.join([el[0] for el in self.sumas[:split]])+'\n'+', '.join([el[0] for el in self.sumas[split:]])
		return res
	def probar(self, letras, p0, p1):
		s0, s2, s3 = 0, 0, 0
		res = False
		for ii in itera.permutations(p1, len(p1)):
			num = p0 + ''.join(ii)
			dic = {}
			for ii in range(10):
				dic[letras[ii]] = num[ii]
			intento = self.intentar(dic)
			if intento==0:
				#print '0: ', num
				s0 += 1
			elif intento < 0:
				#print '3: ', num
				s3 -= intento
				res = num
			else:
				s2 += 1
		#print '-:', s2
		#print '=:', s0
		#print '+:', s3
		return (res, s2, s0, s3)
	def intentar(self, llave, printed = False):
		nm = [[(el if el in ' #' else int(llave[el])) for el in elem] for elem in self.m]
		nsum = [((int(llave[suma[0]]) if len(suma)==1 else int(llave[suma[0]]+llave[suma[1]])), pos) for suma, pos in self.sumas]
		return resolver(nm, nsum, 10, printed)
	def get_letras(self):
		letras = ''
		for suma, lis in self.sumas:
			if len(suma)==2 and len(lis)==2:
				uno = suma[0]
			letras = letras + suma
		for ii in range(len(self.m)):
			for jj in range(len(self.m[0])):
				if self.m[ii][jj] not in '# ':
					letras = letras + self.m[ii][jj]
		letras = list(set([el for el in letras]))
		cc = 0
		while len(letras) < 10:
			ll = 'ABCDEFGHIJK'[cc]
			cc += 1
			if ll not in letras:
				letras.append(ll)
		return sorted(letras)
	def solucion(self, texto = True):
		uno = '?'
		letras = ''
		for suma, lis in self.sumas:
			if len(suma)==2 and len(lis)==2:
				uno = suma[0]
			letras = letras + suma
		for ii in range(len(self.m)):
			for jj in range(len(self.m[0])):
				if self.m[ii][jj] not in '# ':
					letras = letras + self.m[ii][jj]
		letras = list(set([el for el in letras]))
		if len(letras) < 10:
			letras = letras + [el for el in '+-:()@;=$!'][len(letras):]
		if uno != '?':
			letras.pop(letras.index(uno))
			letras = uno + ''.join(letras)
		llave, s2, s0, s3 = self.probar(letras, '1', '023456789')
		if uno == '?':
			llave, s2, s0, s3 = self.probar(letras, '', '0123456789')
		if s0 > 0:
			print 'Solucion incompleta:', s0
		#print '-:', s2
		#print '=:', s0
		#print '+:', s3
		if llave and texto and s3 == 1:
			#print 'Solucion:\n'
			#print letras
			#print llave
			dic = {}
			for ii in range(10):
				dic[letras[ii]] = llave[ii]
			self.intentar(dic, printed = texto)
		return s3



if __name__ == '__main__':
	mykk = cargar('kk1.txt')
	#print mykk.probar('GJUPRBWNCD', '123', '4567809')
	print mykk.solucion()
	#mynewkk = crear(texto = 'NODIMIDECXROCEDICMIXDDXON', pistas = 7, plantilla = 7)

