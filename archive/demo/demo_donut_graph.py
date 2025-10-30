# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations
import random

"""PySide6 port of the Donut Chart Breakdown example from Qt v5.x"""

import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice

class Player():
  def __init__(self, name, number, team, message, positions=[], parent=None):
    self.name = name 
    self.number = number 
    self.team = team
    self.positions = positions
    self.at_bat = 0 
    self.hit = 0 
    self.bb = 0
    self.so = 0
    self.hr = 0
    self.rbi = 0
    self.runs = 0
    self.singles = 0
    self.doubles = 0
    self.triples = 0
    self.sac_fly = 0
    self.BABIP = 0
    self.SLG = 0
    self.AVG = 0
    self.ISO = 0
    self.max = 0
    self.image = None

    #message box
    self.message = message
    #print('player initialized - msg inst', self.message)

    # message box self 
    self.parent = parent

  def __str__(self):
    ret = f'Name: {self.name}\nNumber: {self.number}\nPrimary Position: {self.positions[0]}\n  Secondary Positions: {self.positions[1:]}\n'
    ret += f'At Bats: {self.at_bat}\nHits: {self.hit}\nWalks: {self.bb}\nSO: {self.so}\nHR: {self.hr}\n'
    ret += f'Runs: {self.runs}\nRBI: {self.rbi}\nBABIP: {self.BABIP}\nSLG: {self.SLG}\nAVG: {self.AVG}\nISO: {self.ISO}' 
    return ret
  
  def _get_attrs(self):
      directory = dir(self)
      ret = []
      for el in directory:
        temp = getattr(self, el)
        if isinstance(temp, (int)):
            ##print(temp, el)
            ret.append((el, temp))
      return ret

  def check_graph_min(self):
    stats = ['at_bat', 'hit', 'bb', 'so'] 
    for stat in stats:
      val = getattr(self, stat)
      if val == 0:
        print('Sample chart, must update at bats, hits, walks, SOs !')
        return False 
    return True
  
  def set_min(self):
      #self.message.show_message('Sample chart. Player has no updated stats!')
      self.at_bat = 100 
      self.bb = 10 
      self.hit = 33 
      self.sac_fly = 10 
      self.hr = 25 
      self.rbi = 35 
      self.singles = 20 
      self.doubles = 10 
      self.triples = 3
      

  def graph_view_format_player(self):
        '''data_test_player = [
          {
            'Stat': 'On Base',
            'Amount': [{"Hit": 177}, {"BB": 111},{"HBP": 6}, {"Error": 3}],
          },
          {
            'Stat': 'Outs',
            'Amount': [{"SO": 175}, {"Sac Fly": 5}, {"GIDP": 14}],
          }
        ]'''
        check = self.check_graph_min()
        if not check:
           self.set_min()
        ret = [
            {
            'Stat_1': None, 
            'Amount_1': [] 
            },
            {
            'Stat_2': None, 
            'Amount_2': [] 
            }
        ]
        on_base = ['bb', 'doubles', 'hit', 'hr', 'singles', 'triples']
        outs = ['so', 'sac_fly']
        attrs = self._get_attrs()
        #print(attrs)
        for el in attrs:
            #print(el)
            stat = el[0]
            val = el[1]
            #print(stat, val)
            stat_1 = ret[0]['Stat_1']
            stat_2 = ret[1]['Stat_2']
            if stat in on_base:
                #print(stat)
                if not stat_1:
                    ret[0]['Stat_1'] = 'On Base' 
                    temp = {stat:val}
                    amt_lst_1 = ret[0]['Amount_1']
                    amt_lst_1.append(temp) 
                else:
                    temp = {stat:val}
                    amt_lst_1 = ret[0]['Amount_1']
                    amt_lst_1.append(temp) 
            elif stat in outs:
                #print(stat)
                if not stat_2:
                    ret[1]['Stat_2'] = 'Outs'
                    temp = {stat:val}
                    amt_lst_1 = ret[1]['Amount_2']
                    amt_lst_1.append(temp) 
                else:
                    temp = {stat:val}
                    #print(temp)
                    amt_lst_2 = ret[1]['Amount_2']
                    amt_lst_2.append(temp)
        return ret
    
    

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

#series_dic = {}

class MainSlice(QPieSlice):
    def __init__(self, breakdown_series, parent=None):
        super().__init__(parent)

        self.breakdown_series = breakdown_series
        self.name = None

        self.percentageChanged.connect(self.update_label)

    def get_breakdown_series(self):
        return self.breakdown_series

    def set_name(self, name):
        self.name = name

    def name(self):
        return self.name

    @Slot()
    def update_label(self):
        p = self.percentage() * 100
        self.setLabel(f"{self.name} {p:.2f}%")

