import sys
from PyQt4 import QtGui, uic, QtCore
from enum import Enum

class MyWindow(QtGui.QMainWindow) :

	def __init__(self):
		super(MyWindow, self).__init__()
		self.viboras = []

		self.ui = uic.loadUi('servidor.ui', self)
		self.escucha_tamaño_tabla()
		self.timer_actualiza_juego = QtCore.QTimer(self)
		self.actualiza_espera()          
		self.timer_actualiza_juego.timeout.connect(self.actualizar_juego)
		self.timer_actualiza_juego.start()
		self.ui.spin_espera.valueChanged.connect(self.actualiza_espera)

		self.first_click = True
		self.ui.button_inicar_juego.clicked.connect(self.handle_boton_iniciar)

		self.show()

	def handle_boton_iniciar(self) :
		if not self.first_click  :
			return
		self.vibora = Vibora()
		for [x,y] in vibora.cuerpo() :
			self.colorear(x,y)

		self.colorear()
		self.button_terminar_juego = QtGui.QPushButton('Terminar juego', self)
		self.button_terminar_juego.clicked.connect(self.terminar_juego)
		self.ui.gridLayout.addWidget(self.button_terminar_juego)
		self.ui.button_inicar_juego.setText("Pausar juego")
		self.ui.button_inicar_juego.clicked.connect(self.pausar_juego)
		self.comenzar_vibora()
		self.first_click = False

	def colorear(x, y) :
		if self.ui.table_board.item(x,y) != 0 :
			pass

	def comenzar_vibora() :
		pass

	def pausar_juego(self) :
		self.timer_actualiza_juego.stop()
		self.ui.button_inicar_juego.setText("Reanudar juego")
		self.ui.button_inicar_juego.clicked.connect(self.reanudar_juego)

	def terminar_juego(self) :
   		pass

	def reanudar_juego(self) :
		self.timer_actualiza_juego.start()  
		self.ui.button_inicar_juego.setText("Pausar juego")
		self.ui.button_inicar_juego.clicked.connect(self.pausar_juego) 	

	def actualizar_juego(self) :
		pass

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
		columnas_actuales = self.ui.table_board.columnCount()
		n = abs(columnas_actuales - columnas_pedidas)
		if columnas_actuales < columnas_pedidas :
			accion, siguiente = self.ui.table_board.insertColumn, 1 
		else :
			accion, siguiente = self.ui.table_board.removeColumn, -1
		for i in range(n) :
			accion(columnas_actuales)
			columnas_actuales += siguiente

		self.ui.table_board.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

	def modifica_filas(self) :
		filas_pedidas = int(self.ui.spin_filas.text())
		filas_actuales = self.ui.table_board.rowCount()
		n = abs(filas_actuales - filas_pedidas)
		if filas_actuales < filas_pedidas :
			accion, siguiente = self.ui.table_board.insertRow, 1 
		else :
			accion, siguiente = self.ui.table_board.removeRow, -1
		for i in range(n) :
			accion(filas_actuales)
			filas_actuales += siguiente

		self.ui.table_board.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

class Vibora() :

	def __init__(self) :
		self.identificador = 0
		self.longitud = 5
		self.cuerpo = [[0,0],[1,0],[2,0],[3,0],[4,0]]#lista de tuplas, donde cada tupla son (x,y) coordenadas en la tabla. Tupla en posicion 0 es cabeza
		self.direccion = Direccion.abajo

	def avanza(self) :
		""" 
		de la cola hasta antes de la cabeza todos avanzan a la posicion en 
		la que se encuentra la siguiente parte del cuerpo, la cabeza se mueve segun 
		la direccion de la serpiente (despues de actualizar la direccion si es que hubo cambios)

		si las nuevas coordenadas de la cabeza ya pertenecen a alguna parte del cuerpo
		distinta a la cabeza, la serpiente muere (porque se comio)"""
		for i in range(self.longitud-1, 0, -1) :



	def modifica_direccion(self) :
		"""segun lo que marque el key-press-event de las flechas del teclado, si no hubo cambios la 
		direccion no se modifica. Si la direccion es invalida la direccion no se modifica"""
		pass



class Direccion(Enum):
	arriba = 0
	abajo = 1
	izquierda = 2
	derecha = 3


if __name__ == '__main__' :
	app = QtGui.QApplication(sys.argv)
	window = MyWindow()
	sys.exit(app.exec_())