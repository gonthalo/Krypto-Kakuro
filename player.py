#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, inspect, sys, math, threading, pygame, pygame.mixer
from time import time
from random import random
from pygame.locals import *
from PIL import Image
from datetime import datetime
from pitonkk.kk import *

PATH = inspect.getfile(inspect.currentframe())[:-9]

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 550, 450
FPS = 30
NEGRO = (0, 0, 0)
NABLA = (10, 200, 110)
BLANCO = (255, 255, 255)
CIELO = (40, 50, 200)
ROJO = (250, 20, 20)

if True == True:
	img_aux = Image.new('RGB', (1, 1), 'black')
	img_aux.save(PATH + 'img/void.png')

img_esquina = Image.open(PATH + 'img/esquina.png')
MAT_ESQ = [[1.-img_esquina.getpixel((ii, jj))[0]/255. for jj in range(img_esquina.size[1])] for ii in range(img_esquina.size[0])]
ESQ = 2
PAD = 3

teclas = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, 241,
K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_SPACE, K_COMMA, K_PERIOD, 45, 39, 231, 43, 60, 61]
LETRAS = u'!"·$%&/()=ABCDEFGHIJKLMNÑOPQRSTUVWXYZ ;:_?Ç*>¿'
letras = u"1234567890abcdefghijklmnñopqrstuvwxyz ,.-'ç+<¡"
diccio = {'hola': 'IDIOTA'}
for ii in range(len(teclas)):
	diccio[teclas[ii]] = LETRAS[ii]
	diccio[-teclas[ii]] = letras[ii]
acentuar = {'a':u'á', 'e':u'é', 'i':u'í', 'o':u'ó', 'u':u'ú', 'A':u'Á', 'E':u'É', 'I':u'Í', 'O':u'Ó', 'U':u'Ú'}
def wrr():
	return ['-', '/', '|', '\\'][int(time()*100)%4]

def n00():
	return

def ynt(num):
	if (num >= 0):
		return int(num)
	return int(num) - 1

class Imagen:
	def __init__(self, file_name):
		self.area = pygame.image.load(PATH + 'img/' + file_name)
		self.rect = self.area.get_rect()
		self.x = self.rect.width
		self.y = self.rect.height
	def poner(self, i_x, i_y, phi=0):
		SCREEN.blit(pygame.transform.rotate(self.area, phi), self.rect.move(i_x, i_y))

class Boton:
	def __init__(self, xxx, yyy, texto, accion, padding = PAD, color = NABLA):
		self.texto = texto
		self.accion = accion
		if xxx == -1:
			xxx = SCREEN_WIDTH/2 - self.texto.x/2
		if yyy == -1:
			yyy = SCREEN_HEIGHT/2 - self.texto.y/2
		posicion = self.x, self.y = xxx, yyy
		size = (texto.x, texto.y)
		img_aux = Image.new('RGB', (size[0] + 2*ESQ + 2*padding, size[1] + 2*ESQ + 2*padding), 'black')
		for jj in range(-1, 1):
			for ii in range(size[0] + 2*padding):
				img_aux.putpixel((ii + ESQ, jj + ESQ/2), color)
				img_aux.putpixel((ii + ESQ, size[1] + 2*padding + 3*ESQ/2 - 1 - jj), color)
			for ii in range(size[1] + 2*padding):
				img_aux.putpixel((jj + ESQ/2, ii + ESQ), color)
				img_aux.putpixel((size[0] + 2*padding + 3*ESQ/2 - 1 - jj, ii + ESQ), color)
		for vx, vy, matriz in [(0, 0, MAT_ESQ),
		(size[0] + 2*padding + ESQ, 0, [[MAT_ESQ[jj][ESQ - 1 - ii] for jj in range(ESQ)] for ii in range(ESQ)]),
		(size[0] + 2*padding + ESQ, size[1] + 2*padding + ESQ, [[MAT_ESQ[ESQ - 1 - ii][ESQ - 1 - jj] for jj in range(ESQ)] for ii in range(ESQ)]),
		(0, size[1] + 2*padding + ESQ, [[MAT_ESQ[ESQ - 1 - jj][ii] for jj in range(ESQ)] for ii in range(ESQ)])]:
			for ii in range(ESQ):
				for jj in range(ESQ):
					img_aux.putpixel((ii + vx, jj + vy), tuple([int(tt*matriz[ii][jj]) for tt in (10, 200, 110)]))
		path_aux = 'b_image_' + str(posicion[0]) + '_' + str(posicion[1]) + '.png'
		img_aux.save(PATH + 'img/' + path_aux)
		self.fondo = Imagen(path_aux)
		self.padding = padding
	def dibujar(self):
		self.fondo.poner(self.x - ESQ - self.padding, self.y - ESQ - self.padding)
		self.texto.poner(self.x, self.y)
	def clicar(self, mousex, mousey):
		if (mousex > self.x - ESQ/2 and mousey > self.y - ESQ/2 and mousex - self.x < self.texto.x + ESQ/2 and mousey - self.y < self.texto.y + ESQ/2):
			self.accion()

