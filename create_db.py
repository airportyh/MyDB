import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def create_db(dbname, username):
    conn = psycopg2.connect("user=%s" % username)
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    cur = conn.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
    conn.close()
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a DB name")
        exit(1)

    dbname = sys.argv[1]
    create_db(dbname, "airportyh")