class DonutBreakdownChart(QChart):
    def __init__(self, data, colors=[], parent=None):
        super().__init__(QChart.ChartTypeCartesian,
                         parent, Qt.WindowFlags())
        self.main_series = QPieSeries()
        self.main_series.setPieSize(0.7)
        self.addSeries(self.main_series)
        self.raw_data = data
        self.colors = colors
        self.color = Qt.red
        self.series_dict = {}

    def add_breakdown_series(self, breakdown_series, color):
        font = QFont("Arial", 12)

        # add breakdown series as a slice to center pie
        main_slice = MainSlice(breakdown_series)
        main_slice.set_name(breakdown_series.name())
        main_slice.setValue(breakdown_series.sum())
        self.main_series.append(main_slice)

        # customize the slice
        main_slice.setBrush(color)
        main_slice.setLabelVisible()
        main_slice.setLabelColor(Qt.white)
        main_slice.setLabelPosition(QPieSlice.LabelInsideHorizontal)
        main_slice.setLabelFont(font)

        # position and customize the breakdown series
        breakdown_series.setPieSize(0.8)
        breakdown_series.setHoleSize(0.7)
        breakdown_series.setLabelsVisible()

        for pie_slice in breakdown_series.slices():
            color = QColor(color).lighter(115)
            pie_slice.setBrush(color)
            pie_slice.setLabelFont(font)

        # add the series to the chart
        self.addSeries(breakdown_series)

        # recalculate breakdown donut segments
        self.recalculate_angles()

        # update customize legend markers
        self.update_legend_markers()

    def recalculate_angles(self):
        angle = 0
        slices = self.main_series.slices()
        for pie_slice in slices:
            breakdown_series = pie_slice.get_breakdown_series()
            breakdown_series.setPieStartAngle(angle)
            angle += pie_slice.percentage() * 360.0  # full pie is 360.0
            breakdown_series.setPieEndAngle(angle)

    def update_legend_markers(self):
        # go through all markers
        for series in self.series():
            markers = self.legend().markers(series)
            for marker in markers:
                if series == self.main_series:
                    # hide markers from main series
                    marker.setVisible(False)
                else:
                    # modify markers from breakdown series
                    label = marker.slice().label()
                    p = marker.slice().percentage() * 100
                    marker.setLabel(f"{label} {p:.2f}%")
                    marker.setFont(QFont("Arial", 8))
    
    def pop_dict(self):
      for indx, el in enumerate(self.raw_data):
        #print(indx, el)
        series = QPieSeries()
        #print(el)

        resource = el['Resource']
        series.setName(resource)

        self.series_dict[resource] = []

        amount = el['Amount']

        for el in amount:
            #print(el)
            type, num = list(el.keys()) + list(el.values()) 
            #print(type, num)
            series.append(type, num)
        self.series_dict[resource].append(series)
            #print(series_dic)
    
    # experimental - graph view 
    def pop_dict_exp(self, r_key, a_key):
      reset_r = r_key 
      reset_a = a_key

      for indx, el in enumerate(self.raw_data):
        #print(indx, el)
        series = QPieSeries()

        r_key = reset_r
        a_key = reset_a

        r_key = r_key + f'_{str(indx+1)}'
        stat = el[r_key]
        
        series.setName(stat)

        self.series_dict[stat] = []

        a_key = a_key + f'_{str(indx+1)}'
        amount = el[a_key]

        for el in amount:
            #print(el)
            type, num = list(el.keys()) + list(el.values()) 
            #print(type, num)
            series.append(type, num)
        self.series_dict[stat].append(series)
            #print(series_dic)
    
    def add_breakdowns(self):
      for el in self.series_dict:
      #print(el, series_dic[el])
        series_lst = self.series_dict[el]
        for series in series_lst:
          color = self.get_rand_color(self.colors, self.series_dict)
          self.add_breakdown_series(series, color)
    
    def get_rand_color(self, colors, dict):
      if len(colors) == 0:
         return self.color 
      
      for el in dict:
        #print(el)
        rand = random.randint(0, len(colors)-1)

        check = colors[rand]

        if check in colors:
          indx = colors.index(check)
          colors.pop(indx)
          return check
        
        rand = random.randint(0, len(colors)-1)
    
    
        
          
        
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Graph is based on data of:
    #    'Total consumption of energy increased by 10 per cent in 2010'
    # Statistics Finland, 13 December 2011
    # http://www.stat.fi/til/ekul/2010/ekul_2010_2011-12-13_tie_001_en.html
    
    colors = [Qt.red, Qt.darkRed, Qt.green, Qt.darkGreen, Qt.blue, Qt.darkBlue, Qt.magenta, Qt.darkMagenta, Qt.cyan, Qt.darkCyan, Qt.yellow, Qt.darkYellow, Qt.gray, Qt.darkGray, Qt.lightGray, Qt.transparent]

    player = Player('Nick Broussard', 18, 'Beef Sliders', 'hello', ['second base', 'pitcher', 'left field'])
    player.at_bat = 40
    player.so = 5
    player.bb = 5 
    player.hit = 5 
    player.sac_fly = 5 
    player.hr = 5 
    player.rbi = 5 
    player.singles = 5 
    player.doubles = 5 
    player.triples = 5
    
    data_test_player_exp = player.graph_view_format_player()

    donut_breakdown = DonutBreakdownChart(data_test_player_exp, colors)
    donut_breakdown.setAnimationOptions(QChart.AllAnimations)
    donut_breakdown.setTitle("Total consumption of energy in Finland 2010")
    donut_breakdown.legend().setAlignment(Qt.AlignRight)

    donut_breakdown.pop_dict_exp('Stat', 'Amount')

    #series_dict = donut_breakdown.series_dict

    donut_breakdown.add_breakdowns()

    window = QMainWindow()
    chart_view = QChartView(donut_breakdown)
    chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
    window.setCentralWidget(chart_view)
    available_geometry = window.screen().availableGeometry()
    size = available_geometry.height() * 0.75
    window.resize(size, size * 0.8)
    window.show()

    sys.exit(app.exec())
