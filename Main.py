import threading
import Social_group_parser
import Vec_worker
import Text_parser
import time
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from File_worker import Reclam_taker
import getpass

library = threading.Thread(target=Vec_worker.library_prepearing)
library.setDaemon(True)

login = u'zander5@mail.ru'
password = u'Arektar561'

while library in threading.enumerate():
    time.sleep(1)
    print('.')


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi('mainwindow.ui')
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_groups)
        self.ui.pushButton_2.clicked.connect(self.update_vecs)
        self.ui.pushButton_3.clicked.connect(self.compare_vecs)
        self.ui.pushButton_2.setEnabled(False)
        self.show()

    def add_groups(self):
        con_wind = ConnectionPropertiesWindow()
        con_wind.show()

    def update_vecs(self):
        work_wind = WorkingWindow()
        work_wind.show()

        my_vec_taker = Vec_worker.Tree_analyser()
        my_vec_taker.start(work_wind)


    def compare_vecs(self):
        compare_wind = ComparePropertiesWindow()
        compare_wind.show()


class ConnectionPropertiesWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi('login_password.ui')
        self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.buttonBox.accepted.connect(self.check_and_continue)

    def check(self):
        user_login = self.ui.lineEdit.text
        user_password = self.ui.lineEdit_2.text
        error_edit = self.ui.lineEdit_3
        if user_login == '':
            error_edit.text = "Введите логин!!!"
        elif user_password == '':
            error_edit.text = "Введите пароль!!!"
        elif (not self.ui.radioButton.checked) and (not self.ui.radioButton_2.checked):
            error_edit.text = "Выберите источник сообществ!!!"
        else:
            param = 4
            if self.ui.radioButton_2.checked:
                param -= 2
            if self.ui.radioButton_2.checked:
                param -= 1

            self.start(user_login, user_password, param)

    def start(self, user_login, user_password, param):
        work_wind = WorkingWindow()
        work_wind.show()
        try:
            groups_parser = Social_group_parser.VkParser(user_login, user_password)
        except:
            self.error_edit.text = "Ошибка авторизации!!!"
            work_wind.close()
            return
        groups_parser.start(param, work_wind)


class WorkingWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi('working.ui')
        self.progress = self.ui.progressBar
        self.info = self.ui.label


class ComparePropertiesWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi('login_password.ui')
        self.ui.buttonBox.accepted.connect(self.check_and_continue)

    def check(self):
        if (self.ui.textBrowser.text == '') or (self.ui.lineEdit.text == ''):
            self.ui.error_lable.text = "Введите текст \nили путь к текстовону \nфайлу"
        elif self.ui.spinBox.value == 0:
            self.ui.error_lable.text = "Выбарите количество \nискомых сообществ"
        elif (self.ui.textBrowser.text != '') or (self.ui.lineEdit.text != ''):
            self.ui.error_lable.text = "Сравнивается только один текст. \nСотрите либо текст, либо путь к файлу."
        else:
            self.start()

    def start(self):
        pass


class ResultWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = uic.loadUi('resultwindow.ui')
        self.ui.pushButton.clicked.connect(self.save)
        self.ui.pushButton_2.clicked.connect(self.close)

    def write_result(self, result):
        self.ui.textBrowser.text = result  # !!! join ...

    def save(self):
        pass

    def close(self):
        pass


if __name__ == "__main__":
    app = QtGui.QGuiApplication(sys.argv)
    mw = MainWindow()
    app.exec_()
    pass
"""
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
