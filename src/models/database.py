import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
    
    # here I can use a decorator that initialized the cursor and after the query is complete closes the connection

    def update(self, query, args=set()):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        con.commit()
        con.close()

    def fetchone(self, query, args):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(query, args)
        result = cur.fetchone()
        con.close()
        return result
    
    def fetchall(self, query, args):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(query, args)
        result = cur.fetchall()
        con.close()
        return result


