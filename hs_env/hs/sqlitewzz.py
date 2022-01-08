import sqlite3

class DBwzz:
    def __init__(self, client=None):
        self.client = sqlite3.connect('..\db.sqlite3')

    def find(self, character):
        cursor = self.cursor()
        cursor.execute