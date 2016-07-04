import pymysql

class MySQL:
    def __init__(self,host,user,password,db,port,charset,timeout):
        print('connect...')
        self.conn = pymysql.connect(host=host,user=user,password=password,db=db,port=port,charset=charset,connect_timeout=timeout)
        self.cursor = self.conn.cursor()

    def update(self,sql):
        print('update sql...')
        self.cursor.execute(sql)
        self.conn.commit()

    def query(self,sql):
        print('query sql...')
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            print('update fail')

    def __del__(self):
        print('close connect...')
        self.cursor.close()
        self.conn.close()

if __name__=='__main__':
    db = MySQL('127.0.0.1','root','123456','dandan',3306,'utf8',5)
    rows = db.query('select * from article')
    print(rows)
