from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")

with psycopg2.connect(os.environ["POSTGRESQL_DATABASE"]) as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM public."Invitations"')
        records = cur.fetchall()

        check("Records is not empty", len(records) > 0)

        cur.execute('SELECT * FROM public."Invitations" WHERE full_name = %s', ("Noelia Lloret",))
        records = cur.fetchall()

        print(records)
conn.close()