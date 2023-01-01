import psycopg2
from psycopg2 import connect, extensions, sql
import psycopg2.errors
import sys

def create_table(dbname, table_name, username):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    cur = conn.cursor()
    try:
        cur.execute(sql.SQL(
        """
        create table {} (
            id serial
        )
        """).format(sql.Identifier(table_name)))
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide a DB name and a table name")
        exit(1)

    dbname = sys.argv[1]
    table_name = sys.argv[2]
    create_table(dbname, table_name, "airportyh")
    print("table %s created for %s" % (table_name, dbname))