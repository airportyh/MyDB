import psycopg2
from psycopg2 import connect, extensions, sql
import sys

def update_row(dbname, table_name, id, columns, values, username):
    assert len(columns) == len(values)
    conn = psycopg2.connect("dbname=%s user=%s" % (dbname, username))
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)
    try:
        cur = conn.cursor()
        set_list = sql.SQL(", ").join(
            map(lambda column: sql.SQL("{} = %s").format(sql.Identifier(column)), columns)
        )
        the_sql = sql.SQL("""
        update {}
        set {}
        where id = %s
        returning id
        """).format(
            sql.Identifier(table_name),
            set_list
        )
        print(the_sql)
        cur.execute(
            the_sql, 
            values + [id],
        )
        result = cur.fetchone()
        
        return result is not None
    finally:
        conn.close()
    
if __name__ == "__main__":
    dbname = "test_db"
    table_name = "persons"
    result = update_row(dbname, table_name, 1, ("name", "age"), ("Tobias", 32), "airportyh")
    print("values inserted table %s" % (table_name,))
    print(result)