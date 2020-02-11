import os, sys, copy, sqlite3
import pandas as pd
from datetime import datetime as dt
from pathlib import Path
from PyQt5 import QtWidgets

def get_setting(file, property): # Property = True -> return 'True'
    f = open(file, 'r')
    while True:
        line = f.readline()
        if not line: break
        if property in line:
            break
    f.close()

    if not line:
        return 0
    else:
        return line.split('=')[-1].strip()

def set_setting(file, property, value):
    lines = []
    new_line = property + ' = ' + str(value) + '\n'
    with open(file, 'r+') as f:
        while True:
            line = f.readline()
            if not line:
                break
            if line.split('=')[0].strip() == property:
                lines = lines + [new_line]
            else:
                lines = lines + [line]
        f.seek(0)
        f.writelines(lines)
        f.truncate()

def Initialize_DB(data_dir, save_dir): # dataframe into database
    con = sqlite3.connect(save_dir)

    excel = pd.read_excel(data_dir)
    excel = excel_file_initialize(excel)
    excel_list = excel.values.tolist()

    cur = con.cursor()
    query = 'CREATE TABLE IF NOT EXISTS booktable(' \
            'book_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
            'name TEXT,' \
            'author TEXT,' \
            'initial_price INTEGER,' \
            'sale_price INTEGER,' \
            'count INTEGER,' \
            'IsSale TEXT,' \
            'HowSale TEXT,' \
            'WhenSale TEXT);'

    cur.execute(query)
    cur.executemany("INSERT INTO booktable (name, author, initial_price, sale_price, count, IsSale, HowSale, WhenSale) \
     VALUES(?, ?, ?, ?, ?, ?, ?, ?);", excel_list)
    con.commit()
    con.close()

def save_DB(df, db_dir):
    con = sqlite3.connect(db_dir)
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS booktable')

    query = 'CREATE TABLE IF NOT EXISTS booktable(' \
            'book_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
            'name TEXT,' \
            'author TEXT,' \
            'initial_price INTEGER,' \
            'sale_price INTEGER,' \
            'count INTEGER,' \
            'IsSale TEXT,' \
            'HowSale TEXT,' \
            'WhenSale TEXT);'

    cur.execute(query)
    cur.executemany("INSERT INTO booktable (name, author, initial_price, sale_price, count, IsSale, HowSale, WhenSale) \
         VALUES(?, ?, ?, ?, ?, ?, ?, ?);", df.values.tolist())
    con.commit()
    con.close()

def Open_DB(db_dir):
    con = sqlite3.connect(db_dir)
    cur = con.cursor()
    cur.execute('SELECT name, author, initial_price, sale_price, count, IsSale, HowSale, WhenSale FROM booktable')
    L = list(map(lambda x: list(x), cur.fetchall()))
    con.close()

    df = pd.DataFrame(L, columns=['책이름','저자','정가','판매가','수량','판매여부','판매방법','판매일시'])
    return df

def recent_DB(db_folder, top = 6):
    file_time_list = []

    for (path, dir, files) in os.walk(db_folder):
        for filename in files:
            if 'backup' in filename: continue
            if filename.split('.')[-1] != 'db': continue
            fileMtime = dt.fromtimestamp(os.path.getmtime(path + '\\' + filename)).strftime("%Y-%m-%d %H:%M:%S")
            file_time_list.append([path, filename, fileMtime])

    file_time_list.sort(key = lambda file_time_list: file_time_list[2])
    file_time_list.reverse()

    if len(file_time_list) > top:
        return file_time_list[0:top]
    else:
        return file_time_list

def only_one_menu_button_click(btn_list, one_button):
    for check_btn in btn_list:
        if not check_btn.objectName() == one_button:
            if check_btn.isChecked():
                check_btn.toggle()

def file_search(dir_name): # Find excel file (xxx_modify.xlsx)
    for (path, dir, files) in os.walk(dir_name):
        for filename in files:
            ext = filename.split('_')[-1]
            if 'modify' in ext:
                return dir_name+'/'+filename
    return False

def isNaN(string):
    return string != string

def create_folder(folder_name):
    Path(folder_name).mkdir(parents=True, exist_ok=True)

def excel_file_initialize(excel): # Remove empty rows, Add additional columns (판매여부, 방법, 일시)
    new_list = []
    value_list = list(excel.values.tolist())

    for book in value_list:
        if isNaN(book[0]):
            continue
        elif isNaN(book[1]):
            book[1] = '-'
            book[2] = int(book[2])
            book[3] = int(book[3])
            book[4] = int(book[4])
        else:
            book[2] = int(book[2])
            book[3] = int(book[3])
            book[4] = int(book[4])

        for num in range(book[4]): # book numbering
            book_copy = copy.deepcopy(book)
            book_copy[4] = num+1
            new_list.append(book_copy)

    num_row = len(new_list)

    # find empty line
    empty_index = []
    for book_num in range(num_row):
        if isNaN(new_list[book_num][0]):
            empty_index.append(book_num)

    append_index = [x for x in list(range(num_row)) if x not in empty_index]

    new_excel = pd.DataFrame(new_list, columns=list(excel.columns))
    issell = pd.DataFrame({'판매여부':['X']*(num_row-len(empty_index))}, index=append_index)
    howsell = pd.DataFrame({'판매방법':['-']*(num_row-len(empty_index))}, index=append_index)
    whensell = pd.DataFrame({'판매일시':['-']*(num_row-len(empty_index))}, index=append_index)

    return pd.concat([new_excel, pd.concat([issell, howsell, whensell], axis=1)], axis=1)