def get_text(texto, fondo, frente, font, size):
	pygame.font.init()
	fuente = pygame.font.SysFont(font, size)
	if fondo == None:
		texto = fuente.render(texto, True, frente)
	else:
		texto = fuente.render(texto, True, frente, fondo)
	img_a = Imagen('void.png')
	img_a.area = texto
	img_a.rect = img_a.area.get_rect()
	img_a.x, img_a.y = img_a.rect.width, img_a.rect.height
	return img_a

class Texto:
	def __init__(self, posicion, cnt, fuente, fsize, color, colorf):
		self.posicion = posicion
		self.content = cnt
		self.rend = ''
		self.color = color
		self.colorf = colorf
		self.fuente = fuente
		self.fsize = fsize
		self.img = False
		self.rendx, self.rendy = self.posicion[0], self.posicion[1]
	def poner(self):
		if self.content != self.rend:
			self.rend = self.content
			self.img = get_text(self.rend, self.colorf, self.color, self.fuente, self.fsize)
			if self.posicion[0] == -1:
				self.rendx = SCREEN_WIDTH/2 - self.img.x/2
			if self.posicion[1] == -1:
				self.rendy = SCREEN_HEIGHT/2 - self.img.y/2
		self.img.poner(self.rendx, self.rendy)

def poner_texto(cadena, alto, fuen, tam, posi, color):
	pygame.font.init()
	fuente = pygame.font.SysFont(fuen, tam)
	dy = alto*len(cadena)/2
	for ind in range(len(cadena)):
		texto = fuente.render(cadena[ind], True, color, (0, 0, 0))
		dx = texto.get_rect().width/2
		SCREEN.blit(texto, texto.get_rect().move(posi[0] - dx, posi[1] + alto*ind - dy))

