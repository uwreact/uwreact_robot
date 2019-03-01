from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

class MainWindow(QMainWindow):

	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("UW React Planning Visualization")



app = QApplication(sys.argv)

window = MainWindow()
window.resize(2000,2000)
window.show()

app.exec_()