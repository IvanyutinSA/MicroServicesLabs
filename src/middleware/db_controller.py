import sqlite3


class DBController:
    def __init__(self):
        self.con = sqlite3.connect("wierd")
        self.cur = self.con.cursor()
