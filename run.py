## Code to run the main code and connect the user interface and canvas. 
import sys
from canvas import Canvas
from PyQt5 import QtWidgets
from ui import Ui_MainWindow
import pdb

app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
MainWindow = QtWidgets.QMainWindow()
ui.setupUi(MainWindow)
canvas = Canvas(ui, ui.centralwidget)

def connect(ui, canvas):
	ui.clear.clicked.connect(canvas.clear_all)
	ui.sort_points.clicked.connect(canvas.sort_points)
	ui.add_points.stateChanged.connect(canvas.toggle_add_mode)
	ui.bezier.stateChanged.connect(canvas.toggle_bezier_mode)
	ui.bspline.stateChanged.connect(canvas.toggle_bspline_mode)
	ui.linear.stateChanged.connect(canvas.toggle_linear_mode)
	ui.catmull_romm.stateChanged.connect(canvas.toggle_catmull_romm)
	
	ui.zoomInX.clicked.connect(canvas.zoomXIn_call)
	ui.zoomoutX.clicked.connect(canvas.zoomXOut_call)
	ui.zoomInY.clicked.connect(canvas.zoomYIn_call)
	ui.zoomoutY.clicked.connect(canvas.zoomYOut_call)


if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	ui = Ui_MainWindow()
	
	MainWindow = QtWidgets.QMainWindow()
	ui.setupUi(MainWindow)
	canvas = Canvas(ui, ui.centralwidget)

	connect(ui, canvas)
	MainWindow.show()
	sys.exit(app.exec_())
