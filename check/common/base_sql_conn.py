import pymysql

class DataBaseConnection:
    def __init__(self, host, port, user, passwd, db, sql):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.sql = sql

    def get_data(self):
        (conn, cur) = self.connect()
        cur.execute(self.sql)
        data = cur.fetchall()
        self.disconnect(conn, cur)
        return data

    def connect(self):
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
            cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
            return (conn, cur)
        except:
            print('connection error!')

    def disconnect(self, conn, cur):
        conn.commit()
        # 关闭指针对象
        cur.close()
        # 关闭连接对象
        conn.close()