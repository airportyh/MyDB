import psycopg2
from psycopg2 import connect, extensions, sql

def list_dbs(username):
    # Connect to your postgres DB
    conn = psycopg2.connect("user=%s" % username)

    cur = conn.cursor()

    cur.execute("select datname from pg_database")
    results = list(map(lambda t: t[0], cur.fetchall()))
    conn.close()
    return results

if __name__ == "__main__":
    list_dbs("airportyh")