import sys, random
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
import pandas as pd

df =  pd.read_csv('../Crash Statistics Victoria.csv')
# df = df[:100].groupby('ACCIDENT_DATE')['ACCIDENT_DATE'].transform('count')

df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'])
df = df.loc[df['ACCIDENT_DATE'].between('2013-7-1','2013-7-13', inclusive=True)]

dates  = []
counts = []
max_acc  = 0

for val, cnt in df['ACCIDENT_DATE'].value_counts().iteritems():
	dates.append(str(val)[:10])
	counts.append(cnt/24)

max_acc =  int(max(counts)*24)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.resize(800, 600)

		set0 = QBarSet('Dates')

		set0.append(counts)

		series = QBarSeries()
		series.append(set0)

		chart = QChart()
		chart.addSeries(series)
		chart.setTitle('Bar Chart Demo')
		chart.setAnimationOptions(QChart.SeriesAnimations)

		months = dates

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

if __name__ == '__main__':
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())