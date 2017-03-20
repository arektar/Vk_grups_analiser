import threading
import Social_group_parser
import Analyser
import Posts_parser
import time
import getpass

library = threading.Thread(target=Analyser.library_prepearing)
library.setDaemon(True)
library.start()

login = u'zander5@mail.ru'
password = u'arektar561'

groups_parser = Social_group_parser.VkParser(login, password)
VK_groups_dict = groups_parser.get_new_groups_posts()

parser = Posts_parser.Text_analyser()
groups_base = parser.run(VK_groups_dict)

while library in threading.enumerate():
    time.sleep(1)
    print('.')

vecs_base = {}
for group in groups_base:
    analyser = Analyser.Tree_analyser(groups_base[group])
    vec = analyser.take_vect()
    vecs_base[group] = vec
    print(vec)

if __name__ == "__main__":
    pass