class Escritor:
	def __init__(self, posicion, size, cnt, fsize = 20, fcolor = NABLA):
		img_aux = Image.new('RGB', (size[0] + 2*ESQ, size[1] + 2*ESQ), 'black')
		for jj in range(-1, 1):
			for ii in range(size[0]):
				img_aux.putpixel((ii + ESQ, jj + ESQ/2), fcolor)
				img_aux.putpixel((ii + ESQ, size[1] + 3*ESQ/2 - 1 - jj), fcolor)
			for ii in range(size[1]):
				img_aux.putpixel((jj + ESQ/2, ii + ESQ), fcolor)
				img_aux.putpixel((size[0] + 3*ESQ/2 - 1 - jj, ii + ESQ), fcolor)
		for vx, vy, matriz in [(0, 0, MAT_ESQ),
		(size[0] + ESQ, 0, [[MAT_ESQ[jj][ESQ - 1 - ii] for jj in range(ESQ)] for ii in range(ESQ)]),
		(size[0] + ESQ, size[1] + ESQ, [[MAT_ESQ[ESQ - 1 - ii][ESQ - 1 - jj] for jj in range(ESQ)] for ii in range(ESQ)]),
		(0, size[1] + ESQ, [[MAT_ESQ[ESQ - 1 - jj][ii] for jj in range(ESQ)] for ii in range(ESQ)])]:
			for ii in range(ESQ):
				for jj in range(ESQ):
					img_aux.putpixel((ii + vx, jj + vy), tuple([int(tt*matriz[ii][jj]) for tt in fcolor[:3]]))
		path_aux = 'e_image_' + str(posicion[0]) + '_' + str(posicion[1]) + '.png'
		img_aux.save(PATH + 'img/' + path_aux)
		self.fondo = Imagen(path_aux)
		self.posicion = posicion
		self.size = size
		self.content = cnt
		self.fuente = 'courier'
		self.fsize = fsize
		self.fcolor = fcolor
	def poner(self, writing = False):
		chain = []
		elem = ''
		for item in (self.content + writing*wrr()).split(' '):
			if (len(elem) + len(item))*self.fsize/1.5 > self.size[0] + ESQ - 6:
				chain.append(elem)
				elem = item
				continue
			elem = elem  + ' '*(elem != '') + item
		chain.append(elem)
		self.fondo.poner(self.posicion[0]-ESQ, self.posicion[1]-ESQ)
		poner_texto(chain, self.fsize, self.fuente, self.fsize, (self.posicion[0] + self.size[0]/2, self.posicion[1] + self.size[1]/2), self.fcolor)
		return
		img_aux = get_text(self.content, False, self.fcolor, self.fuente, self.fsize)
		img_aux.poner(posicion)
	def escribir(self, tecla, shift, borrar = False):
		if tecla == 8 or borrar:
			self.content = self.content[:-1]
		if tecla in teclas:
			if shift:
				self.content += diccio[tecla]
			else:
				self.content += diccio[-tecla]
			if len(self.content)>1 and self.content[-2]==u'ç' and self.content[-1] in 'AEIUOeaiuo':
				self.content = self.content[:-2] + acentuar[self.content[-1]]
		elif tecla != 8:
			print tecla
		if tecla == K_KP_ENTER:
			self.content += ':('

class Lista:
	def __init__(self, posicion, size, cnt, fsize = 20, fcolor = NABLA, actions = []):
		n = len(cnt)
		img_aux = Image.new('RGB', (size[0] + 2*ESQ, size[1] + 2*ESQ), 'black')
		for jj in range(-1, 1):
			for ii in range(size[0]):
				img_aux.putpixel((ii + ESQ, jj + ESQ/2), fcolor)
				img_aux.putpixel((ii + ESQ, size[1] + 3*ESQ/2 - 1 - jj), fcolor)
			for ii in range(size[1]):
				img_aux.putpixel((jj + ESQ/2, ii + ESQ), fcolor)
				img_aux.putpixel((size[0] + 3*ESQ/2 - 1 - jj, ii + ESQ), fcolor)
		for vx, vy, matriz in [(0, 0, MAT_ESQ),
		(size[0] + ESQ, 0, [[MAT_ESQ[jj][ESQ - 1 - ii] for jj in range(ESQ)] for ii in range(ESQ)]),
		(size[0] + ESQ, size[1] + ESQ, [[MAT_ESQ[ESQ - 1 - ii][ESQ - 1 - jj] for jj in range(ESQ)] for ii in range(ESQ)]),
		(0, size[1] + ESQ, [[MAT_ESQ[ESQ - 1 - jj][ii] for jj in range(ESQ)] for ii in range(ESQ)])]:
			for ii in range(ESQ):
				for jj in range(ESQ):
					img_aux.putpixel((ii + vx, jj + vy), tuple([int(tt*matriz[ii][jj]) for tt in fcolor[:3]]))
		for jj in range(1, n):
			for ii in range(size[0]+ESQ):
				img_aux.putpixel((ii + ESQ/2, ESQ/2+int((size[1]+ESQ)*jj/n)), fcolor)
		path_aux = 'l_image_' + str(posicion[0]) + '_' + str(posicion[1]) + '.png'
		img_aux.save(PATH + 'img/' + path_aux)
		self.fondo = Imagen(path_aux)
		self.posicion = posicion
		self.size = size
		self.content = cnt
		self.fuente = 'courier'
		self.fsize = fsize
		self.fcolor = fcolor
		self.centers = [self.posicion[1]-ESQ/2 + int(0.5+(2*ii+1.)*(self.size[1]+ESQ)/(2.*n)) for ii in range(n)]
		self.acts = [n00 for ii in range(n)]
		if actions:
			self.acts = actions
	def poner(self, writing = False):
		self.fondo.poner(self.posicion[0]-ESQ, self.posicion[1]-ESQ)
		n = len(self.content)
		for ii in range(n):
			chain = []
			elem = ''
			for item in (self.content[ii] + writing*wrr()).split(' '):
				if (len(elem) + len(item))*self.fsize/1.5 > self.size[0] + ESQ - 6:
					chain.append(elem)
					elem = item
					continue
				elem = elem  + ' '*(elem != '') + item
			chain.append(elem)
			poner_texto(chain, self.fsize, self.fuente, self.fsize, (self.posicion[0] + self.size[0]/2, self.centers[ii]), self.fcolor)
	def clicar(self, mousex, mousey):
		if (mousex > self.posicion[0] - ESQ/2 and mousey > self.posicion[1] - ESQ/2
		 and mousex - self.posicion[0] < self.size[0] + ESQ/2 and mousey - self.posicion[1] < self.size[1] + ESQ/2):
			n = len(self.content)
			num = int(n*(mousey-self.posicion[1] + ESQ/2)/(self.size[1]+ESQ))
			self.acts[num]()

