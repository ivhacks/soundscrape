from unittest import TestCase

import psycopg
import pytest


def _get_conn():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="soundscrape",
        user="soundscrape",
        password="password",
    )


@pytest.mark.xdist_group(name="database")
class DatabaseTests(TestCase):
    def test_connect(self):
        conn = _get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        cursor.fetchone()
        cursor.close()
        conn.close()
