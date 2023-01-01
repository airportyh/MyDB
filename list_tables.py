import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def list_tables(dbname, username):
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))
    
    cur = conn.cursor()
    cur.execute(sql.SQL(
    """
    select * from pg_catalog.pg_tables
    WHERE schemaname != 'information_schema' AND
    schemaname != 'pg_catalog';
    """))
    results = cur.fetchall()
    
    table_names = list(map(lambda t: t[1], results))
    print("Results:")
    print(table_names)
    
    conn.close()

if len(sys.argv) < 2:
    print("Please provide a DB name")
    exit(1)

dbname = sys.argv[1]
list_tables(dbname, "airportyh")