from BookTable_ver2_0.utils import *
from BookTable_ver2_0.color_helper import Color_helper
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

main_class = uic.loadUiType("newfile_answer.ui")[0]

class Newfile_answer_window(QDialog, main_class):
    def __init__(self, newfile_window):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.new_db_name = ''

        self.newfile_window = newfile_window
        self.color_helper = Color_helper(self)
        self.color_helper.get_color_from_setting()
        self.color_helper.set_color()
        self.make_file_button.clicked.connect(self.file_make)
        self.newfile_name_line.textEdited.connect(self.file_dir_check)

    def file_make(self):
        filename = self.newfile_name_line.text().strip()
        if filename == '':
            return 0
        self.new_db_name = filename
        self.reject()

    def file_dir_check(self):
        text = self.newfile_name_line.text()
        special_char = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        ret = True
        for c in text:
            if c in special_char:
                ret = False
                break

        if ret:
            self.make_file_button.setEnabled(True)
        else:
            self.make_file_button.setEnabled(False)