import sqlite3
import os
import openai


class genSQL:
    def __init__(self, db_path:str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def get():
        pass

    def gensql_agent():
        pass

    def prompt():
        pass

    def verify():
        pass


if __name__="__main__":
    pass
