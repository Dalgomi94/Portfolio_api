import traceback
import pymysql
import pymysql.cursors
from config.config import Config


class MySql:
    def __init__(self, is_local=True):
        c = Config()
        self.config = c.get_config(db_type='MYSQL', is_local=is_local)
        self.conn = None
        self.cur = None
        self.ddl_type = [
            'create', 'alter', 'drop', 'truncate', 'rename', ''
        ]
        self.dml_type = [
            'select', 'insert', 'update', 'delete', ''
        ]
        self.db_type = [
            'database', 'table', 'into', 'from', ''
        ]

    def connect(self):
        if self.config is None:
            return False
        self.conn = pymysql.connect(
            host=self.config['host'],
            user=self.config['user'],
            port=self.config['port'],
            password=self.config['password'],
            db=self.config['db'],
            charset=self.config['charset'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        self.cur = self.conn.cursor()
        self.cur.execute(
            'set session autocommit=0;'
        )
        self.cur.execute(
            'set session transaction isolation level read committed;'
        )
        return True

    def disconnect(self):
        try:
            self.cur.close()
            self.conn.close()
        except Exception as e:
            print('=== traceback.print_exc() ===')
            traceback.print_exc()
        # print('disconnect')

    def execute(self, sql, values=None, get_last_id=False):
        if not self.connect():
            return False
        try:
            if values is None:
                self.cur.execute(sql)
            else:
                if isinstance(values, list):
                    self.cur.executemany(sql, values)
                else:
                    self.cur.execute(sql, values)
            if get_last_id:
                self.cur.execute('SELECT LAST_INSERT_ID();')
            result = self.cur.fetchall()
            self.conn.commit()
            return result
        except Exception as e:
            self.conn.rollback()
            print('=== traceback.print_exc() ===')
            traceback.print_exc()
        finally:
            self.disconnect()