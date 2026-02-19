import duckdb
import os

class DBConnector:
    def __init__(self, db_path='data/taxi_data.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = duckdb.connect(db_path)

    def execute(self, query, params=None):
        if params:
            return self.conn.execute(query, params)
        return self.conn.execute(query)

    def query_to_df(self, query):
        return self.conn.execute(query).df()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DBConnector()
    print("Database connected successfully.")
    db.close()
