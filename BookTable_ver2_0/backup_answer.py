from BookTable_ver2_0.utils import *
from BookTable_ver2_0.color_helper import Color_helper
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

main_class = uic.loadUiType("backup_answer.ui")[0]

class Backup_window(QDialog, main_class):
    def __init__(self, mainwindow):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.mainwindow = mainwindow
        self.color_helper = Color_helper(self)
        self.color_helper.get_color_from_setting()
        self.color_helper.set_color()
        self.backup_accept.clicked.connect(self.backup)

    def backup(self):
        Dir = self.mainwindow.db_dir.split('/')
        create_folder('/'.join(Dir[:-2])+'/backup')
        save_DB(self.mainwindow.excel, '/'.join(Dir[:-2])+'/backup'+'/backup_'+Dir[-1])

        self.mainwindow.statusBar.showMessage('File Backup')
        self.close()

