import sqlite3


class Record:
    def __init__(self, file = "Phone.db"):
        self.file = file
        self.conn = sqlite3.connect(self.file, check_same_thread=False)
        self.cursor = self.conn.cursor()


    def create_table(self,
                     user_id,
                     fields: list ):
        query = "CREATE TABLE IF NOT EXISTS user{0} ("

        # name might be user123
        # fields = [["Phone","TEXT"], [Age, "ÏNTEGER"]]
        # field might look like ["Phone","TEXT"]
        for field in fields:
            query = query + field[0] + " " + field[1] + ", "


        query = query[:-2]
        query = query + ")"
        query = query.format(user_id)

        self.cursor.execute(query)
        self.conn.commit()


    def add_record(self, user_id, data: list):
        # data might look like = ["+4179212245", 15]
        query = "INSERT INTO user{0} VALUES ("

        for value in data:
            if type(value) == str:
                query = query + "'" + value + "'" + ", "
            else:
                query = query + value + ", "

        query = query[:-2]
        query = query + ")"
        # query = "ÏNSERT INTO {0} ('+4179212245', 15)"
        query = query.format(user_id)

        self.cursor.execute(query)
        self.conn.commit()


    def list_all(self, user_id: int):
        query = 'SELECT * FROM user{0}'.format(user_id)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.conn.commit()

        return data
