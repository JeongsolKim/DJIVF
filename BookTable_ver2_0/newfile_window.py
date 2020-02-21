#-*- coding:utf-8 -*-

import os, sys, datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QSize, QDir, Qt, QEvent
from BookTable_ver2_0.utils import *
from BookTable_ver2_0.newfile_answer import Newfile_answer_window

class Newfile_window():
    def __init__(self, mainwindow):
        self.fdir = ''
        self.fname = ''
        self.new_db_name = ''

        self.mainwindow = mainwindow
        self.repaint()
        self.mainwindow.pathRoot = QDir.rootPath()
        self.mainwindow.model = QFileSystemModel()
        self.mainwindow.model.setRootPath(self.mainwindow.pathRoot)
        self.mainwindow.indexRoot = self.mainwindow.model.index(self.mainwindow.model.rootPath())
        self.mainwindow.New_treeView.setModel(self.mainwindow.model)
        self.mainwindow.New_treeView.setRootIndex(self.mainwindow.indexRoot)
        
        self.mainwindow.New_treeView.header().setStretchLastSection(True)
        self.mainwindow.New_treeView.header().resizeSection(0,300)
        
        self.mainwindow.New_treeView.clicked['QModelIndex'].connect(self.get_file_path)
        self.mainwindow.New_submit_button.clicked.connect(self.set_file_path)
        self.mainwindow.New_repaint_button.clicked.connect(self.repaint)

        self.mainwindow.New_layout.addWidget(Drop_site(self.mainwindow, self))
        self.mainwindow.New_widget.setStyleSheet('Image:url(./Images/Drop_icon_excel_1.png); background-color:white')


    def get_file_path(self, index):
        indexItem = self.mainwindow.model.index(index.row(), 0, index.parent())

        self.fname = self.mainwindow.model.fileName(indexItem)
        self.fdir = self.mainwindow.model.filePath(indexItem)

        self.mainwindow.New_dirPlainText.setPlainText(self.fdir)

        if self.fdir.endswith('xlsx'):
            self.mainwindow.New_widget.setStyleSheet(
                'border-image:url(./Images/excel_icon_1.png) 0 0 0 0 stretch stretch')
            self.mainwindow.New_dirPlainText.setPlainText(self.fdir)
            self.mainwindow.New_label.setText(self.fdir.split('/')[-1])
        else:
            self.fdir = ''
            self.mainwindow.New_widget.setStyleSheet(
                'Image:url(./Images/Drop_icon_excel_2.png); background-color:white')
            self.mainwindow.New_dirPlainText.setPlainText('')
            self.mainwindow.New_label.setText('')

    def set_file_path(self):  # trick.
        if self.fdir == '':
            return 0

        self.mainwindow.file_name = self.fname
        self.mainwindow.file_dir = self.fdir

        self.newfile_answer = Newfile_answer_window(self)
        self.newfile_answer.exec_()

        if self.newfile_answer.new_db_name == '':
            return 0
        else:
            self.new_db_name = self.newfile_answer.new_db_name

        is_ok = self.file_save_N_open()

        if not is_ok:
            self.mainwindow.statusBar().showMessage('File is something wrong... - ')
            self.mainwindow.New_widget.setStyleSheet(
                'Image:url(./Images/Drop_icon_excel_2.png); background-color:white')
            self.mainwindow.New_dirPlainText.setPlainText('')
            self.mainwindow.New_label.setText('')
            return 0

        self.mainwindow.statusBar().showMessage('New File is made - ' + self.new_db_name + '.db' + '.')

        if self.mainwindow.timer.isActive():
            self.mainwindow.timer.stop()
            self.mainwindow.timer.start(int(self.mainwindow.Autosave_step) * 60 * 1000)

        self.mainwindow.main_stack.setCurrentIndex(0)
        if self.mainwindow.newfile_button.isChecked():
            self.mainwindow.newfile_button.toggle()


    def file_save_N_open(self):
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_folder = './DB/DB'+time[0:8]
        create_folder(new_folder)

        self.mainwindow.db_dir = new_folder+'/'+ self.new_db_name + '.db'
        is_ok = Initialize_DB(self.mainwindow.file_dir.replace('/', '\\'), new_folder+'/'+ self.new_db_name + '.db')
        if not is_ok:
            return 0

        # Open file
        self.mainwindow.excel = Open_DB(new_folder+'/'+ self.new_db_name + '.db')

        # update main window
        self.mainwindow.update_main_tables()
        return True

    def repaint(self):
        self.fdir = ''
        self.mainwindow.New_widget.setStyleSheet('Image:url(./Images/Drop_icon_excel_1.png); background-color:white')
        self.mainwindow.New_label.setText('')

class Drop_site(QWidget):
    def __init__(self, parent, page):
        super().__init__(parent)

        self.mainwindow = parent
        self.page = page
        self.setAcceptDrops(True)
        self.setStyleSheet('background-color:white')

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        get_dir = e.mimeData().urls()[-1].toLocalFile()
        if get_dir.split('.')[-1] == 'xlsx':
            self.mainwindow.New_widget.setStyleSheet(
                'border-image:url(./Images/excel_icon_1.png) 0 0 0 0 stretch stretch')
            self.page.fdir = get_dir
            self.mainwindow.New_dirPlainText.setPlainText(self.page.fdir)
            self.mainwindow.New_label.setText(get_dir.split('/')[-1])
        else:
            self.mainwindow.New_widget.setStyleSheet('Image:url(./Images/Drop_icon_excel_2.png); background-color:white')
            self.mainwindow.New_dirPlainText.setPlainText('')
            self.mainwindow.New_label.setText('')