def giro(p, xx, yy, zz, cc, ss):
	res = [(cc + xx*xx*(1 - cc))*p[0] + (xx*yy*(1 - cc) - zz*ss)*p[1] + (xx*zz*(1 - cc) + yy*ss)*p[2]]
	res.append((xx*yy*(1 - cc) + zz*ss)*p[0] + (cc + yy*yy*(1 - cc))*p[1] + (yy*zz*(1 - cc) - xx*ss)*p[2])
	return res + [(xx*zz*(1 - cc) - yy*ss)*p[0] + (yy*zz*(1 - cc) + xx*ss)*p[1] + (cc + zz*zz*(1 - cc))*p[2]]

class Objeto:
	def __init__(self, puntos, lineas, caras, xxx, yyy):
		if xxx == -1:
			xxx = SCREEN_WIDTH/2
		if yyy == -1:
			yyy = SCREEN_HEIGHT/2
		self.puntos = puntos
		self.lineas = lineas
		self.caras = caras
		self.x, self.y = xxx, yyy
	def trasladar(self, vec):
		self.puntos = map(lambda x: [x[ii] + vec[ii] for ii in range(3)], self.puntos)
		#self.puntos = map(lambda x: [ynt(x[ii]*1000 + .5)*.001 for ii in range(3)], self.puntos)
	def girar(self, p0, p1, phi):
		self.trasladar([-el for el in p0])
		p1 = [p1[ii] - p0[ii] for ii in range(3)]
		nor = math.sqrt(sum(map(lambda x: x*x, p1)))
		xx, yy, zz = map(lambda x: x/nor, p1)
		cc = math.cos(phi)
		ss = math.sin(phi)
		self.puntos = map(lambda x: giro(x, xx, yy, zz, cc, ss), self.puntos)
		self.trasladar(p0)
	def escalar(self, k, ori = [0, 0, 0]):
		self.puntos = map(lambda x: [ori[ii] + k*(x[ii] - ori[ii]) for ii in range(3)], self.puntos)
	def dibujar(self, per = "ortogonal"):
		if per == "ortogonal":
			if self.lineas == []:
				for punto in self.puntos:
					pygame.draw.circle(SCREEN, (0, 0, 255), (ynt(punto[0] + .5) + self.x, ynt(punto[1] + .5) + self.y), 5)
			for linea in self.lineas:
				p1 = self.puntos[linea[0]]
				p2 = self.puntos[linea[1]]
				p1, p2 = map(lambda x: ynt(x + .5), p1), map(lambda x: ynt(x + .5), p2)
				pygame.draw.line(SCREEN, BLANCO, (p1[0] + self.x, p1[1] + self.y), (p2[0] + self.x, p2[1] + self.y), 3)
	def actualizar(self):
		self.girar([0, 0, 0], [1, 1, 1], 0.1)
		self.escalar(0.99 + 0.02*random())

