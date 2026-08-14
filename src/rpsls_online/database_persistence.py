import psycopg2

class DatabasePersistence:
    def __init__(self):
        self._setup_schema()

    def _database_connect(self):
        try:
            with psycopg2.connect(dbname='leaderboard') as conn:
                yield conn
        finally:
            conn.close()

    def _setup_schema(self):
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public' AND 
                table_name = 'leaderboard';'''
                )

                if cursor.fetchone()[0] == 0:
                    cursor.execute('''CREATE TABLE leaderboard (
                    id SERIAL PRIMARY KEY,
                    name text NOT NULL,
                    score int NOT NULL CHECK (score >= 0)
                    );'''
                    )