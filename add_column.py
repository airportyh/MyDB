import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def add_column(dbname, username, table_name, column_name, column_type):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    
    cur = conn.cursor()
    cur.execute(sql.SQL("""
    alter table {}
    add column {} {}
    """).format(
        sql.Identifier(table_name),
        sql.Identifier(column_name),
        sql.Identifier(column_type)
    ))
    conn.close()
    
    print("column %s added for table %s" % (column_name, table_name))

if len(sys.argv) < 5:
    print("Please provide a DB name, a table name, a column name, and a column type")
    exit(1)

dbname = sys.argv[1]
table_name = sys.argv[2]
column_name = sys.argv[3]
column_type = sys.argv[4]
add_column(dbname, "airportyh", table_name, column_name, column_type)