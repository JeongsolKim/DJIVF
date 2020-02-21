#-*- coding:utf-8 -*-

import sys, shutil, datetime, unicodedata, codecs
import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QSize, QDir, Qt, QTimer
from PyQt5 import uic
from BookTable_ver2_0.newfile_window import Newfile_window
from BookTable_ver2_0.openfile_window import Openfile_window
from BookTable_ver2_0.setting_window import Setting_window
from BookTable_ver2_0.color_helper import Color_helper
from BookTable_ver2_0.status_window import Status_window
from BookTable_ver2_0.figure_helper import Figure_helper
from BookTable_ver2_0.utils import *

# to show custom icon on task bar.
import ctypes
myappid = 'jeongsolKim.jaeminYu.DJIVF.ver2' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

main_class = uic.loadUiType("main_renewal.ui")[0]

class MyWindow(QMainWindow, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        # fix screen size to maximum.
        self.showMaximized()

        # set window icon
        self.setWindowIcon(QtGui.QIcon('images/fileicon.png'))

        # set font
        # self.setFont(QtGui.QFont("맑은 고딕 Semilight", 20, QtGui.QFont.Bold))

        # initialize for file directory.
        self.file_name = ''
        self.file_dir = ''
        self.folder_name = ''
        self.folder_dir = ''
        self.db_dir = ''

        # initialize for display
        self.sell_list = []
        self.nonsell_list = []

        # Search bar icon setting.
        #self.search_icon_size = 25
        #self.search_icon.setIcon(QtGui.QIcon('./Images/active-search.png'))
        #self.search_icon.setIconSize(QSize(self.search_icon_size, self.search_icon_size))

        # Menu bar icon setting.
        self.menu_icon_size = 50
        self.sell_button.setIcon(QtGui.QIcon('./Images/sell_icon_1.png'))
        self.sell_button.setIconSize(QSize(self.menu_icon_size, self.menu_icon_size))
        self.status_button.setIcon(QtGui.QIcon('./Images/status_icon_1.png'))
        self.status_button.setIconSize(QSize(self.menu_icon_size, self.menu_icon_size))
        self.property_button.setIcon(QtGui.QIcon('./Images/setting_icon_1.png'))
        self.property_button.setIconSize(QSize(self.menu_icon_size, self.menu_icon_size))
        self.newfile_button.setIcon(QtGui.QIcon('./Images/newfile_icon_1.png'))
        self.newfile_button.setIconSize(QSize(self.menu_icon_size, self.menu_icon_size))
        self.openfile_button.setIcon(QtGui.QIcon('./Images/openfile_icon_1.png'))
        self.openfile_button.setIconSize(QSize(self.menu_icon_size, self.menu_icon_size))
        self.savefile_button.setIcon(QtGui.QIcon('./Images/savefile_icon_1.png'))
        self.savefile_button.setIconSize(QSize(self.menu_icon_size, self.menu_icon_size))

        # Talbe header size control
        nonsell_header = self.nonsell_table.horizontalHeader()
        nonsell_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        nonsell_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        sell_header = self.timesell_table.horizontalHeader()
        sell_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        sell_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        sell_header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        # initialize for color
        self.color_helper = Color_helper(self)
        self.color_helper.get_color_from_setting()
        self.color_helper.set_color()

        # initialize for status graph
        self.figure_helper = Figure_helper(self.status_graph_layout)

        # initialize for property
        self.IsTutorial = get_setting('./settings.txt', 'TUTORIAL')
        self.IsAutosave = get_setting('./settings.txt', 'AUTOSAVE')
        self.Autosave_step = get_setting('./settings.txt', 'AUTOSAVE_STEP')

        # initialize for (auto) save
        self.start_time = datetime.datetime.now()
        self.last_save = '-'

        if self.IsAutosave == 'True':
            self.timer = QTimer()
            self.timer.start(int(self.Autosave_step) * 60 * 1000)  # unit=milliseconds.
            self.timer.timeout.connect(self.save)

    def change_page(self):
        btn_list = [self.sell_button, self.status_button, self.property_button, self.newfile_button, self.openfile_button]
        btn_name = ['sell_button','status_button','property_button','newfile_button','openfile_button']
        sender_btn = self.sender()
        btn_num = btn_name.index(sender_btn.objectName()) # try and catch ValueError -> return 0.

        if self.main_stack.currentIndex() == btn_num:
            if not sender_btn.isChecked():
                sender_btn.toggle()
                return 0

        self.main_stack.setCurrentIndex(btn_num)
        only_one_menu_button_click(btn_list, sender_btn.objectName())

        if btn_num == 1: self.statusWindow()
        elif btn_num == 2: self.settingWindow()
        elif btn_num == 3: self.newfileWindow()
        elif btn_num == 4: self.openfileWindow()

# -------------------------------------------------------------------------------------#

    def newfileWindow(self):
        self.newfile_helper = Newfile_window(self)

    def openfileWindow(self):
        self.open_helper = Openfile_window(self)

    def settingWindow(self):
        self.setting_helper = Setting_window(self, self.color_helper)

    def statusWindow(self):
        self.status_helper = Status_window(self, self.figure_helper)

# -------------------------------------------------------------------------------------#

    def closeWindow(self):
        self.close()

    def search(self):
        if self.db_dir == '':
            return 0

        if not self.sender().objectName() == 'calendarWidget':
            target = ''.join(self.search_text.text().split())
            update_list([self.nonsell_table, self.timesell_table], self.excel, target)

        elif self.sender().objectName() == 'calendarWidget':
            target = ''.join(self.search_text.text().split())
            date = self.sender().selectedDate().toString("yyyy-MM-dd")
            update_list([self.timesell_table], self.excel, target, date)

    def check_otherbox(self):
        if self.sender().objectName() == 'checkBox1':
            if self.checkBox1.isChecked() and self.checkBox2.isChecked():
                self.checkBox2.toggle()
            elif not self.checkBox1.isChecked() and not self.checkBox2.isChecked():
                self.checkBox2.toggle()

        elif self.sender().objectName() == 'checkBox2':
            if self.checkBox2.isChecked() and self.checkBox1.isChecked():
                self.checkBox1.toggle()
            elif not self.checkBox2.isChecked() and not self.checkBox1.isChecked():
                self.checkBox1.toggle()

    @pyqtSlot()
    def save(self):
        if self.db_dir == '':
            return 0

        if self.sender().objectName() == 'savefile_button':
            self.statusBar().showMessage('Saving...', 1000)
        else:
            self.statusBar().showMessage('AutoSaving...', 1000)

        save_DB(self.excel, self.db_dir)

        self.last_save = datetime.datetime.now()
        if self.sender().objectName() == 'savefile_button':
            self.statusBar().showMessage('Last save: '+self.last_save.strftime("%Y-%m-%d %H:%M:%S")+'.')
        else:
            self.statusBar().showMessage('Last save: ' + self.last_save.strftime("%Y-%m-%d %H:%M:%S") + ' (autosave).')

    def change(self):
        if self.db_dir == '':
            return 0
        soldcol = self.excel.columns.get_loc('판매여부')
        timecol = self.excel.columns.get_loc('판매일시')

        if not self.checkBox1.isChecked() and not self.checkBox2.isChecked():
            return 0

        if self.sender().objectName() == 'sell_button_2':
            if self.checkBox1.isChecked() or self.checkBox2.isChecked():
                if self.nonsell_table.currentRow() > -1:
                    selected_row = self.nonsell_table.selectedItems()[0].text()
                    idx = (i for i, e in enumerate(list(self.excel.values.tolist())) if (e[0] == selected_row and e[soldcol] == 'X'))
                    idx_current = next(idx)

                    self.excel.at[idx_current, '판매여부'] = 'O'
                    self.excel.at[idx_current, '판매일시'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if self.checkBox1.isChecked():
                        self.excel.at[idx_current, '판매방법'] = '현금'
                    elif self.checkBox2.isChecked():
                        self.excel.at[idx_current, '판매방법'] = '계좌이체'

                    # check list
                    self.nonsell_list, self.sell_list = separate_book(self.excel)

                    # repainting
                    self.nonsell_info_box.clear()
                    self.search()

        elif self.sender().objectName() == 'back_button':
            if self.timesell_table.currentRow() > -1:
                selected_row = self.timesell_table.selectedItems()[0].text()
                selected_row2 = self.timesell_table.selectedItems()[2].text()
                idx = (i for i, e in enumerate(list(self.excel.values.tolist())) if e[timecol] == selected_row2)
                idx_current = next(idx)

                self.excel.at[idx_current, '판매여부'] = 'X'
                self.excel.at[idx_current, '판매방법'] = '-'
                self.excel.at[idx_current, '판매일시'] = '-'

                # check list
                self.nonsell_list, self.sell_list = separate_book(self.excel)

                # repainting
                self.sell_info_box.clear()
                self.search()


    def show_info(self):
        # Initialize
        soldcol = self.excel.columns.get_loc('판매여부')
        timecol = self.excel.columns.get_loc('판매일시')

        if self.sender().objectName() == 'nonsell_table':
            # Get selected info
            selected_row = self.sender().selectedItems()[0].text()
            idx = (i for i, e in enumerate(list(self.excel.values.tolist())) if (e[0] == selected_row and e[soldcol] == 'X'))
            selected_book = list(self.excel.values.tolist())[next(idx)]

            # Calculate additional info.
            discount = int(round((selected_book[2] - selected_book[3]) / selected_book[2], 1) * 100)
            if discount == 30:
                selected_book.insert(3, str(discount) + '% - 오늘의 책')
            else:
                selected_book.insert(3, str(discount) + '%')

            # Write.
            self.nonsell_info_box.clear()
            self.nonsell_info_box.appendPlainText('도서명: {}\n'.format(selected_book[0]))
            self.nonsell_info_box.appendPlainText('저자: {}\n'.format(selected_book[1]))
            self.nonsell_info_box.appendPlainText('정가: {}\n'.format(selected_book[2]))
            self.nonsell_info_box.appendPlainText('할인율: {}\n'.format(selected_book[3]))
            self.nonsell_info_box.appendPlainText('판매가: {}\n'.format(selected_book[4]))
            self.nonsell_info_box.repaint()

        elif self.sender().objectName() == 'timesell_table':
            selected_row = self.sender().selectedItems()[0].text()
            selected_row2 = self.sender().selectedItems()[2].text()
            idx = (i for i, e in enumerate(list(self.excel.values.tolist())) if (e[0] == selected_row and e[timecol] == selected_row2))
            selected_book = list(self.excel.values.tolist())[next(idx)]

            # Calculate additional info.
            discount = int(round((selected_book[2] - selected_book[3]) / selected_book[2], 1) * 100)
            if discount == 30:
                selected_book.insert(3, str(discount) + '% - 오늘의 책')
            else:
                selected_book.insert(3, str(discount) + '%')

            # Write.
            self.sell_info_box.clear()
            self.sell_info_box.appendPlainText('도서명: {}\n'.format(selected_book[0]))
            self.sell_info_box.appendPlainText('저자: {}\n'.format(selected_book[1]))
            self.sell_info_box.appendPlainText('정가: {}\n'.format(selected_book[2]))
            self.sell_info_box.appendPlainText('할인율: {}\n'.format(selected_book[3]))
            self.sell_info_box.appendPlainText('판매가: {}\n'.format(selected_book[4]))
            self.sell_info_box.appendPlainText('판매방법: {}\n'.format(selected_book[7]))
            self.sell_info_box.appendPlainText('판매일시: {}\n'.format(selected_book[8]))
            self.sell_info_box.repaint()

    def update_main_tables(self, target=''):
        update_list([self.nonsell_table, self.timesell_table], self.excel, target)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
