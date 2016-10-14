import sys
from PyQt4 import QtGui, uic, QtCore
from enum import Enum

class MyWindow(QtGui.QMainWindow) :

	def __init__(self):
		super(MyWindow, self).__init__()
		self.vibora = Vibora()
		self.ui = uic.loadUi('servidor.ui', self)		
		self.ui.table_board.keyPressEvent = self.keyPressEvent_board
		self.escucha_tamaño_tabla()
		self.timer_actualiza_juego = QtCore.QTimer(self)
		self.actualiza_espera()          
		self.timer_actualiza_juego.timeout.connect(self.actualizar_juego)
		self.timer_actualiza_juego.start()
		self.ui.spin_espera.valueChanged.connect(self.actualiza_espera)
		self.board_seleccionado = False
		self.en_juego = False
		self.first_click = True
		self.ui.button_inicar_juego.clicked.connect(self.handle_boton_iniciar)		
		self.show()

	def handle_boton_iniciar(self) :
		if not self.first_click  :
			return
		self.vibora = Vibora()
		self.colorear_vibora(100,149,237)
		self.en_juego = True
		self.button_terminar_juego = QtGui.QPushButton('Terminar juego', self)
		self.button_terminar_juego.clicked.connect(self.terminar_juego)
		self.ui.gridLayout.addWidget(self.button_terminar_juego)
		self.ui.button_inicar_juego.setText("Pausar juego")
		self.ui.button_inicar_juego.clicked.connect(self.pausar_juego)
		self.first_click = False

	def colorear_vibora(self, r, g, b) :
		for [x,y] in self.vibora.cuerpo :
			self.colorear(x,y,r, g, b)

	def colorear(self, x, y, r, g, b) :
		if self.ui.table_board.item(x,y) == None :
			cell = QtGui.QTableWidgetItem()
			self.ui.table_board.setItem(x, y, cell)
		color = QtGui.QColor(r,g,b)
		try :
			self.ui.table_board.item(x,y).setBackground(QtGui.QBrush(color))
		except :
			#si hubo un error es porque el item en dicha posicion no existia. No hacemos nada
			pass

	def descolorear(self, x, y) :
		self.colorear(x, y, 255, 255, 255)

	def pausar_juego(self) :
		self.timer_actualiza_juego.stop()
		self.en_juego = False
		self.ui.button_inicar_juego.setText("Reanudar juego")
		self.ui.button_inicar_juego.clicked.connect(self.reanudar_juego)

	def terminar_juego(self) :
		self.timer_actualiza_juego.stop()
		self.ui.button_inicar_juego.clicked.connect(self.deshabilita)		
		self.en_juego = False
		self.borrar_vibora() 

	def borrar_vibora(self) :
		self.colorear_vibora(255, 255, 255)


	def reanudar_juego(self) :
		self.timer_actualiza_juego.start()  
		self.en_juego = True
		self.ui.button_inicar_juego.setText("Pausar juego")
		self.ui.button_inicar_juego.clicked.connect(self.pausar_juego)

	def deshabilita(self):
		return

	def actualizar_juego(self) :
		if not self.vibora.viva :
			self.terminar_juego()
		if self.en_juego :
			self.mueve_serpiente()

	def mueve_serpiente(self) :
		coordenadas_cola = self.vibora.cola
		self.descolorear(coordenadas_cola[0], coordenadas_cola[1])
		self.vibora.avanza()
		self.colorear_vibora(100,149,237)

	def actualiza_espera(self) :
		espera = int(self.ui.spin_espera.text())
		self.timer_actualiza_juego.setInterval(espera)

	def escucha_tamaño_tabla(self) :
		self.inicializa_tabla()
		self.ui.spin_columnas.valueChanged.connect(self.modifica_columnas)
		self.ui.spin_filas.valueChanged.connect(self.modifica_filas)

	def inicializa_tabla(self) :
		self.ui.table_board.setRowCount(int(self.ui.spin_filas.text()))
		self.ui.table_board.setColumnCount(int(self.ui.spin_columnas.text()))
		self.ui.table_board.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		self.ui.table_board.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

	def modifica_columnas(self) :
		columnas_pedidas = int(self.ui.spin_columnas.text())
		self.vibora.actualizar_tamaño_ancho(columnas_pedidas)
		columnas_actuales = self.ui.table_board.columnCount()
		n = abs(columnas_actuales - columnas_pedidas)
		if columnas_actuales < columnas_pedidas :
			accion, siguiente = self.ui.table_board.insertColumn, 1 
		else :
			accion, siguiente = self.ui.table_board.removeColumn, -1
		for i in range(n) :
			accion(columnas_actuales-1)
			columnas_actuales += siguiente		
		self.ui.table_board.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

	def modifica_filas(self) :
		filas_pedidas = int(self.ui.spin_filas.text())
		self.vibora.actualizar_tamaño_alto(filas_pedidas)
		filas_actuales = self.ui.table_board.rowCount()
		n = abs(filas_actuales - filas_pedidas)
		if filas_actuales < filas_pedidas :
			accion, siguiente = self.ui.table_board.insertRow, 1 
		else :
			accion, siguiente = self.ui.table_board.removeRow, -1
		for i in range(n) :
			accion(filas_actuales-1)
			filas_actuales += siguiente		
		self.ui.table_board.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

	def keyPressEvent_board(self, eventQKeyEvent) :
		key = eventQKeyEvent.key()
		if key == QtCore.Qt.Key_Left:
			if self.movimiento_valido(Direccion.izquierda) :
				self.vibora.direccion = Direccion.izquierda
		elif key == QtCore.Qt.Key_Up:
			if self.movimiento_valido(Direccion.arriba) :
				self.vibora.direccion = Direccion.arriba
		elif key == QtCore.Qt.Key_Right:
			if self.movimiento_valido(Direccion.derecha) :
				self.vibora.direccion = Direccion.derecha
		elif key == QtCore.Qt.Key_Down:
			if self.movimiento_valido(Direccion.abajo) :
				self.vibora.direccion = Direccion.abajo

	def movimiento_valido(self, direccion) :
		if direccion == Direccion.arriba or direccion == Direccion.abajo :
			return self.vibora.direccion == Direccion.izquierda or self.vibora.direccion == Direccion.derecha
		else :
			return self.vibora.direccion == Direccion.arriba or self.vibora.direccion == Direccion.abajo

