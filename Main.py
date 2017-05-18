import threading
import Social_group_parser
import Vec_worker
import Text_parser
import File_worker
import Data_base_worker
import time
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QScrollBar
from File_worker import Reclam_taker
import getpass
import os

login = u'zander5@mail.ru'
password = u'Arektar561'
dict_path = __file__[:__file__.rfind('\\') + 1] + r'ru_dicts\ruscorpora_mean_hs.model.bin'
app = QApplication(sys.argv)
my_path = __file__[:__file__.rfind('\\') + 1]


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        ui_path = my_path + 'mainwindow.ui'
        self.ui = uic.loadUi(ui_path, self)
        # self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_groups)
        self.ui.pushButton_2.clicked.connect(self.update_vecs)
        self.ui.pushButton_3.clicked.connect(self.compare_vecs)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.result = {}
        # self.show()

    def add_groups(self):
        self.con_wind = ConnectionPropertiesWindow()
        # con_wind.setWindowModality(Qt.WindowModal)
        self.con_wind.show()

    def update_vecs(self):
        self.work_wind = WorkingWindow()

        my_text_worker = Text_parser.Text_analyser()
        my_text_worker.start(self.work_wind)

    def compare_vecs(self):
        self.my_compare_property_wind = ComparePropertiesWindow()
        self.my_compare_property_wind.show()


class ConnectionPropertiesWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi(my_path + 'login_password.ui', self)
        # self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.buttonBox.accepted.connect(self.check)
        self.error_edit = self.ui.label_3
        self.work_wind = WorkingWindow()
        self.show()

    def check(self):
        user_login = self.ui.lineEdit.text()
        user_password = self.ui.lineEdit_2.text()
        if user_login == '':
            self.error_edit.text = "Введите логин!!!"
        elif user_password == '':
            self.error_edit.text = "Введите пароль!!!"
        elif (not self.ui.radioButton.isDown) and (not self.ui.radioButton_2.isDown):
            self.error_edit.text = "Выберите источник сообществ!!!"
        else:
            param = 4
            if self.ui.radioButton_2.isDown:
                param -= 2
            if self.ui.radioButton_2.isDown:
                param -= 1
            self.start(user_login, user_password, param)

    def start(self, user_login, user_password, param):
        self.work_wind.show()
        try:
            groups_parser = Social_group_parser.VkParser(user_login, user_password)
        except:
            self.error_edit.text = "Ошибка авторизации!!!"
            self.work_wind.close()
            return
        groups_parser.start(param, self.work_wind)


class WorkingWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi(my_path + 'working.ui', self)
        self.progress = self.ui.progressBar
        self.info = self.ui.label
        self.result = ''

    def start_process(self, Worker, worker_args):
        self.thread = QThread(self)
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.process)
        self.worker.end.connect(self.get_result)
        self.worker.end.connect(self.thread.quit)
        self.worker.end.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.message.connect(self.update_progress)
        self.thread.start()

    def update_progress(self, mess):
        self.progress.setValue(mess[1])
        self.info.setText(mess[0])

    def get_result(self, data):
        self.close()
        result_groups, result = data
        self.my_result_window = ResultWindow()
        self.my_result_window.write_result(result_groups, result)
        self.my_result_window.show()


class ComparePropertiesWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi(my_path + 'start_compare.ui', self)
        self.ui.buttonBox.accepted.connect(self.check)

    def check(self):
        path = self.ui.lineEdit.text()
        text = self.ui.textBrowser.toPlainText()
        if (text == '') and (path == ''):
            self.ui.error_lable.text = "Введите текст \nили путь к текстовону \nфайлу"
        elif self.ui.spinBox.value == 0:
            self.ui.error_lable.text = "Выбарите количество \nискомых сообществ"
        elif (text != '') and (path != ''):
            self.ui.error_lable.text = "Сравнивается только один текст. \nСотрите либо текст, либо путь к файлу."
        else:
            self.start(path, text)

    def start(self, path, text):
        if not text:
            my_file_worker = File_worker.Reclam_taker(path)
            text = my_file_worker.get_text()

        global user_text, user_num
        user_text = text
        user_num = self.ui.spinBox.value()
        global result_groups, result
        result_groups = ''
        result = ''
        self.work_wind = WorkingWindow()
        self.work_wind.show()
        self.work_wind.start_process(Worker, text)


class ResultWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi(my_path + 'resultwindow.ui', self)
        self.ui.pushButton.clicked.connect(self.save)
        self.show()

    def write_result(self, result_groups, result):
        text = '<html>'
        for each in result:
            group = each[0]
            text += "<b>Сообщество: </b>%s<br /> " % result_groups[group].name
            text += "<b>Близость: </b>%f<br />" % each[1]
            text += "<b>Пользователей: </b>%i<br />" % result_groups[group].members_count
            #text += "<b>Ссылка: </b> <a href={0}>{0}</a><br />".format(result_groups[group].link)
            text += "<b>Ссылка: </b>%s<br />" % result_groups[group].link
            if result_groups[group].description != '--':
                description = result_groups[group].description
                description = description.replace('\n', "<br />")
                text += "<b>Описание: </b>%s<br />" % description
            if result_groups[group].age_limits != 0:
                text += "<b>Возрастное ограничение: </b>%i+<br />" % result_groups[group].age_limits
            if result_groups[group].country != '--':
                text += "<b>Страна: </b>%s<br />" % result_groups[group].country
            if result_groups[group].city != '--':
                text += "<b>Город: </b>%s<br />" % result_groups[group].city
            if result_groups[group].group_type != '--':
                text += "<b>Тип: </b>%s<br />" % result_groups[group].group_type
            if result_groups[group].site != '--':
                #text += "<b>Личный сайт: </b><a href={0}>{0}</a><br />".format(result_groups[group].site)
                text += "<b>Личный сайт: </b>%s<br />" % result_groups[group].site
            text += '<br />'
        text += '</html>'
        self.text = text
        self.ui.textBrowser.append(text)
        scroll = self.ui.textBrowser.verticalScrollBar()
        i = QScrollBar.SliderToMinimum
        scroll.triggerAction(QScrollBar.SliderToMinimum)

    def save(self):
        File_worker.write_result(self.text)


class Worker(QObject):
    end = pyqtSignal(tuple)
    message = pyqtSignal(tuple)

    @pyqtSlot()
    def process(self):
        print('START')
        mess = ('Подготовка текста', 0)
        self.message.emit(mess)
        my_text_worker = Text_parser.Text_analyser()
        prepared_text = my_text_worker.prepareText(user_text)
        self.num = user_num

        mess = ('Векторизация пользовательского текста', 20)
        self.message.emit(mess)
        my_vec_worker = Vec_worker.Tree_analyser()
        text_vec = my_vec_worker.take_words_vec(prepared_text)

        mess = ('Чтение векторов сообществ из базы', 30)
        self.message.emit(mess)
        my_database_worker = Data_base_worker.DB_worker()
        groups_vecs = my_database_worker.get_vecs()

        mess = ('Поиск ближайших векторов сообществ', 60)
        self.message.emit(mess)
        result = Vec_worker.find_nearest(self.num, groups_vecs, text_vec)

        mess = ('Получение информации о ближайших сообществах', 85)
        self.message.emit(mess)
        result_groups = [i[0] for i in result]
        result_groups = my_database_worker.get_groups_data(result_groups)

        mess = ('Готово', 100)
        self.message.emit(mess)
        print('FINISHED')
        data = (result_groups, result)
        self.end.emit(data)


if __name__ == "__main__":
    mw = MainWindow()
    library = threading.Thread(target=Vec_worker.library_prepearing,
                               args=(mw.ui.pushButton_2, mw.ui.pushButton_3, dict_path))
    library.setDaemon(True)

    library.start()

    mw.show()
    sys.exit(app.exec_())

    """
    while library in threading.enumerate():
        time.sleep(1)
        print('.')


if __name__ == "__main__":
    actions_dict = {1: [1, 2, 3, 9], 2: [], 3: [], 9: []}
    print("Добро пожаловать в рекламный анализатор соц. сетей")
    library.start()
    while True:
        action = 0
        while action not in actions_dict:
            print("Меню:")
            print("\t1. Загрузка новых сообществ в базу")
            print("\t2. Определение тематик сообществ")
            print("\t3. Определение сообществ, подходящих тематике текста")
            print("\t9. Закрыть программу")
            action = int(input("Выберите пункт меню: "))
            if action not in actions_dict:
                print("Такого пункта в меню нет")
        if action == 1:
            # login=getpass.getpass("Введите логин аккаунта vk.com")
            # password=getpass.getpass("Введите пароль аккаунта vk.com")
            groups_parser = Social_group_parser.VkParser(login, password)
            action = 0
            while action not in actions_dict[1]:
                print("Выберите ограничения:")
                print("\t1. Получить тематические сообщества и сообщества данного пользователя")
                print("\t2. Получить только тематические сообщества")
                print("\t3. Получить только сообщества данного пользователя")
                print("\t4. Назад")
                action = int(input("Выберите пункт меню: "))
                if action not in actions_dict[1]:
                    print("Такого пункта в меню нет")
            if action == 1:
                VK_groups_dict = groups_parser.get_new_groups_posts(1)
                # print(VK_groups_dict)
                pass

            elif action == 2:
                VK_groups_dict = groups_parser.get_new_groups_posts(2)
                # print(VK_groups_dict)
                pass

            elif action == 3:
                VK_groups_dict = groups_parser.get_new_groups_posts(3)
                # print(VK_groups_dict)
                pass

            elif action == 9:
                break
            action = 0
        elif action == 2:
            parser = Text_parser.Text_analyser()
            VK_groups_dict = {VK_groups_dict.keys()[0]: VK_groups_dict[VK_groups_dict.keys()[0]]}
            groups_base = parser.prepare_posts_text(VK_groups_dict)

            vecs_base = {}
            for group in groups_base:
                analyser = Vec_worker.Tree_analyser(groups_base[group])
                vec = analyser.take_vect()
                vecs_base[group] = vec
                print(vec)

        elif action == 3:
            reclam_file = Reclam_taker()
            text = reclam_file.get_text()

        elif action == 9:
            break
        action = 0
"""