def separate_book(file, target='', date=False):
    nonsell_list = []
    sell_list = []
    value_list = list(file.values.tolist())

    namecol = file.columns.get_loc('책이름')
    writercol = file.columns.get_loc('저자')
    soldcol = file.columns.get_loc('판매여부')
    timecol = file.columns.get_loc('판매일시')

    if target == '':
        for book in value_list:
            if not date:
                if book[soldcol] == 'X':
                    nonsell_list.append(book)
                elif book[soldcol] == 'O':
                    sell_list.append(book)
            else:
                if date == book[timecol].split(' ')[0]:
                    if book[soldcol] == 'X':
                        nonsell_list.append(book)
                    elif book[soldcol] == 'O':
                        sell_list.append(book)
    else:
        for book in value_list:
            if target in ''.join(book[namecol].split()) or target in ''.join(book[writercol].split()):
                if not date:
                    if book[soldcol] == 'X':
                        nonsell_list.append(book)
                    elif book[soldcol] == 'O':
                        sell_list.append(book)
                else:
                    if date == book[timecol].split(' ')[0]:
                        if book[soldcol] == 'X':
                            nonsell_list.append(book)
                        elif book[soldcol] == 'O':
                            sell_list.append(book)


    return nonsell_list, sell_list

def resetTable(Obj_list):
    for Obj in Obj_list:
        for i in range(Obj.rowCount()):
            Obj.removeRow(0)

def addRow(Obj, content):
    numRows = Obj.rowCount()
    Obj.insertRow(numRows)
    for i in range(len(content)):
        Obj.setItem(numRows, i, QtWidgets.QTableWidgetItem(content[i]))

def write_table(Obj_list, list1, list2, col1, col2, col3):
    resetTable(Obj_list)

    for Obj in Obj_list:
        if Obj.objectName() == 'nonsell_table':
            if list1:
                # second, write non sell lists
                for nonsell_book in list1:
                    if isNaN(nonsell_book[col2]):
                        addRow(Obj, [nonsell_book[col1], '-'])
                    else:
                        addRow(Obj, [nonsell_book[col1], nonsell_book[col2]])

        elif Obj.objectName() == 'sell_table':
            if list2:
                # third, write sell list
                for sell_book in list2:
                    if isNaN(sell_book[col2]):
                        addRow(Obj, [sell_book[col1], '-'])
                    else:
                        addRow(Obj, [sell_book[col1], sell_book[col2]])

        elif Obj.objectName() == 'timesell_table':
            if list2:
                list2.sort(key=lambda x: x[col3])
                for sell_book in list2:
                    if isNaN(sell_book[col2]):
                        addRow(Obj, [sell_book[col1], '-', sell_book[col3]])
                    else:
                        addRow(Obj, [sell_book[col1], sell_book[col2], sell_book[col3]])

        elif Obj.objectName() == 'status_table':
            sep_list = []
            if list2:
                list2.sort(key=lambda x: x[col1])
                temp_date = list2[0][col1].split(' ')[0]
                temp_list = []
                for sell_book in list2:
                    if sell_book[col1].split(' ')[0] == temp_date:
                        temp_list.append(sell_book)
                    else:
                        sep_list.append(temp_list)
                        temp_list = [sell_book]
                        temp_date = sell_book[col1].split(' ')[0]
                sep_list.append(temp_list)

                for date_list in sep_list:
                    cash_price = 0
                    account_price = 0
                    total_price = 0
                    for i in range(len(date_list)):
                        if date_list[i][col3] == '현금':
                            cash_price += int(date_list[i][col2])
                            total_price += int(date_list[i][col2])
                        elif date_list[i][col3] == '계좌이체':
                            account_price += int(date_list[i][col2])
                            total_price += int(date_list[i][col2])

                    addRow(Obj, [date_list[i][col1].split(' ')[0], str(cash_price)+'원', str(account_price)+'원', str(total_price)+'원'])


def update_list(Obj_list, file, target='', date=False):
    namecol = file.columns.get_loc('책이름')
    writercol = file.columns.get_loc('저자')
    timecol = file.columns.get_loc('판매일시')

    # Initialize
    resetTable(Obj_list)

    # Separate
    if len(Obj_list) == 1 and Obj_list[0].objectName() == 'timesell_table':
        nonsell_list, sell_list = separate_book(file, target, date)
    else:
        nonsell_list, sell_list = separate_book(file, target, date)

    # Write
    write_table(Obj_list, nonsell_list, sell_list, namecol, writercol, timecol)
    return 0
