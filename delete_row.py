import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def delete_row(dbname, table_name, id, username):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    try:
        cur = conn.cursor()
        cur.execute(
            sql.SQL("""
            delete from {} where id = %s returning id
            """).format(
                sql.Identifier(table_name)
            ), 
            (id,)
        )
        result = cur.fetchone()
        
        return result is not None
    finally:
        conn.close()
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide a DB name, a table name, and an ID")
        exit(1)

    dbname = sys.argv[1]
    table_name = sys.argv[2]
    id = sys.argv[3]
    result = delete_row(dbname, table_name, id, "airportyh")
    print("deleted row %s from table %s" % (id, table_name))
    print(result)