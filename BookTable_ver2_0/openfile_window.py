#-*- coding:utf-8 -*-

import os, sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import pyqtSlot, QSize, QDir, Qt
from BookTable_ver2_0.utils import *
import getpass

class Openfile_window():
    def __init__(self, mainwindow):
        self.db_dir = ''

        self.mainwindow = mainwindow
        self.repaint()
        self.mainwindow.Open_submit_button.clicked.connect(self.set_file_path)
        self.mainwindow.Open_repaint_button.clicked.connect(self.repaint)

        self.mainwindow.Open_layout.addWidget(Drop_site(self.mainwindow, self))
        self.mainwindow.Open_widget.setStyleSheet('Image:url(./Images/Drop_icon_2.png); background-color:white')

    def get_file_path(self, index):
        indexItem = self.mainwindow.model.index(index.row(), 0, index.parent())

        self.db_dir = self.mainwindow.model.filePath(indexItem)
        self.mainwindow.Open_dirPlainText.setPlainText(self.db_dir)

    def set_file_path(self): # trick.
        if self.db_dir == '':
            return 0
        self.mainwindow.db_dir = self.db_dir
        self.mainwindow.main_stack.setCurrentIndex(0)

        # Open file
        self.mainwindow.excel = Open_DB(self.mainwindow.db_dir.replace('/', '\\'))

        # update main window
        self.mainwindow.update_main_tables()

    def repaint(self):
        self.db_dir = ''
        self.mainwindow.Open_widget.setStyleSheet('Image:url(./Images/Drop_icon_2.png); background-color:white')
        self.mainwindow.Open_label.setText('')

class Drop_site(QWidget):
    def __init__(self, parent, page):
        super().__init__(parent)

        self.mainwindow = parent
        self.page = page
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        get_dir = e.mimeData().urls()[-1].toLocalFile()
        if get_dir.split('.')[-1] == 'db':
            self.mainwindow.Open_widget.setStyleSheet('border-image:url(./Images/database_icon_1.png) 0 0 0 0 stretch stretch')
            self.page.db_dir = get_dir
            self.mainwindow.Open_dirPlainText.setPlainText(self.page.db_dir)
            self.mainwindow.Open_label.setText(get_dir.split('/')[-1])
        else:
            self.mainwindow.Open_widget.setStyleSheet('Image:url(./Images/Drop_icon_3.png); background-color:white')
            self.mainwindow.Open_dirPlainText.setPlainText('')
            self.mainwindow.Open_label.setText('')

