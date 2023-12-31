import psycopg2
from psycopg2 import connect, extensions, sql
import psycopg2.extras
import sys

def list_columns(dbname, table_name, username):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql.SQL("""
        SELECT 
           column_name as name, 
           data_type as type
        FROM 
           information_schema.columns
        WHERE 
           table_name = %s;
        """), (table_name,))
        result = list(map(lambda d: dict(d), cur.fetchall()))
    finally:
        conn.close()
    return result
    
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Please provide a DB name, a table name")
        exit(1)

    dbname = sys.argv[1]
    table_name = sys.argv[2]
    print(list_columns(dbname, table_name, "airportyh"))