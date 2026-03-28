import pymysql

class DBUtil:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="mall")
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def query(self, sql,args=None):
        self.cursor.execute(sql,args)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()