class Marcador:
	def __init__(self, textos, xxx, yyy, start = 0):
		self.textos = textos
		self.x, self.y = xxx, yyy
		self.selected = start
	def poner(self):
		return #en construccion
	def clicar(self):
		return 

def spam_imgs(lis):
	for text, xx, yy in lis:
		if xx == -1:
			xx = SCREEN_WIDTH/2 - text.rect[2]/2
		if yy == -1:
			yy = SCREEN_HEIGHT/2 - text.rect[3]/2
		text.poner(xx, yy)

def terminate():
	pygame.quit()
	sys.exit()

class Pantalla:
	def __init__(self, botones = [], escritores = [], imagenes = [], listas = [], textos = [], objetos = [], kk = []):
		self.elist = escritores
		self.ilist = imagenes
		self.blist = botones
		self.tlist = textos
		self.llist = listas
		self.olist = objetos
		self.shift_pressed = False
		self.selected = -1
		self.del_pressed = False
		self.del_lag = False
		self.kklist = kk
	def poner(self):
		SCREEN.fill(NEGRO)
		spam_imgs(self.ilist)
		for boton in self.blist:
			boton.dibujar()
		for texto in self.tlist:
			texto.poner()
		for ind in range(len(self.elist)):
			ven = self.elist[ind]
			ven.poner(writing = (ind==self.selected))
		for lista in self.llist:
			lista.poner()
		for obj in self.olist:
			obj.dibujar()
		for kk in self.kklist:
			kk.poner()
		pygame.display.update()
	def actualizar(self, mousex, mousey, clic):
		for obj in self.olist:
			obj.actualizar()
		if clic:
			for kk in self.kklist:
				kk.clicar(mousex, mousey)
		if clic:
			for boton in self.blist:
				boton.clicar(mousex, mousey)
			for lis in self.llist:
				lis.clicar(mousex, mousey)
		for ind in range(len(self.elist)):
			ven = self.elist[ind]
			if clic and (mousex > ven.posicion[0] - ESQ/2 and mousey > ven.posicion[1] - ESQ/2 and mousex - ven.posicion[0] < ven.size[0] + ESQ/2 and mousey - ven.posicion[1] < ven.size[1] + ESQ/2):
				self.selected = ind
		if self.selected != -1 and self.del_pressed and self.del_lag<time():
			self.elist[self.selected].escribir(8, False)
	def pulsar(self, tec):
		for kk in self.kklist:
			kk.tecla(tec)
		if tec == K_RSHIFT or tec == K_LSHIFT:
			self.shift_pressed = True
			return
		if tec == 8:
			self.del_pressed = True
			self.del_lag = time()+0.15
		if tec == 27:#Escape
			self.selected = -1
		if self.selected != -1:
			if tec == 9:
				self.selected = (self.selected + 1)%len(self.elist)
			self.elist[self.selected].escribir(tec, self.shift_pressed)
	def soltar(self, tec):
		if tec == K_RSHIFT or tec == K_LSHIFT:
			self.shift_pressed = False
		if tec == 8:
			self.del_pressed = False

