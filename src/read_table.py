import os
import psycopg

conn_dict =  psycopg.conninfo.conninfo_to_dict(os.environ["COCKROACH_DB_URL"])

print(conn_dict)
with psycopg.connect(**conn_dict) as conn:
    cursor = conn.execute("SELECT * FROM events");
    print(cursor.fetchall())
