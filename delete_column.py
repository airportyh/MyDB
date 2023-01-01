import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def delete_column(dbname, table_name, column_name, username):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    
    try:
        cur = conn.cursor()
        cur.execute(sql.SQL("""
        alter table {}
        drop column {}
        """).format(
            sql.Identifier(table_name),
            sql.Identifier(column_name)
        ))
    finally:
        conn.close()
    
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Please provide a DB name, a table name, a column name")
        exit(1)

    dbname = sys.argv[1]
    table_name = sys.argv[2]
    column_name = sys.argv[3]
    delete_column(dbname, table_name, column_name, "airportyh")
    print("column %s deleted for table %s" % (column_name, table_name))