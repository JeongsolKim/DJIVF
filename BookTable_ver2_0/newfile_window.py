#-*- coding:utf-8 -*-

import os, sys, datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QSize, QDir, Qt, QEvent
from BookTable_ver2_0.utils import *

class Newfile_window():
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.mainwindow.pathRoot = QDir.rootPath()
        self.mainwindow.model = QFileSystemModel()
        self.mainwindow.model.setRootPath(self.mainwindow.pathRoot)
        self.mainwindow.indexRoot = self.mainwindow.model.index(self.mainwindow.model.rootPath())
        self.mainwindow.treeView.setModel(self.mainwindow.model)
        self.mainwindow.treeView.setRootIndex(self.mainwindow.indexRoot)

        self.mainwindow.treeView.clicked['QModelIndex'].connect(self.get_file_path)
        self.mainwindow.submit_button.clicked.connect(self.set_file_path)

        #self.mainwindow.newfile_dragdrop.setAcceptDrops(True)
        #self.mainwindow.newfile_dragdrop.textChanged.connect(self.drag_N_drop)

    def get_file_path(self, index):
        indexItem = self.mainwindow.model.index(index.row(), 0, index.parent())

        self.mainwindow.file_name = self.mainwindow.model.fileName(indexItem)
        self.mainwindow.file_dir = self.mainwindow.model.filePath(indexItem)

        self.mainwindow.dirPlainText.setPlainText(self.mainwindow.file_dir)

    def set_file_path(self):  # trick.
        if self.mainwindow.file_name == '':
            return 0
        self.mainwindow.main_stack.setCurrentIndex(0)
        if self.mainwindow.newfile_button.isChecked():
            self.mainwindow.newfile_button.toggle()

        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_folder = './DB/DB'+time[0:8]
        create_folder(new_folder)

        self.mainwindow.db_dir = new_folder+'/BookTableDB'+time+'.db'
        Initialize_DB(self.mainwindow.file_dir.replace('/', '\\'), new_folder+'/BookTableDB'+time+'.db')

        # Open file
        self.mainwindow.excel = Open_DB(new_folder+'/BookTableDB'+time+'.db')

        # update main window
        self.mainwindow.update_main_tables()

    def drag_N_drop(self):
        pass