from PyQt5.QtCore import pyqtSlot, QSize, QDir, Qt, QTimer
from BookTable_ver2_0.utils import *
import numpy as np

class Status_window():
    def __init__(self, mainwindow, figure_helper):
        self.mainwindow = mainwindow
        self.figure_helper = figure_helper

        if not self.mainwindow.file_name == '':
            self.timer = QTimer()
            self.timer.start(1000)  # unit=milliseconds.
            self.timer.timeout.connect(self.update_status)

    def update_status(self):
        self.nslist, self.slist = separate_book(self.mainwindow.excel)

        self.update_percentage_bar()
        self.update_table()
        self.update_graph()

    def update_table(self):
        timecol = self.mainwindow.excel.columns.get_loc('판매일시')
        pricecol = self.mainwindow.excel.columns.get_loc('판매가')
        howcol = self.mainwindow.excel.columns.get_loc('판매방법')

        write_table([self.mainwindow.status_table], self.nslist, self.slist, timecol, pricecol, howcol)

    def update_percentage_bar(self):
        self.mainwindow.soldpercentage.setValue((len(self.slist)/(len(self.nslist)+len(self.slist)))*100)

    def update_graph(self):
        timecol = self.mainwindow.excel.columns.get_loc('판매일시')
        howcol = self.mainwindow.excel.columns.get_loc('판매방법')

        date_list = []
        sep_list = []
        if self.slist:
            self.slist.sort(key=lambda x: x[timecol])
            temp_date = self.slist[0][timecol].split(' ')[0]
            date_list.append(temp_date.split('-')[1]+'-'+temp_date.split('-')[2])
            temp_list = []
            for sell_book in self.slist:
                if sell_book[timecol].split(' ')[0] == temp_date:
                    temp_list.append(sell_book)
                else:
                    sep_list.append(temp_list)
                    temp_list = [sell_book]
                    temp_date = sell_book[timecol].split(' ')[0]
                    date_list.append(temp_date.split('-')[1]+'-'+temp_date.split('-')[2])
            sep_list.append(temp_list)

            cash_list = []
            account_list = []

            for one_Date in sep_list:
                cash_num = 0
                account_num = 0
                for i in range(len(one_Date)):
                    if one_Date[i][howcol] == '현금':
                        cash_num += 1
                    elif one_Date[i][howcol] == '계좌이체':
                        account_num += 1
                cash_list.append(cash_num)
                account_list.append(account_num)

            self.figure_helper.draw_group_bar_graph(np.arange(len(date_list)), [cash_list, account_list], date_list)

    def update_total(self):
        pricecol = self.mainwindow.excel.columns.get_loc('판매가')
        price = 0
        for book in self.slist:
            price += int(book[pricecol])
        self.mainwindow.total.setText(str(price))