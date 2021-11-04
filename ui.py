from PyQt5 import QtCore, QtGui, QtWidgets

# Top level window. 
class TopLevelWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		# self.canvas = Canvas()
		main_window = Window()
		self.setCentralWidget(main_window)

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("Interactive interpolation for splines.")
		MainWindow.resize(920, 600)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		################ Clear canvas ###################

		self.clear = QtWidgets.QPushButton(self.centralwidget)
		self.clear.setGeometry(QtCore.QRect(730, 420, 90, 27))
		self.clear.setObjectName("pushButton")
		# self.clear.clicked.connect(self.canvas.clear_all)

		################ Sort points button ###############

		self.sort_points = QtWidgets.QPushButton(self.centralwidget)
		self.sort_points.setGeometry(QtCore.QRect(830, 420, 90, 27))
		self.sort_points.setObjectName("sortButton")
		# self.sort_points.clicked.connect(self.canvas.sort_points)
	
		############## 	Add points button ################

		self.add_points = QtWidgets.QCheckBox(self.centralwidget)
		self.add_points.setGeometry(QtCore.QRect(760, 90, 121, 22))
		self.add_points.setObjectName("checkBox")
		# self.add_points.stateChanged.connect(self.canvas.toggle_add_mode)

		########### 	Separating lines.  ##################
		
		self.line = QtWidgets.QFrame(self.centralwidget)
		self.line.setGeometry(QtCore.QRect(750, 120, 141, 20))
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setObjectName("line")
		
		self.line_2 = QtWidgets.QFrame(self.centralwidget)
		self.line_2.setGeometry(QtCore.QRect(770, 390, 111, 20))
		self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_2.setObjectName("line_2")
		
		self.line_3 = QtWidgets.QFrame(self.centralwidget)
		self.line_3.setGeometry(QtCore.QRect(760, 290, 131, 20))
		self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_3.setObjectName("line_3")
		
		##############  Zoom in buttons. ######################

		self.zoomInX = QtWidgets.QPushButton(self.centralwidget)
		self.zoomInX.setGeometry(QtCore.QRect(750, 320, 80, 27))
		self.zoomInX.setObjectName("pushButton_2")
		# self.zoomInX.clicked.connect(self.canvas.zoomXIn_call)

		self.zoomoutX = QtWidgets.QPushButton(self.centralwidget)
		self.zoomoutX.setGeometry(QtCore.QRect(830, 320, 80, 27))
		self.zoomoutX.setObjectName("pushButton_3")
		# self.zoomoutX.clicked.connect(self.canvas.zoomXOut_call)

		self.zoomInY = QtWidgets.QPushButton(self.centralwidget)
		self.zoomInY.setGeometry(QtCore.QRect(750, 350, 80, 27))
		self.zoomInY.setObjectName("pushButton_4")
		# self.zoomInY.clicked.connect(self.canvas.zoomYIn_call)

		self.zoomoutY = QtWidgets.QPushButton(self.centralwidget)
		self.zoomoutY.setGeometry(QtCore.QRect(830, 350, 80, 27))
		self.zoomoutY.setObjectName("pushButton_5")
		# self.zoomoutY.clicked.connect(self.canvas.zoomYOut_call)
		
		######################		LCD 	##################################
		
		self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
		self.lcdNumber.setGeometry(QtCore.QRect(750, 470, 61, 23))
		self.lcdNumber.setObjectName("lcdNumber")
		self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
		self.lcdNumber_2.setGeometry(QtCore.QRect(830, 470, 61, 23))
		self.lcdNumber_2.setObjectName("lcdNumber_2")

		self.setLCD()
		
		############## 	Vertical Layout Widget ###############		
		self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(750, 150, 141, 141))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
	
		self.bezier = QtWidgets.QCheckBox(self.verticalLayoutWidget)
		self.bezier.setObjectName("checkBox_3")
		self.verticalLayout.addWidget(self.bezier)
		# self.bezier.stateChanged.connect(self.canvas.toggle_bezier_mode)
		
		# B-spline interpolation. 
		self.bspline = QtWidgets.QCheckBox(self.verticalLayoutWidget)
		self.bspline.setObjectName("checkBox_4")
		self.verticalLayout.addWidget(self.bspline)
		# self.bspline.stateChanged.connect(self.canvas.toggle_bspline_mode)
		
		# Linear interpolation. 
		self.linear = QtWidgets.QCheckBox(self.verticalLayoutWidget)
		self.linear.setObjectName("checkBox_2")
		self.verticalLayout.addWidget(self.linear)
		# self.linear.stateChanged.connect(self.canvas.toggle_linear_mode)

		# Catmull romm widget.
		self.catmull_romm = QtWidgets.QCheckBox(self.verticalLayoutWidget)
		self.catmull_romm.setObjectName("checkBox_5")
		self.verticalLayout.addWidget(self.catmull_romm)
		# self.catmull_romm.stateChanged.connect(self.canvas.toggle_catmull_romm)
		
		# Raising all points. 
		self.clear.raise_()
		self.add_points.raise_()
		self.line.raise_()
		self.line_2.raise_()
		self.line_3.raise_()

		# Raising all zoom functions. 
		self.zoomInX.raise_()
		self.zoomoutX.raise_()
		self.zoomInY.raise_()
		self.zoomoutY.raise_()

		# Vertical layout widget. 
		self.verticalLayoutWidget.raise_()
		self.lcdNumber_2.raise_()
		self.lcdNumber.raise_()
		
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def setLCD(self):
		# Pallete being generated here.
		palette_1 = self.lcdNumber.palette()
		palette_2 = self.lcdNumber_2.palette()
		
		# Setting first pallete colors. 
		palette_1.setColor(palette_1.WindowText, QtGui.QColor(80, 80, 80))
		palette_1.setColor(palette_1.Background, QtGui.QColor(255, 255, 255))
		palette_1.setColor(palette_1.Light, QtGui.QColor(255, 0, 0))
		palette_1.setColor(palette_1.Dark, QtGui.QColor(0, 255, 0))

		# Setting second pallete colors. 
		palette_2.setColor(palette_2.WindowText, QtGui.QColor(80, 80, 80))
		palette_2.setColor(palette_2.Background, QtGui.QColor(255, 255, 255))
		palette_2.setColor(palette_2.Light, QtGui.QColor(255, 0, 0))
		palette_2.setColor(palette_2.Dark, QtGui.QColor(0, 255, 0))

		self.lcdNumber.setPalette(palette_1)
		self.lcdNumber_2.setPalette(palette_2)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate

		# MainWindow is being shown here. 
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.clear.setText(_translate("MainWindow", "Clear"))
		self.sort_points.setText(_translate("MainWindow", "Sort"))
		self.add_points.setText(_translate("MainWindow", "Add Points"))
		
		# Scaling along X and Y direction. 
		self.zoomInX.setText(_translate("MainWindow", "ScaleX(+)"))
		self.zoomoutX.setText(_translate("MainWindow", "ScaleX(-)"))
		
		self.zoomInY.setText(_translate("MainWindow", "ScaleY(+)"))
		self.zoomoutY.setText(_translate("MainWindow", "ScaleY(-)"))

		self.bezier.setText(_translate("MainWindow", "Bezier "))
		self.bspline.setText(_translate("MainWindow", "B-spline"))
		self.linear.setText(_translate("MainWindow", "Linear"))
		self.catmull_romm.setText(_translate("MainWindow", "Catmul-Romm"))
