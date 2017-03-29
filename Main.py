import threading
import Social_group_parser
import Vec_worker
import Text_parser
import time
from File_worker import Reclam_taker
import getpass

library = threading.Thread(target=Vec_worker.library_prepearing)
library.setDaemon(True)

login = u'zander5@mail.ru'
password = u'Arektar561'

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
