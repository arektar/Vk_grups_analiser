import os
from os import path


class Reclam_taker():
    def from_text_file(self, path):
        with open(path) as text_file:
            reclam = text_file.read()
        return reclam
