import os
from os import path


class Reclam_taker():
    def __init__(self):
        self.reclam_path = input("Введите путь к файлу с рекламой: ")
        while not path.exists(self.reclam_path):
            print("Файл не найден")
            self.reclam_path = input("Введите путь к файлу с рекламой: ")
        self.magic_end = self.reclam_path.split(".")[-1]

    def get_text(self):
        text = ''
        if self.magic_end == "txt":
            text = self.from_text_file()
        return text

    def from_text_file(self):
        with open(self.reclam_path) as text_file:
            reclam = text_file.read()
        return reclam

def write_result(simularity_dict):
    with open('result.txt') as result_file:
        for group in simularity_dict:
            result_file.write(group, )


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