"""
Author: Abhinav Narayan Harish
Last edited: 10/3/21

-> Canvas is being created to manage interpolation adding and deleting points. 

References: 

1. Code from Assignment:1 - CS 7496 for conducting interactive interpolation. 
2. Polygonal Interactor: https://stackoverflow.com/questions/66301388/2-interactive-poly-editor-with-matplotlib-not-working

"""

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.lines import Line2D


# FigureCanvas being imported here. 
class Canvas(FigureCanvas):
	def __init__(self, second_parent, parent = None, width = 7.3, height = 6, dpi = 100):
		self.figure = Figure(figsize=(width,height), dpi=dpi)
		super(Canvas, self).__init__(self.figure)
		self.setParent(parent)

		self.ax = self.figure.add_subplot(111)
		self.second_parent = second_parent
		self.parent = parent

		self.inter_flag = False
		self.x_data = []
		self.y_data = []

		# points being set up here.
		self.points = self.ax.scatter([], [], s=200, color='blue', animated=True)
		self.constraint_list = []

		# Setting axes limits.
		self.xmin = -100
		self.ymin = -100
		self.xmax = 100
		self.ymax = 100

		# Axes xmin and xmax, ymin and ymax.
		self.ax.set_xlim((self.xmin, self.xmax))
		self.ax.set_ylim((self.ymin, self.ymax))

		# Button press and key press event. 
		self.cid1 = self.mpl_connect("button_press_event", self.click)
		self.cid2 = self.mpl_connect("key_press_event", self.key_press_callback)
		self.cid3 = self.mpl_connect("motion_notify_event", self.mouse_move)
		self.cid4 = self.mpl_connect("button_release_event", self.mouse_release)
		self.draw_cid = self.mpl_connect('draw_event', self.grab_background)

		# Tolerance for point selection. 
		self._idx = None
		self.eps = 5

		# Minimum number of points in each spline. 
		self.POINTS_MIN = 1
		self.LINE_MIN = 2
		self.BEZIER_MIN = 4
		self.BSPLINE_MIN = 4
		self.CATMULL_ROMM_MIN = 4

		# States of each of the files. 
		self.linear_state = False
		self.bezier_state = False
		self.bspline_state = False
		self.catmull_romm_state = False
		self.add_mode = False

		# 4 different splines. 
		self.line_inter = Line2D([], [], color='red')
		self.line_bezier = Line2D([], [], color = 'green')
		self.line_bspline = Line2D([], [], color = 'orange')
		self.line_catmull_romm = Line2D([], [], color = 'black')

		# Adding line_inter, bezier, b-spline and catmull-romm. 
		self.ax.add_line(self.line_inter)
		self.ax.add_line(self.line_bezier)
		self.ax.add_line(self.line_bspline)
		self.ax.add_line(self.line_catmull_romm)

		# Figure canvas obtained here. 
		self.figure.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
		self.figure.canvas.setFocus()

	# Catmull-romm interpolation using x-data and y-data. 
	def catmullrom_interpolation_of_points(self):
		interpolated_points = list()
		control_points = np.hstack((np.array([self.x_data]).T, np.array([self.y_data]).T))
		time_array = np.linspace(0.0, 1.0, 101)  # time[0] = 0.0, time[1] = 0.01, ... time[100] = 1.0
		for i in range(0, len(control_points) - 3, 1):
			p0, p1, p2, p3 = control_points[i:i + 4]
			points = [self.catmullrom_interpolation_at_t(p0, p1, p2, p3, t) for t in time_array]
			interpolated_points += points
		
		interpolated_points = np.array(interpolated_points)
		return interpolated_points[:, 0], interpolated_points[:, 1]

	def catmullrom_interpolation_at_t(self, p0, p1, p2, p3, t):
		"""All the points are given as np.array. t is a floating number that represents time."""
		# Student answer begins  
		T = np.array((t ** 3, t ** 2, t, 1.0))
		M = np.array([[-1.0, 3.0, -3.0, 1.0],
						[2.0, -5.0, 4.0, -1.0],
						[-1.0, 0.0, 1.0, 0.0],
						[0.0, 2.0, 0.0, 0.0]]) / 2.0
		G = np.vstack((p0, p1, p2, p3))
		return T.dot(M).dot(G)

	# Linear interpolation of points. 
	def linear_interpolation_of_points(self):
		control_points = np.hstack((np.array([self.x_data]).T, np.array([self.y_data]).T))
		interpolated_points = list()  
		time_array = np.linspace(0.01, 0.99, 100)

		for p0, p1 in zip(control_points[:-1], control_points[1:]):
			# time_array = np.linspace(0.01, 0.99, 100)
			points = [self.linear_interpolation_at_t(p0, p1, t) for t in time_array]
			interpolated_points += points

		interpolated_points = np.array(interpolated_points)
		return interpolated_points[:, 0], interpolated_points[:, 1]

	def linear_interpolation_at_t(self, p0, p1, t):
		assert 0 <= t <= 1 
		return (1 - t) * p0 + t * p1


	def bezier_interpolation_of_points(self):
		control_points = np.hstack((np.array([self.x_data]).T, np.array([self.y_data]).T))
		interpolated_points = []
		time_array = np.linspace(0.0, 1.0, 101)
		for i in range(0, len(control_points) - 3, 3):
			p0, p1, p2, p3 = control_points[i:i + 4]
			points = [self.bezier_interpolation_at_t(p0, p1, p2, p3, t) for t in time_array]
			interpolated_points += points
		
		interpolated_points = np.array(interpolated_points)
		return interpolated_points[:, 0], interpolated_points[:, 1]

	def bezier_interpolation_at_t(self, p0, p1, p2, p3, t):

		T = np.array((t ** 3, t ** 2, t, 1.0))
		M = np.array([[-1.0, 3.0, -3.0, 1.0],
				[3.0, -6.0, 3.0, 0.0],
				[-3.0, 3.0, 0.0, 0.0],
				[1.0, 0.0, 0.0, 0.0]])
		G = np.vstack((p0, p1, p2, p3))
		return T.dot(M).dot(G)

	def bspline_interpolation_of_points(self):
		control_points = np.hstack((np.array([self.x_data]).T, np.array([self.y_data]).T))
		interpolated_points = list()
		time_array = np.linspace(0.0, 1.0, 101)  # time[0] = 0.0, time[1] = 0.01, ... time[100] = 1.0
		for i in range(0, len(control_points) - 3, 1):
		   p0, p1, p2, p3 = control_points[i:i + 4]
		   points = [self.bspline_interpolation_at_t(p0, p1, p2, p3, t) for t in time_array]
		   interpolated_points += points
		interpolated_points = np.array(interpolated_points)

		# Returning interpolated points. 
		return interpolated_points[:, 0], interpolated_points[:, 1]
	

	def bspline_interpolation_at_t(self, p0, p1, p2, p3, t):

		T = np.array((t ** 3, t ** 2, t, 1.0))
		M = np.array([[-1.0, 3.0, -3.0, 1.0],
				[3.0, -6.0, 3.0, 0.0],
				[-3.0, 0.0, 3.0, 0.0],
				[1.0, 4.0, 1.0, 0.0]]) / 6.0
		G = np.vstack((p0, p1, p2, p3))
		return T.dot(M).dot(G)

	# delete point depending on whether it is close or not. 
	def delete_point(self, event):
		self.get_closest_index(event)
		if self._idx is not None:
			self.x_data.pop(self._idx)
			self.y_data.pop(self._idx)
			# print("The length of x data is", len(self.x_data))
			self._idx = None

		self.update_all_components()

	# Grabbing point background. 
	def grab_background(self, event=None):
		# self.points.set_visible(False)
		# self.safe_draw()
		self.background = self.figure.canvas.copy_from_bbox(self.figure.bbox)
		# self.points.set_visible(True)
		self.blit()

	# Clear all points. 
	def clear_all(self, event=None):
		self.x_data = []
		self.y_data = []

		self.ax.set_xlim(self.xmin, self.xmax)
		self.ax.set_ylim(self.ymin, self.ymax)
		# self.draw()
		self.update_all_components()

	# Change add mode. 
	def change_add_mode(self):
		self.add_mode = not self.add_mode

	# Key press callback. 
	def key_press_callback(self, event):
		if not event.inaxes:
			return

		if event.key == 'd':
			self.delete_point(event)
		
		if event.key == 'i':
			self.linear_state = not self.linear_state
			self.update_line()
			
		if event.key == 'b':
			self.bezier_state = not self.bezier_state
			self.update_bezier()

		if event.key == 'c':
			self.clear_all()

		if event.key == 'a':
			self.add_mode = not self.add_mode

	# zoom callback. 
	def zoomXIn_call(self):
		self.zoom_x(5)

	def zoomXOut_call(self):
		self.zoom_x(-5)

	def zoomYIn_call(self):
		self.zoom_y(5)

	def zoomYOut_call(self):
		self.zoom_y(-5)

	def zoom_x(self, value):
		bottom_x_lim = self.ax.get_xlim()[0]
		top_x_lim = self.ax.get_xlim()[1]

		bottom_x_lim += value
		top_x_lim -= value

		self.ax.set_xlim(bottom_x_lim, top_x_lim)
		# self.draw()
		self.update_all_components()

	def zoom_y(self, value):
		bottom_y_lim = self.ax.get_ylim()[0]
		top_y_lim = self.ax.get_ylim()[1]

		bottom_y_lim += value
		top_y_lim -= value

		self.ax.set_ylim(bottom_y_lim, top_y_lim)
		# self.draw()
		self.update_all_components()

	# def zoomOutCallback(self, value):
	# 	self.zoomIn(-5)

	def mouse_move(self, event):
		if not event.inaxes:
			return
		# Second parent. 
		self.second_parent.lcdNumber.display(int(100*event.xdata)/100.)	
		self.second_parent.lcdNumber_2.display(int(100*event.ydata)/100.) 

		if self._idx is None:
			return

		x, y = event.xdata, event.ydata

		self.x_data[self._idx] = x
		self.y_data[self._idx] = y 
		

		self.update_all_components()

	# Total add mode. 
	def toggle_add_mode(self):
		self.add_mode = not self.add_mode

	def toggle_linear_mode(self):
		self.linear_state = not self.linear_state
		self.update_line()

	# Toggling bezier and b-spline. 
	def toggle_bezier_mode(self):
		self.bezier_state = not self.bezier_state
		self.update_bezier()

	# Toggling b-spline mode as on and off. 
	def toggle_bspline_mode(self):
		self.bspline_state = not self.bspline_state
		# print("B-spline toggle", self.bspline_state)
		self.update_bspline()

	def toggle_catmull_romm(self):
		self.catmull_romm_state = not self.catmull_romm_state
		# print("Catmull Romm toggle")
		self.update_catmull_romm()

	# Update all components. 
	def update_all_components(self):
		self.update_points()
		self.update_line()
		self.update_bezier()
		self.update_bspline()
		self.update_catmull_romm()
		self.draw_figure()

	# Mouse being released. 
	def mouse_release(self, event):
		# print("Mouse release")
		self._idx = None

	# Get closest index to the event. 
	def get_closest_index(self, event):
		# print("Get get_closest_index ")
		if not event.inaxes:
			return
		pts_array = np.hstack((np.array([self.x_data]).T, np.array([self.y_data]).T))
		cur_loc = np.array([[event.xdata, event.ydata]])
		# print(pts_array, cur_loc)
		dist = np.sqrt(np.sum((cur_loc - pts_array)**2, axis=1))
		# print("dist", dist)
		if len(dist) > 0:
			min_loc  = np.argmin(dist)
			if dist[min_loc] < self.eps:
				self._idx = min_loc
			else:
				self._idx = None
		else:
			self._idx = None

		# print(self._idx)

	def add_point(self, event):
		if not event.inaxes:
			return 

		xclick = event.xdata
		yclick = event.ydata

		# Checking if add mode is on or not. 
		if self.add_mode and xclick is not None and yclick is not None:
			self.x_data.append(event.xdata)
			self.y_data.append(event.ydata)
		
		self.update_all_components()


	def grab_background(self, event=None):
		self.background = self.copy_from_bbox(self.ax.bbox)

	def update_points(self):
		xy = [[x, y] for (x, y) in zip(self.x_data, self.y_data)]
		self.points.set_offsets(xy)
		self.draw_figure()

	def update_bezier(self):
		if self.bezier_state and len(self.x_data) >= self.BEZIER_MIN:
			xl, yl = self.bezier_interpolation_of_points()
		else:
			xl, yl = [], []

		self.line_bezier.set_data(xl, yl)
		self.draw_figure()

	# Update b-spline. 
	def update_bspline(self):
		if self.bspline_state and len(self.x_data) >= self.BSPLINE_MIN:
			xl, yl = self.bspline_interpolation_of_points()
		else:
			xl, yl = [], []

		self.line_bspline.set_data(xl, yl)
		self.draw_figure()

	# Updating catmull romm points by conducting this process. 
	def update_catmull_romm(self):
		if self.catmull_romm_state and len(self.x_data) >= self.CATMULL_ROMM_MIN:
			xl, yl = self.catmullrom_interpolation_of_points()
		else:
			xl, yl = [], []

		self.line_catmull_romm.set_data(xl, yl)
		self.draw_figure()

	def update_line(self):	
		# print(len(self.x_data))
		if self.linear_state and len(self.x_data) >= self.LINE_MIN:
			control_points = [[x,y] for (x, y) in zip(self.x_data, self.y_data)]
			xl, yl = self.linear_interpolation_of_points()
		else:
			xl, yl = [], []

		self.line_inter.set_data(xl, yl)
		self.draw_figure()

	def sort_points(self):
		sort_idx = np.argsort(self.x_data)
		self.x_data = [self.x_data[idx] for idx in sort_idx]
		self.y_data = [self.y_data[idx] for idx in sort_idx]
		self.update_all_components()

	def draw_figure(self):
		self.figure.canvas.restore_region(self.background)

		if len(self.x_data) >= self.POINTS_MIN:
			self.ax.draw_artist(self.points)
		
		if len(self.x_data) >= self.LINE_MIN:
			self.ax.draw_artist(self.line_inter)
		
		if len(self.x_data) >= self.BEZIER_MIN:
			self.ax.draw_artist(self.line_bezier)

		if len(self.x_data) >= self.BSPLINE_MIN:
			self.ax.draw_artist(self.line_bspline)

		if len(self.x_data) >= self.CATMULL_ROMM_MIN:
			self.ax.draw_artist(self.line_catmull_romm)

		self.figure.canvas.blit(self.figure.bbox)

	# Clicked. 
	def click(self, event):
		self.get_closest_index(event)
		# print("Mouse clicked", self._idx)

		if self._idx == None:
			self.add_point(event)