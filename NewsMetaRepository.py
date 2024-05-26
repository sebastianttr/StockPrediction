import duckdb
import uuid

class NewsMetaRepository:

    def __init__(self, csv_file=None):
        self.connection = duckdb.connect(database=':memory:', read_only=False)
        if csv_file is not None:
            self.connection.execute("CREATE TABLE news_meta AS SELECT * FROM read_csv_auto(?)", csv_file)
        self.connection.execute("CREATE TABLE news_meta (id VARCHAR, title VARCHAR UNIQUE, url VARCHAR, timestamp VARCHAR UNIQUE,source VARCHAR)")
        self.connection.execute("CREATE SEQUENCE id_sequence START 1 INCREMENT BY 1;")

    def insert(self, news_meta):
        self.connection.execute("PREPARE insert_meta AS "
                                "INSERT INTO news_meta VALUES (nextval('id_sequence'), ?, ?, ?, ?) ON CONFLICT DO NOTHING;")
        self.connection.execute(f"EXECUTE insert_meta('{news_meta['title']}', '{news_meta['url']}', '{news_meta['timestamp']}', '{news_meta['source']}');")

    def select_all(self):
        return self.connection.execute("SELECT * FROM news_meta").fetchdf()

    def select_by_id(self, id):
        return self.connection.execute("SELECT * FROM news_meta WHERE id = ?", id).fetchdf()

    def select_by_title(self, title):
        return self.connection.execute("SELECT * FROM news_meta WHERE title = ?", title).fetchdf()

    def select_by_url(self, url):
        return self.connection.execute("SELECT * FROM news_meta WHERE url = ?", url).fetchdf()

    def select_by_date(self, date):
        return self.connection.execute("SELECT * FROM news_meta WHERE date = ?", date).fetchdf()

    def delete_all(self):
        self.connection.execute("DELETE FROM news_meta")

    def export(self, csv_file):
        self.connection.execute(f"EXPORT DATABASE '{csv_file}';")

    def close(self):
        self.connection.close()

