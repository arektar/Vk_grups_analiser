# -*- coding: cp1251*-
import pymorphy2


class Text_analyser():
    def __init__(self):
        self.ps_good_table = {"NOUN": "_S", "ADJF": "_A", "VERB": "_V", "INFN": "_V"}
        """
        pymorph word2vec
        NOUN    _S  	имя существительное	хомяк
        ADJF    _A  	имя прилагательное (полное)	хороший
        ADJS    _A  	имя прилагательное (краткое)	хорош
        COMP    _ADV	компаратив	лучше, получше, выше
        VERB    _V	    глагол (личная форма)	говорю, говорит, говорил
        INFN    _V	    глагол (инфинитив)	говорить, сказать
        PRTF	_S      причастие (полное)	прочитавший, прочитанная
        PRTS	_S      причастие (краткое)	прочитана
        GRND	--      деепричастие	прочитав, рассказывая
        NUMR	--      числительное	три, пятьдесят
        ADVB	--      наречие	круто
        NPRO	--      местоимение-существительное	он
        PRED	--      предикатив	некогда
        PREP	--      предлог	в
        CONJ	--      союз	и
        PRCL	--      частица	бы, же, лишь
        INTJ	--      междометие	ой
        """
        self.morph = pymorphy2.MorphAnalyzer()
        pass

    def prepare_posts_text(self, groups_posts_dict):
        groups_base = {}
        for group in groups_posts_dict:
            posts = groups_posts_dict[group]
            groups_base[group] = []
            for post in posts:
                text = post[u'text']
                parse_result = self.prepareText(text)
                if parse_result: groups_base[group].append(parse_result)
                # print(text)
        print(groups_base)

        return groups_base

    def prepareText(self, text):
        "подготовка текста для работы с моделью: получение списка слов (нет), определение части речи (нет), отсеивание лишних слов и т.д."
        text_tree = []
        text = text.replace('\n\n', ' ')
        text = text.replace('\n', ' ')
        sentences = self.take_sentences(text)[:-1]
        for sentence in sentences:
            tegs = self.easy_tokenizer(sentence)
            tegs = self.sym_filter(tegs)
            tegs = self.parts_of_speach(tegs)
            if tegs: text_tree.append(tegs)

        return text_tree

    def take_sentences(self, text):
        stop_sym = [".", "!", "?", ";", "..."]
        sentence_list = []
        not_end = True
        for_many_point = 1
        while not_end:
            stop_pos = -1
            for sym in stop_sym:
                sym_pos = text.find(sym)
                if sym_pos != -1: sym_pos = sym_pos + len(sym)
                while sym_pos + 3 < len(text) and sym_pos != -1 and not text[sym_pos + 1].isupper():
                    if text[sym_pos] in stop_sym:
                        if sym != "." or text[sym_pos] != ".": break
                    sym_pos = text.find(sym, sym_pos)
                    if sym_pos != -1: sym_pos = sym_pos + len(sym)
                if stop_pos == -1 and sym_pos != -1:
                    stop_pos = sym_pos
                elif sym_pos != -1 and sym_pos < stop_pos:
                    stop_pos = sym_pos
                elif sym_pos == len(text):
                    stop_pos = sym_pos

            if stop_pos == -1:
                stop_pos = len(text)
                not_end = False
            if stop_pos == 1:
                text = text[stop_pos:]
                continue
            sentence_list.append(text[:stop_pos])

            text = text[stop_pos:]
            if text == []: not_end = False

        return sentence_list

    def easy_tokenizer(self, text):
        pause_sym = [u",", u".", u"!", u"?", u";", u":", u"(", u")", u"[", u"]", u"'", u'"', u"<", u">", u"{", u"}",
                     u"-", u"«", u"»"]
        tokens = text.split()
        i = 0
        while i < len(tokens):
            token = tokens[i]
            while token[-1] in pause_sym and len(token) > 1:
                sym = token[-1]
                token = token[:-1]
                tokens[i] = token
                tokens.insert(i + 1, sym)
            while token[0] in pause_sym and len(token) > 1:
                sym = token[0]
                token = token[1:]
                tokens[i] = token
                tokens.insert(i, sym)
            i += 1
        return tokens

    def sym_filter(self, tegs_list):
        words_list = []
        for teg in tegs_list:
            if not teg: continue
            if teg.isalpha(): words_list.append(teg)
        return words_list

    def parts_of_speach(self, words_list):
        dict_tags = []
        for word in words_list:
            ps = self.morph.parse(word)[0].tag.POS
            if ps in self.ps_good_table:
                dict_tag = self.morph.parse(word)[0].normal_form
                dict_tag = dict_tag + self.ps_good_table[ps]
                if dict_tag: dict_tags.append(dict_tag)
        return dict_tags


if __name__ == "__main__":

    parser = Text_analyser()
    VK_groups_dict = {"Test_groupe": [{"text":"""Разработка системы имеет своей целью улучшение эффективности
    рекламы путем выявления сообществ, подходящих заданной рекламе по своей тематике, что позволит качественно
    улучшить рекламирование в сообществах социальных сетей. Поскольку анализ основан на ежемесячной выборке сообщений,
    появляющихся на странице социальной группы, программа определяет актуальную на данный момент тематику этой группы.
    """}]}
    groups_base = parser.prepare_posts_text(VK_groups_dict)

    import  Vec_worker
    Vec_worker.library_prepearing()
    analyser = Vec_worker.Tree_analyser()
    vecs = analyser.take_groups_vecs(groups_base)
    print(vecs)
    #from Data_base_worker import
