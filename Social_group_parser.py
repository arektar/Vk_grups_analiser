# -*- coding: cp1251*-
import vk
import time

app_id = "5286311"


class VkParser():
    def __init__(self, login, password, blacklist_path='blacklist'):
        self.session = vk.AuthSession(
            app_id=app_id,
            user_login=login,
            user_password=password,
            scope='groups'
        )
        self.vk_api = vk.API(self.session, v='5.62')
        self.blacklist_path = blacklist_path

    def get_catalog(self):
        categories = self.vk_api.groups.getCatalogInfo(subcategories=1)['categories']
        subcategories = []
        for index, category in enumerate(categories):
            if 'subcategories' in category.keys():
                subcategories = categories.pop(index)['subcategories']
                break
        return categories, subcategories

    def get_groups_id_in_category(self, category_id, if_sub=0):
        ids = []
        if if_sub:
            groups = self.vk_api.groups.getCatalog(subcategory_id=category_id)['items']
        else:
            groups = self.vk_api.groups.getCatalog(category_id=category_id)['items']
        for group in groups:
            ids.append(group['id'])
        return ids

    def get_from_categories(self):
        categories, subcategories = self.get_catalog()
        groups_ids = list()
        for category in categories:
            groups_ids.extend(self.get_groups_id_in_category(category['id']))
            time.sleep(0.5)
        for category in subcategories:
            groups_ids.extend(self.get_groups_id_in_category(category['id'], if_sub=1))
            time.sleep(0.5)
        return groups_ids

    def get_user_groups(self):
        ids = self.vk_api.groups.get()['items']
        return ids

    def prepare_blacklist(self):
        with open(self.blacklist_path) as blacklist_file:
            blacklist = blacklist_file.read().split('\n')
        return blacklist

    def check_in_blacklist(self, groups_set):
        blacklist = set(self.prepare_blacklist())
        new_groups_list = groups_set.difference(blacklist)
        return new_groups_list

    def get_new_groups(self):
        groups_ids_set = set()
        groups_ids_set.update(self.get_from_categories())
        groups_ids_set.update(self.get_user_groups())
        print(groups_ids_set)
        new_groups_ids_set = self.check_in_blacklist(groups_ids_set)
        print(new_groups_ids_set)
        return new_groups_ids_set

    def get_new_groups_posts(self):
        new_groups_ids_set = self.get_new_groups()
        groups_posts_base = {}
        try:
            groups_data = self.vk_api.groups.getById(group_ids=list(new_groups_ids_set))
            for group_data in groups_data:
                try:
                    name = group_data[u'name']
                    posts = self.vk_api.wall.get(owner_id=-group_data['id'], count=100)[u'items']
                except vk.exceptions.VkAPIError as error:
                    if error.code == 6:  # Слишком частые запросы
                        time.sleep(0.5)
                        name = group_data[u'name']
                        posts = self.vk_api.wall.get(owner_id=-group_data['id'], count=100)[u'items']
                    elif error.code == 15:  # Закрытое сообщество
                        posts = "Closed_Wall"
                    else:
                        raise
                except requests.exceptions.ReadTimeout:  #Не дождались ответа от ВК
                    time.sleep(0.5)
                    name = group_data[u'name']
                    posts = self.vk_api.wall.get(owner_id=-group_data['id'], count=100)[u'items']
                groups_posts_base[name] = posts
        except:
            raise
        return groups_posts_base


if __name__ == "__main__":
    my_SW_parser = VkParser('zander5@mail.ru', "Arektar561")
    my_SW_parser.get_new_groups_posts()
