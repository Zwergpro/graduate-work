import psycopg2
from sshtunnel import SSHTunnelForwarder

from private.settings import DATABASES, SSH_SETTINGS


class DB:
    cursor = None
    server = None

    def __enter__(self):
        self.server = SSHTunnelForwarder(**SSH_SETTINGS)
        self.server.start()

        try:
            db = psycopg2.connect(**DATABASES['default'])
            self.cursor = db.cursor()
        except Exception:
            self.server.close()
            raise

        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor is not None:
            self.cursor.close()

        if self.server is not None:
            self.server.stop()