class Vibora() :

	def __init__(self) :
		self.identificador = 0
		self.longitud = 5
		self.viva = True
		self.cuerpo = [[0,0],[1,0],[2,0],[3,0],[4,0]]#lista de listas, donde cada lista son (x,y) coordenadas en la tabla. Lista en posicion 0 es cola
		self.direccion = Direccion(1)
		self.cola = self.cuerpo[0]
		self.cabeza = self.cuerpo[-1]
		self.ancho_tablero = 20
		self.alto_tablero = 20

	def avanza(self) :
		for i in range(self.longitud-1) :
			self.cuerpo[i] = self.cuerpo[i+1][:]

		if self.direccion == Direccion.arriba :
			self.cuerpo[-1][0] = self.cuerpo[-1][0] - 1 if self.cuerpo[-1][0] != 0 else self.alto_tablero-1

		elif self.direccion == Direccion.abajo :
			self.cuerpo[-1][0] = self.cuerpo[-1][0] + 1 if self.cuerpo[-1][0] != self.alto_tablero-1 else 0

		elif self.direccion == Direccion.izquierda :
			self.cuerpo[-1][1] = self.cuerpo[-1][1] - 1 if self.cuerpo[-1][1] != 0 else self.ancho_tablero-1

		elif self.direccion == Direccion.derecha :
			self.cuerpo[-1][1] = self.cuerpo[-1][1] + 1 if self.cuerpo[-1][1] != self.ancho_tablero-1 else 0

		self.actualizar_extremos()

		#como es una vibora de longitud 5, el unico caso en el que se puede morir es cuando choca con cola
		if self.cabeza == self.cola :
			self.viva = False

	def actualizar_tamaño_ancho(self, ancho) :
		self.ancho_tablero = ancho
	
	def actualizar_tamaño_alto(self, alto) :
		self.alto_tablero = alto

	def actualizar_extremos(self) :
		self.cola = self.cuerpo[0]
		self.cabeza = self.cuerpo[-1] 



class Direccion(Enum):
	arriba = 0
	abajo = 1
	izquierda = 2
	derecha = 3

if __name__ == '__main__' :
	app = QtGui.QApplication(sys.argv)
	window = MyWindow()
	sys.exit(app.exec_())