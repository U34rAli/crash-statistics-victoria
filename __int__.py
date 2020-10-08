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

def set_accidentchart():
    data = get_data_between_dates()
    data = {
        "data": data,
        "title": 'Accident per hour (Average)',
        "x_label": 'Dates'
    }
    chartw = ChartWindow(DataAnalysisTool, data)
    chartw.show()


ui.loadbtn.clicked.connect(load_dataset)
ui.datesearchbtn.clicked.connect(set_date_between_dates)
ui.searchbtn.clicked.connect(set_keyword_date)
ui.accidentchart.clicked.connect(set_accidentchart)


if __name__ == "__main__":
    DataAnalysisTool.show()
    sys.exit(app.exec_())