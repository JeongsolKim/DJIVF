from PyQt5.QtWidgets import *
from PyQt5 import uic
from BookTable_ver2_0.utils import *



class Setting_window():
    def __init__(self, mainwindow, color_helper):
        self.init_values = {'AUTOSAVE':True, 'AUTOSAVE_STEP':5, 'TUTORIAL':True, 'MAINCOLOR':'#1d305a'}

        self.mainwindow = mainwindow
        self.color_helper = color_helper
        self.load_setting()
        self.update_checkbox()

        self.mainwindow.Autosave_check.clicked.connect(self.set_spinbox)
        self.mainwindow.Autosave_time.valueChanged.connect(self.set_checkbox)
        self.mainwindow.setting_save.clicked.connect(self.property_change)
        self.mainwindow.setting_reset.clicked.connect(self.reset_setting)
        #self.mainwindow.filebackup_button.clicked.connect(self.back_up)
        self.mainwindow.filereset_button.clicked.connect(self.reset_really)
        self.mainwindow.colorwidget_button.clicked.connect(self.color_setting)

    def load_setting(self):
        self.IsAutosave = get_setting('settings.txt', 'AUTOSAVE') == 'True'
        self.Autosave_step = get_setting('settings.txt', 'AUTOSAVE_STEP')
        self.IsTutorial = get_setting('settings.txt', 'TUTORIAL') == 'True'

    def reset_setting(self):
        set_setting('settings.txt', 'AUTOSAVE', self.init_values.get('AUTOSAVE'))
        set_setting('settings.txt', 'AUTOSAVE_STEP', self.init_values.get('AUTOSAVE_STEP'))
        set_setting('settings.txt', 'TUTORIAL', self.init_values.get('TUTORIAL'))
        set_setting('settings.txt', 'MAINCOLOR', self.init_values.get('MAINCOLOR'))

        self.load_setting()
        self.update_checkbox()
        self.color_helper.get_color_from_setting()
        self.color_helper.set_color()

    def get_autosave(self):
        self.IsAutosave = self.mainwindow.Autosave_check.isChecked()
        self.Autosave_step = self.mainwindow.Autosave_time.value()

    def get_tutorial(self):
        self.IsTutorial = self.mainwindow.Tutorial_check.isChecked()

    def property_change(self):
        self.get_autosave()
        self.get_tutorial()

        set_setting('./settings.txt', 'AUTOSAVE', self.IsAutosave)
        set_setting('./settings.txt', 'AUTOSAVE_STEP', self.Autosave_step)
        set_setting('./settings.txt', 'TUTORIAL', self.IsTutorial)
        set_setting('./settings.txt', 'MAINCOLOR', self.color_helper.color)
        self.update_checkbox()

    def set_spinbox(self):
        if self.mainwindow.Autosave_check.isChecked():
            self.mainwindow.Autosave_time.setValue(5)
        else:
            self.mainwindow.Autosave_time.setValue(0)

    def set_checkbox(self):
        if self.mainwindow.Autosave_time.value() == 0:
            if self.mainwindow.Autosave_check.isChecked():
                self.mainwindow.Autosave_check.toggle()
        else:
            if not self.mainwindow.Autosave_check.isChecked():
                self.mainwindow.Autosave_check.toggle()

    def update_checkbox(self):
        if self.mainwindow.Autosave_check.isChecked() and not self.IsAutosave:
            self.mainwindow.Autosave_check.toggle()
        elif not self.mainwindow.Autosave_check.isChecked() and self.IsAutosave:
            self.mainwindow.Autosave_check.toggle()

        self.mainwindow.Autosave_time.setValue(int(self.Autosave_step))

        if self.IsTutorial and not self.mainwindow.Tutorial_check.isChecked():
            self.mainwindow.Tutorial_check.toggle()
        elif not self.IsTutorial and self.mainwindow.Tutorial_check.isChecked():
            self.mainwindow.Tutorial_check.toggle()

    # -------------------------------------------------------------------------------------- #
    def color_setting(self):
        self.color_helper.set_color(False)

    def back_up(self):
        pass

    def reset_really(self):
        if self.mainwindow.file_name == '':
            return 0

        buttonReply = QMessageBox.question(self, '초기화 확인', "정말로 파일을 초기화 하시겠습니까? 초기화 이후에는 복구가 불가능합니다.",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.reset()
        else:
            pass

    def reset(self):
        folder = self.mainwindow.folder_dir + '/' + self.mainwindow.folder_name
        file = self.mainwindow.file_name.split('_modify')[0] + '.xlsx'
        excel = pd.read_excel(folder + '/' + file)
        self.mainwindow.excel = excel_file_initialize(excel)
        self.mainwindow.excel.to_excel(folder + '/' + file.split('.')[0] + '_modify.xlsx', index=False)

        QMessageBox.information(self,'초기화 완료', '파일 초기화가 완료되었습니다.')

        self.mainwindow.search()


