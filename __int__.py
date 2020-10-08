import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from main import Ui_DataAnalysisTool
import os.path
from os import path
import logging
from chart import CrashChart as ChartWindow
from test import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox

logging.basicConfig(filename='logger.log', level=logging.DEBUG)
app = QtWidgets.QApplication(sys.argv)
DataAnalysisTool = QtWidgets.QMainWindow()
ui = Ui_DataAnalysisTool()
ui.setupUi(DataAnalysisTool)


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


def file_path_decorator(function):
    def wrapper(*args,**kwargs):
        filename = ui.filename.text()
        if path.exists(filename):
            kwargs['data'] = pd.read_csv(filename)
            kwargs['filename'] = filename
            logging.info("file Loaded")
            return function(*args,**kwargs)
        else:
            logging.error("Path not exist")
            QMessageBox.about(DataAnalysisTool, "Alert", "File path not found")
            return None
    return wrapper

def set_datatable(data):
    model = PandasModel(data)
    ui.datatable.setModel(model)


# path validation requried and show message on wrong path.
@file_path_decorator
def load_dataset(*args, **kwargs):
    data = kwargs['data']
    set_datatable(data.head())

@file_path_decorator
def get_data_between_dates(*args, **kwargs):
    df = kwargs['data']
    start_date = ui.startdate.date().toString(QtCore.Qt.ISODate)
    end_date = ui.enddate.date().toString(QtCore.Qt.ISODate)
    df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'])
    mask = (df['ACCIDENT_DATE'] > start_date) & (df['ACCIDENT_DATE'] <= end_date)
    return df.loc[mask]


def set_keyword_date():
    df = get_data_between_dates()
    search = ui.searchinput.text()
    df = df[df['DCA_CODE'].str.contains(search, case=False)]
    set_datatable(df)

def set_date_between_dates():
    data = get_data_between_dates()
    set_datatable(data)

def show_graph(x_axis, y_axis, title, x_label):
    data = {
        "x_axis": x_axis,
        "y_axis": y_axis,
        "title": title,
        "x_label": x_label
    }
    chartw = ChartWindow(DataAnalysisTool, data)
    chartw.show()

def set_accidentchart():
    df = get_data_between_dates()
    # if df != None:
    title = 'Accident per hour (Average)'
    x_label = 'Dates'
    newdf = get_data_between_dates()
    uni = newdf['ACCIDENT_DATE'].value_counts().rename_axis('days').reset_index(name='counts')
    uni = uni.sort_values(by='days')
    dates = uni['days']
    dates = dates.apply(lambda x: x.strftime('%Y-%m-%d'))
    dates = dates.tolist()
    counts = (uni['counts']/24).tolist()
    show_graph(dates, counts, title, x_label)
    

def set_alcohol_impact_chart():
    df = get_data_between_dates()
    # if df != None:
    x_label = 'Trends'
    alc_time = 'yes' if ui.alcoholCheckBox.isChecked() else 'no'
    title = 'Alcohol Impact and Alcohol time ' + alc_time.upper() 
    selectedcolumn = 'LIGHT_CONDITION'
    df['ALCOHOLTIME'] = df['ALCOHOLTIME'].str.lower()
    df = df[df['ALCOHOLTIME'] == alc_time]
    no_alc = df[selectedcolumn].value_counts().rename_axis('trends').reset_index(name='counts')
    counts = no_alc['counts'].tolist()
    trends = no_alc['trends'].tolist()
    show_graph(trends, counts, title, x_label)


def set_speedzone_chart():
    df = get_data_between_dates()
    # if df != None:
    title = "Accidents per speed zone"
    x_label = "Speed Limits"
    speedzone = 'SPEED_ZONE'
    year = 2013
    selectedcolumn = 'ACCIDENT_DATE'
    df['YEAR'] = pd.DatetimeIndex(df[selectedcolumn]).year
    years = df['YEAR'].unique()
    df = df[df['YEAR'] == year]
    no_alc = df[speedzone].value_counts().rename_axis('trends').reset_index(name='counts')
    counts = no_alc['counts'].tolist()
    trends = no_alc['trends'].tolist()
    show_graph(trends, counts, title, x_label)

ui.loadbtn.clicked.connect(load_dataset)
ui.datesearchbtn.clicked.connect(set_date_between_dates)
ui.searchbtn.clicked.connect(set_keyword_date)
ui.accidentchart.clicked.connect(set_accidentchart)
ui.impactbtn.clicked.connect(set_alcohol_impact_chart)
ui.otherinsightbtn.clicked.connect(set_speedzone_chart)


if __name__ == "__main__":
    DataAnalysisTool.show()
    sys.exit(app.exec_())