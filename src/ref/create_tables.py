import os
import psycopg

conn_dict =  psycopg.conninfo.conninfo_to_dict(os.environ["COCKROACH_DB_URL"])

print(conn_dict)
with psycopg.connect(**conn_dict) as conn:
    conn.execute("DROP TABLE IF EXISTS events")
    # create simple table named events with date,title,description,source
    #   source?: string
    conn.execute("CREATE TABLE events (date date, title text, description text, source text, country text, exchange text, url text, company text)")
    conn.commit()
    # insert some data
    conn.execute("INSERT INTO events VALUES ('2020-01-01', 'New Year', 'Happy New Year', 'source', 'country', 'exchange', 'url', 'company')")
    conn.execute("CREATE UNIQUE INDEX events_url_idx ON events (title, COALESCE(url, '00000000-0000-0000-0000-000000000000'))");
    print("Table events created")
