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
