# -*- coding: utf-8-*-
import os
from os import path


class Reclam_taker():
    def __init__(self, path):
        self.reclam_path = path
        self.magic_end = self.reclam_path.split(".")[-1]

    def get_text(self):
        text = ''
        if self.magic_end == "txt":
            text = self.from_text_file()
        return text

    def from_text_file(self):
        with open(self.reclam_path,encoding='utf-8') as text_file:
            text = text_file.read()
        return text

def write_result(text):
    with open('result.html','a+') as result_file:
        result_file.write(text)


if __name__ == "__main__":
    my_taker = Reclam_taker()
    text = my_taker.get_text()
    import Text_parser
    import Vec_worker

    my_text_parser = Text_parser.Text_analyser()
    words = my_text_parser.prepareText(text)

    Vec_worker.library_prepearing()
    analyser = Vec_worker.Tree_analyser()
    vecs = analyser.take_words_vec(words)
    print(vecs)