import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def create_row(dbname, table_name, columns, values, username):
    assert len(columns) == len(values)
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    try:
        cur = conn.cursor()
        values_list = ", ".join(["%s"] * len(values))
        columns_list = ", ".join(["{}"] * len(columns))
        the_sql = sql.SQL("""
        insert into {} (%s)
        values (%s)
        RETURNING id
        """ % (columns_list, values_list)).format(
            sql.Identifier(table_name),
            *map(lambda col: sql.Identifier(col), columns)
        )
        cur.execute(
            the_sql, 
            values
        )
        result = cur.fetchone()
        
        return result[0]
    finally:
        conn.close()
    
if __name__ == "__main__":
    dbname = "test_db"
    table_name = "persons"
    result = create_row(dbname, table_name, ("name", "age"), ("Ben", 31), "airportyh")
    print("values inserted table %s" % (table_name,))
    print(result)