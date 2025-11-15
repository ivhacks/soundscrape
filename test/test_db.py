from unittest import TestCase

import psycopg
import pytest


@pytest.mark.xdist_group(name="database")
class DatabaseTests(TestCase):
    def test_connect(self):
        conn = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="soundscrape",
            user="soundscrape",
            password="password",
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        cursor.fetchone()
        cursor.close()
        conn.close()
