from contextlib import contextmanager
import psycopg2
from psycopg2.extras import DictCursor

class DatabasePersistence:
    def __init__(self):
        self._setup_schema()

    @contextmanager
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

    def _load_leaderboard(self):
        with self._database_connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute('''
                SELECT * FROM leaderboard
                ORDER BY score DESC;
                ''')

                leaderboard = cursor.fetchall()

        return leaderboard

    def get_leaderboard(self):
        temp = self._load_leaderboard()
        leaderboard = [(player['name'], player['score'])
                    for player in temp]

        return leaderboard

    def update_leaderboard(self, name, score):
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT COUNT(*) FROM leaderboard''')
                if cursor.fetchone()[0] >= 5:
                    cursor.execute('''
                    DELETE FROM leaderboard
                    WHERE id = (
                    SELECT id FROM leaderboard WHERE score = (
                    SELECT MIN(score) FROM leaderboard)
                    ORDER BY name desc
                    LIMIT 1);''')

                cursor.execute('''
                INSERT INTO leaderboard (name, score)
                VALUES (%s, %s)''',
                (name, score,))