class KK_display:
	def __init__(self, kakuro, position):
		self.x, self.y = position
		self.letras = kakuro.get_letras()
		self.clave = [' ']*10
		self.m = kakuro.m
		self.sel = -1
		self.sumas = kakuro.sumas
	def descodificar(self, char):
		if char == ' ':
			return ' '
		if char in self.letras:
			cc = self.clave[self.letras.index(char)]
			if cc == ' ':
				return char
			return cc
		return char
	def descifrar(self, texto):
		try:
			return ''.join([self.descodificar(char) for char in texto])
		except:
			print texto
	def clicar(self, mousex, mousey):
		ii = (mousex - self.x)/45.
		jj = (mousey - self.y)/45.
		if ii>=0 and jj>=0 and ii<len(self.m[0]) and jj<len(self.m):
			if ii-int(ii) < 8/9. and jj - int(jj) < 8/9.:
				ii = int(ii)
				jj = int(jj)
				if self.m[jj][ii] in ' 123456789':
					self.sel = (ii, jj)
		ii = mousex - (self.x + len(self.m[0])*45 + 40)
		jj = mousey - (self.y + 10)
		if ii >= 0 and ii < 28 and jj >= 0 and jj < 350 and jj%35 < 28:
			self.sel = (int(jj/35) , )
	def tecla(self, key):
		if key == K_ESCAPE:
			self.sel = -1
		if self.sel == -1:
			return
		if key == K_BACKSPACE:
			key = K_SPACE
		if key in [K_SPACE, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]:
			if len(self.sel) == 1:
				num = diccio[-key]
				if num in '1234567890 ':
					self.clave[self.sel[0]] = num
			elif len(self.sel) == 2:
				num = diccio[-key]
				if num in '123456789 ': 
					self.m[self.sel[1]][self.sel[0]] = num
		else:
			return
		if ''.join(sorted(list(set(self.clave))))!='0123456789':
			return
		ind1 = 0
		for ii in range(len(self.m)):
			suma1 = 0
			for jj in range(len(self.m[0])):
				if (self.m[ii][jj] == ' '):
					return
				if (self.m[ii][jj] == '#' and suma1>0):
					if (int(self.descifrar(self.sumas[ind1][0])) != suma1):
						return
					suma1 = 0
					ind1 += 1
				if (self.m[ii][jj]!= '#'):
					suma1 = suma1 + int(self.descifrar(self.m[ii][jj]))
		print 'resuelto'
	def poner(self):
		fuente = pygame.font.SysFont('texgyrepagellamath', 30)
		for ii in range(len(self.m[0])):
			for jj in range(len(self.m)):
				if self.m[jj][ii] != '#':
					SCREEN.fill(NABLA, [self.x + ii*45, self.y + jj*45, 39, 39])
					if self.sel == (ii, jj):
						SCREEN.fill(CIELO, [self.x + self.sel[0]*45, self.y + self.sel[1]*45, 39, 39])
						SCREEN.fill(NABLA, [self.x + self.sel[0]*45 + 2, self.y + self.sel[1]*45 + 2, 35, 35])
					texto = fuente.render(self.descifrar(self.m[jj][ii]), True, NEGRO)
					dx = texto.get_rect().width/2
					dy = texto.get_rect().height/2
					SCREEN.blit(texto, texto.get_rect().move(self.x + ii*45 + 19 - dx, self.y + jj*45 + 22 - dy))
		fuente2 = pygame.font.SysFont('arial', 12)
		for suma, casillas in self.sumas:
			texto = fuente2.render(self.descifrar(suma), True, NABLA)
			dx = texto.get_rect().width/2
			dy = texto.get_rect().width/2
			if casillas[0][1] == casillas[-1][1]:
				SCREEN.blit(texto, texto.get_rect().move(self.x + casillas[0][1]*45 - dx + 20, self.y + casillas[0][0]*45 - 16))
				SCREEN.blit(texto, texto.get_rect().move(self.x + casillas[-1][1]*45 - dx + 20, self.y + casillas[-1][0]*45 + 44))
			elif casillas[0][0] == casillas[-1][0]:
				SCREEN.blit(texto, texto.get_rect().move(self.x + casillas[0][1]*45 - dx - 10, self.y + casillas[0][0]*45 + 15))
				SCREEN.blit(texto, texto.get_rect().move(self.x + casillas[-1][1]*45 - dx + 50, self.y + casillas[-1][0]*45 + 15))
			else:
				print 'Error en las sumas'
		fuente3 = pygame.font.SysFont('texgyrepagellamath', 20)
		for ii in range(10):
			texto = fuente3.render(self.letras[ii] + '=', True, NABLA)
			dx = texto.get_rect().width/2
			SCREEN.blit(texto, texto.get_rect().move(self.x + len(self.m[0])*45 + 25 - dx, self.y + 35*ii + 15))
			SCREEN.fill(NABLA, [self.x + len(self.m[0])*45 + 40, self.y + 35*ii + 10, 28, 28])
			if self.sel == (ii, ):
				SCREEN.fill(CIELO, [self.x + len(self.m[0])*45 + 40, self.y + 35*self.sel[0] + 10, 28, 28])
				SCREEN.fill(NABLA, [self.x + len(self.m[0])*45 + 42, self.y + 35*self.sel[0] + 12, 24, 24])
			texto2 = fuente3.render(self.clave[ii], True, NEGRO)
			SCREEN.blit(texto2, texto2.get_rect().move(self.x + len(self.m[0])*45 + 50, self.y + 35*ii + 15))


