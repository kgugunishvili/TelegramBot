import sqlite3


class Record:
    def __init__(self, file = "Phone.db"):
        self.file = file
        self.conn = sqlite3.connect(self.file, check_same_thread=False)
        self.cursor = self.conn.cursor()


    def create_table(self,
                     user_id,
                     fields: list ):
        query = f"CREATE TABLE IF NOT EXISTS user{user_id} ("

        # name might be user123
        # fields = [["Phone","TEXT"], [Age, "ÏNTEGER"]]
        # field might look like ["Phone","TEXT"]
        for field in fields:
            query = query + field[0] + " " + field[1] + ", "


        query = query[:-2]
        query = query + ")"

        self.cursor.execute(query)
        self.conn.commit()


    def add_record(self, user_id, data: list):
        # data might look like = ["+4179212245", 15]
        query = f"INSERT INTO user{user_id} VALUES ("

        for value in data:
            if type(value) == str:
                query = query + "'" + value + "'" + ", "
            else:
                query = query + value + ", "

        query = query[:-2]
        query = query + ")"
        # query = "INSERT INTO {0} ('+4179212245', 15)"
        self.cursor.execute(query)
        self.conn.commit()


    def list_all(self, user_id: int):
        query = f'SELECT * FROM user{user_id}'
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.conn.commit()

        return data


    def search(self, user_id, demand):
        query = f"SELECT Phones FROM user{user_id} WHERE Names='{demand}'"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return data
