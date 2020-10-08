import sys, random
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
import pandas as pd


class CrashChart(QMainWindow):
	def __init__(self, parent=None, data=None):
		super(CrashChart, self).__init__(parent)

		self.resize(800, 600)
		set0 = QBarSet(data['x_label'])
		set0.append(data['y_axis'])
		max_acc =  int(max(data['y_axis']))
		series = QBarSeries()
		series.append(set0)
		chart = QChart()
		chart.addSeries(series)
		chart.setTitle(data['title'])
		chart.setAnimationOptions(QChart.SeriesAnimations)
		months = data['x_axis']
		axisX = QBarCategoryAxis()
		axisX.append(months)
		axisY = QValueAxis()
		axisY.setRange(0, max_acc)
		chart.addAxis(axisX, Qt.AlignBottom)
		chart.addAxis(axisY, Qt.AlignLeft)
		chart.legend().setVisible(True)
		chart.legend().setAlignment(Qt.AlignBottom)
		chartView = QChartView(chart)
		self.setCentralWidget(chartView)


