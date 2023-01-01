import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def create_table(dbname, username, table_name):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    
    cur = conn.cursor()
    cur.execute(sql.SQL("create table {} ()").format(sql.Identifier(table_name)))
    conn.close()
    
    print("table %s created for %s" % (table_name, dbname))

if len(sys.argv) < 3:
    print("Please provide a DB name and a table name")
    exit(1)

dbname = sys.argv[1]
table_name = sys.argv[2]
create_table(dbname, "airportyh", table_name)