#Funciones locales

icono_img = Imagen('icon.png')

def creador():
	print "Creando KK"
	time0 = time()
	newkakuro = crear()
	cc = 1
	for root, dirs, files in os.walk(PATH + "puzzles/"):
		for log in files:
			cc += 1
	newkakuro.guardar(PATH + 'puzzles/kk0000'[:-len(str(cc))]+str(cc)+'.txt')
	print "KK creado"
	print 'Tiempo total: ', '%.1f'%(time()-time0), "segundos"

#Funciones principales

def main():
	global FPSCLOCK, SCREEN
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	pygame.display.set_icon(icono_img.area)
	SCREEN = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption('Krypto Kakuro')
	runGame()


def runGame():
	global creando, kkactual
	creando = False
	hilo = -1
	kkactual = 11
	kakuro1 = cargar(PATH + 'puzzles/kk0011.txt')[0]
	mykklis = [KK_display(kakuro1, [0, 0])]
	def comenzar():
		global creando
		creando = 1-creando
		if creando:
			BOTONES[0] = Boton(450, 40, get_text(u'Detener', False, ROJO, 'Arial', 20), comenzar)
		else:
			BOTONES[0] = Boton(450, 40, get_text(u'Generar', False, NABLA, 'Arial', 20), comenzar)
	def nada():
		pass
	def cargar_kk():
		global kkactual
		kakuro1 = cargar(PATH + 'puzzles/kk0000'[:-len(str(kkactual))]+str(kkactual)+".txt")[0]
		mykklis[0] = KK_display(kakuro1, [0, 0])
		TEXTOS[0].content = "KK: "+ str(kkactual)
	def atras():
		global kkactual
		kkactual = max(1, kkactual - 1)
		cargar_kk()
	def alante():
		cc = 0
		for root, dirs, files in os.walk(PATH + "puzzles/"):
			for log in files:
				cc += 1
		global kkactual
		kkactual = min(cc, kkactual + 1)
		cargar_kk()
	def aleatorio():
		return 0
	def no_resuelto():
		return 0
	BOTONES = [Boton(450, 40, get_text(u'Generar', False, NABLA, 'Arial', 20), comenzar),
	Boton(200, 400, Imagen('leftarrow.png'), atras, padding = 5),
	Boton(350, 400, Imagen('rightarrow.png'), alante, padding = 5)]
	VENTANAS = []
	IMAGENES = []
	LISTADO = []
	TEXTOS = [Texto([260, 400], 'KK: 11', "Arial", 20, NABLA, False)]
	OPCIONES = []
	mipan = Pantalla(botones = BOTONES, escritores = VENTANAS, imagenes = IMAGENES, textos = TEXTOS, listas = LISTADO, kk = mykklis)
	mousex, mousey = 0, 0
	mouseclic = False
	while True:
		FPSCLOCK.tick(FPS)
		mouseclic = False
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYUP:
				mipan.soltar(event.key)
			elif event.type == KEYDOWN:
				mipan.pulsar(event.key)
				mykklis[0].tecla(event.key)
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseclic = True
		mipan.poner()
		mipan.actualizar(mousex, mousey, mouseclic)
		if creando == True:
			if hilo == -1:
				hilo = threading.Thread(target = creador)
				hilo.start()
			elif hilo.isAlive()==False:
				hilo = threading.Thread(target = creador)
				hilo.start()

if __name__ == "__main__":
	main()
