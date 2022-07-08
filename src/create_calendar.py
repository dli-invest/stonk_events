import os
import psycopg2

conn = psycopg2.connect(os.environ["COCKROACH_DB_URL"])

with conn.cursor() as cur:
    cur.execute("SELECT now()")
    res = cur.fetchall()
    conn.commit()
    print(res)