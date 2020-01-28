from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QColorDialog, QLabel, QFrame, QMainWindow, QStackedWidget
from PyQt5 import QtGui
from BookTable_ver2_0.utils import *
import math

class Color_helper():
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.ColorDialog = QColorDialog()
        self.button_list = ['sell_button_2', 'filebackup_button', 'filereset_button', 'setting_save', 'submit_button', 'colorwidget_button','test_color']

    def get_color_from_setting(self):
        self.color = get_setting('./settings.txt', 'MAINCOLOR')

    def set_color(self, init=True):
        if init:
            self.change_color(self.color)
        elif not init:
            selected_color = self.ColorDialog.getColor()
            if selected_color.isValid():
                self.color = selected_color.name()
                self.change_color(self.color)

    def change_color(self, selected_color):
        set = self.mainwindow.findChildren(QWidget)
        word_color = self.determine_word_color_using_brightness('perceived2',120)

        for object in set:
            if 'color_' in object.objectName():
                object.setStyleSheet('background-color:' + selected_color)
            elif object.objectName() in self.button_list:
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
