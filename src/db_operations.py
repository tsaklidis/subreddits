import os
import sqlite3

from helpers import log


class DB:
    def __init__(self):

        tbl = 'CREATE TABLE IF NOT EXISTS rollbacks(id TEXT PRIMARY KEY, value TEXT, is_comment INTEGER);'

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.conn = sqlite3.connect(dir_path + '/rollback_db.sqlite')

        self.cur = self.conn.cursor()
        self.cur.execute(tbl)
        self.conn.commit()

    def insert(self, data):
        query = 'INSERT INTO rollbacks (id, value, is_comment) VALUES (?, ?, ?)'
        values = (data['id'], data['value'], data['is_comment'])
        try:
            self.cur.execute(query, values)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as db_error:
            print(db_error)
            return False

    def get_value_by_id(self, id):
        query = 'SELECT value FROM rollbacks WHERE id = ?'
        values = (id,)
        self.cur.execute(query, values)
        row = self.cur.fetchone()
        return row

    def __del__(self):
        self.conn.close()
