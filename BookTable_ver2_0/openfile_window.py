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

        self.file_list = recent_DB('./DB')
        self.mainwindow.Open_layout.addWidget(Drop_site(self.mainwindow, self))
        self.mainwindow.Open_widget.setStyleSheet('Image:url(./Images/Drop_icon_2.png); background-color:white')

        self.recent_file_buttons = [self.mainwindow.recent_file1, self.mainwindow.recent_file2,
                                    self.mainwindow.recent_file3,
                                    self.mainwindow.recent_file4, self.mainwindow.recent_file5,
                                    self.mainwindow.recent_file6]
        self.recent_file_labels = [self.mainwindow.recent_label1, self.mainwindow.recent_label2,
                                   self.mainwindow.recent_label3,
                                   self.mainwindow.recent_label4, self.mainwindow.recent_label5,
                                   self.mainwindow.recent_label6]

        for button in self.recent_file_buttons:
            button.clicked.connect(self.click_recent_file)

        self.recent_file_show()

    def recent_file_show(self):
        #for button in recent_file_buttons:
        #    button.setFlat(True)

        for i in range(len(self.file_list)):
            menu_icon_size = 150
            self.recent_file_buttons[i].setIcon(QIcon('./Images/database_icon_1.png'))
            self.recent_file_buttons[i].setIconSize(QSize(menu_icon_size, menu_icon_size))
            self.recent_file_buttons[i].setEnabled(True)
            self.recent_file_labels[i].setText(self.file_list[i][1])

    def click_recent_file(self):
        btn_num = int(self.mainwindow.sender().objectName()[-1])
        selected = self.file_list[btn_num-1]
        self.db_dir = selected[0].replace('\\', '/')+'/'+selected[1]

        self.set_file_path()

    def set_file_path(self): # trick.
        if self.db_dir == '':
            return 0
        self.mainwindow.db_dir = self.db_dir
        self.mainwindow.main_stack.setCurrentIndex(0)
        if self.mainwindow.openfile_button.isChecked():
            self.mainwindow.openfile_button.toggle()
            self.mainwindow.sell_button.toggle()

        # Open file
        self.mainwindow.excel = Open_DB(self.mainwindow.db_dir.replace('/', '\\'))

        # update main window
        self.mainwindow.update_main_tables()

        self.mainwindow.statusBar().showMessage('File Opened - ' + self.db_dir.split('/')[-1] + '.')

        if self.mainwindow.timer.isActive():
            self.mainwindow.timer.stop()
            self.mainwindow.timer.start(int(self.mainwindow.Autosave_step) * 60 * 1000)

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

