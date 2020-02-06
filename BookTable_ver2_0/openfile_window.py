#-*- coding:utf-8 -*-

import os, sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QSize, QDir, Qt
from BookTable_ver2_0.utils import *
import getpass

class Openfile_window():
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.mainwindow.pathRoot = QDir.rootPath()
        self.mainwindow.model = QFileSystemModel()
        self.mainwindow.model.setRootPath(self.mainwindow.pathRoot)
        self.mainwindow.indexRoot = self.mainwindow.model.index(self.mainwindow.model.rootPath())
        self.mainwindow.Open_treeView.setModel(self.mainwindow.model)
        self.mainwindow.Open_treeView.setRootIndex(self.mainwindow.indexRoot)

        self.mainwindow.Open_treeView.header().setStretchLastSection(True)
        self.mainwindow.Open_treeView.header().resizeSection(0, 300)

        self.mainwindow.Open_treeView.clicked['QModelIndex'].connect(self.get_file_path)
        self.mainwindow.Open_submit_button.clicked.connect(self.set_file_path)

        self.mainwindow.Open_layout.addWidget(Drop_site(self.mainwindow))

    def get_file_path(self, index):
        indexItem = self.mainwindow.model.index(index.row(), 0, index.parent())

        self.mainwindow.db_dir = self.mainwindow.model.filePath(indexItem)
        self.mainwindow.Open_dirPlainText.setPlainText(self.mainwindow.db_dir)

    def set_file_path(self): # trick.
        if self.mainwindow.db_dir == '':
            return 0
        self.mainwindow.main_stack.setCurrentIndex(0)

        # Open file
        self.mainwindow.excel = Open_DB(self.mainwindow.db_dir.replace('/', '\\'))

        # update main window
        self.mainwindow.update_main_tables()

class Drop_site(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.mainwindow = parent
        self.setAcceptDrops(True)
        self.setStyleSheet('background-color:white')

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        #img = e.mimeData().imageData()
        self.mainwindow.db_dir = e.mimeData().urls()[-1].toLocalFile()
        self.mainwindow.Open_dirPlainText.setPlainText(self.mainwindow.db_dir)

