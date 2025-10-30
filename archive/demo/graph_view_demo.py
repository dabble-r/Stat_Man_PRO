from __future__ import annotations
import random

"""PySide6 port of the Donut Chart Breakdown example from Qt v5.x"""


import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Slot)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QDialog, QListView, QSizePolicy,
    QWidget, QTreeWidget, QTreeWidgetItem, QHeaderView, QPushButton, QVBoxLayout, QHBoxLayout)
from stat_mg_py6.demo.demo_donut_graph import MainSlice, DonutBreakdownChart
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from Styles.stylesheets import StyleSheets
from League.player import Player

data_test_player = [
    {
      'Stat': 'On Base',
      'Amount': [{"Hit": 177}, {"BB": 111},{"HBP": 6}, {"Error": 3}],
    },
    {
      'Stat': 'Outs',
      'Amount': [{"SO": 175}, {"Sac Fly": 5}, {"GIDP": 14}],
    }
]



def get_graph(selected, data):
    if selected is None:
        print('player graph')
        player_dict = data

        graph_widget = QDialog()
        graph_widget.resize(750, 750)

        donut_breakdown = DonutBreakdownChart(player_dict)
        donut_breakdown.setAnimationOptions(QChart.AllAnimations)
        donut_breakdown.setTitle("Test League Graph View")
        donut_breakdown.legend().setAlignment(Qt.AlignRight)

        donut_breakdown.pop_dict()

        chart_view = QChartView(donut_breakdown)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        graph_layout = QVBoxLayout()
        graph_layout.addWidget(chart_view)

        graph_widget.setLayout(graph_layout)

        graph_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Graph is based on data of:
    #    'Total consumption of energy increased by 10 per cent in 2010'
    # Statistics Finland, 13 December 2011
    # http://www.stat.fi/til/ekul/2010/ekul_2010_2011-12-13_tie_001_en.html
    
    colors = [Qt.red, Qt.darkRed, Qt.green, Qt.darkGreen, Qt.blue, Qt.darkBlue, Qt.magenta, Qt.darkMagenta, Qt.cyan, Qt.darkCyan, Qt.yellow, Qt.darkYellow, Qt.gray, Qt.darkGray, Qt.lightGray, Qt.transparent]

    '''for indx, el in enumerate(data):
    #print(indx, el)
    series = QPieSeries()
    #print(el)

    resource = el['Resource']
    series.setName(resource)

    series_dic[resource] = []

    amount = el['Amount']

    for el in amount:
        #print(el)
        type, num = list(el.keys()) + list(el.values()) 
        #print(type, num)
        series.append(type, num)
    series_dic[resource].append(series)
        #print(series_dic)'''

    '''
    series1 = QPieSeries()
    series1.setName("Fossil fuels")
    series1.append("Oil", 353295)
    series1.append("Coal", 188500)
    series1.append("Natural gas", 148680)
    series1.append("Peat", 94545)

    series2 = QPieSeries()
    series2.setName("Renewables")
    series2.append("Wood fuels", 319663)
    series2.append("Hydro power", 45875)
    series2.append("Wind power", 1060)

    series3 = QPieSeries()
    series3.setName("Others")
    series3.append("Nuclear energy", 238789)
    series3.append("Import energy", 37802)
    series3.append("Other", 32441)
    '''

    donut_breakdown = DonutBreakdownChart(data_test_player, colors)
    donut_breakdown.setAnimationOptions(QChart.AllAnimations)
    donut_breakdown.setTitle("Total consumption of energy in Finland 2010")
    donut_breakdown.legend().setAlignment(Qt.AlignRight)

    donut_breakdown.pop_dict_exp('Stat', 'Amount')

    series_dict = donut_breakdown.series_dict

    donut_breakdown.add_breakdowns()

    '''
    for el in series_dic:
      #print(el, series_dic[el])
      series_lst = series_dic[el]
      for series in series_lst:
        donut_breakdown.add_breakdown_series(series, Qt.red)'''
    
    #print(series_dic)


    #donut_breakdown.add_breakdown_series(series1, Qt.red)
    #donut_breakdown.add_breakdown_series(series2, Qt.darkGreen)
    #donut_breakdown.add_breakdown_series(series3, Qt.darkBlue)


    window = QMainWindow()
    chart_view = QChartView(donut_breakdown)
    chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
    window.setCentralWidget(chart_view)
    available_geometry = window.screen().availableGeometry()
    size = available_geometry.height() * 0.75
    window.resize(size, size * 0.8)
    window.show()

    sys.exit(app.exec())




