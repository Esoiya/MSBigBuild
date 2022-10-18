import mariadb

# { "user": "admin", "password": "pinkEleph@nt!", "host": "localhost", "database": "robbingHood"}

class DB:

    def __init__(self, user="admin", password="pinkEleph@nt!", host="94.237.60.14", database="robbingHood"):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = mariadb.connect(
            user=self.user,
            password= self.password,
            host=self.host,
            database=self.database
            )
        
        self.cur = self.conn.cursor()

        return self

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        print("Database updated")
        self.conn.commit()


    def execute(self, query):
        self.cur.execute(query)


    def fetchall(self):
        return self.cur.fetchall()

    def fetch_both(self):
        rows = self.fetchall()
        desc = self.cur.description
        data = [ { desc[i][0]: row[i] for i in range(len(desc)) } for row in rows]
        return data

    
    def __exit__(self):
        print(f"Closing the connection to {self.database}")
        self.cur.close()
        self.conn.close()