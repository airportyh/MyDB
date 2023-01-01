import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def list_columns(dbname, username, table_name):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))

    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    
    cur = conn.cursor()
    cur.execute(sql.SQL("""
    SELECT 
       table_name, 
       column_name, 
       data_type 
    FROM 
       information_schema.columns
    WHERE 
       table_name = %s;
    """), (table_name,))
    result = list(cur.fetchall())
    
    conn.close()
    print("Result:")
    print(result)

if len(sys.argv) < 3:
    print("Please provide a DB name, a table name")
    exit(1)

dbname = sys.argv[1]
table_name = sys.argv[2]
list_columns(dbname, "airportyh", table_name)