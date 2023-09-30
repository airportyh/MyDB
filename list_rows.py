import psycopg2
from psycopg2 import connect, extensions, sql
import psycopg2.extras
import sys

def list_rows(dbname, table_name, username):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql.SQL("""
        SELECT 
           *
        FROM 
           {}
        ORDER BY id
        """).format(sql.Identifier(table_name)), (table_name,))
        result = list(map(lambda d: dict(d), cur.fetchall()))
    finally:
        conn.close()
    return result