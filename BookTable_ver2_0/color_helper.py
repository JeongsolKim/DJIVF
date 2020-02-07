from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QColorDialog, QLabel, QFrame, QMainWindow, QStackedWidget
from PyQt5 import QtGui
from BookTable_ver2_0.utils import *
import math

class Color_helper():
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ColorDialog = QColorDialog()
        self.button_list = ['sell_button_2', 'filebackup_button', 'filereset_button', 'setting_save', 'submit_button',
                            'New_submit_button', 'Open_submit_button', 'colorwidget_button', 'backup_accept']

    def get_color_from_setting(self):
        self.color = get_setting('./settings.txt', 'MAINCOLOR')

    def set_color(self, init=True, target='color_'):
        if init:
            self.change_color(self.color)
        elif not init:
            selected_color = self.ColorDialog.getColor()
            if selected_color.isValid():
                self.color = selected_color.name()
                self.change_color(self.color, target)

    def change_color(self, selected_color, target='color_'):
        fset = self.mainwindow.findChildren(QFrame)
        wset = self.mainwindow.findChildren(QWidget)
        word_color = self.determine_word_color_using_brightness('perceived2', 120)

        for object in fset:
            if target in object.objectName():
                object.setStyleSheet('background-color:' + selected_color +'; color:'+word_color+';')
        for object in wset:
            if object.objectName() in self.button_list and target=='color_':
                object.setStyleSheet('background-color:' + selected_color +'; color:'+word_color+';')

    def determine_word_color_using_brightness(self, method='standard', threshold=125):
        h = self.color.lstrip('#')
        self.RGB = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        if method == 'standard':
            brightness = 0.2126*self.RGB[0] + 0.7152*self.RGB[1] + 0.0722*self.RGB[2]
        elif method == 'perceived1':
            brightness = 0.299*self.RGB[0] + 0.587*self.RGB[1] + 0.114*self.RGB[2]
        elif method == 'perceived2':
            brightness = math.sqrt(0.299*(self.RGB[0]**2) + 0.587*(self.RGB[1]**2) + 0.114*(self.RGB[2]**2))

        if brightness >= threshold:
            return 'rgb(0,0,0)' # black
        elif brightness < threshold:
            return 'rgb(255,255,255)' # white
