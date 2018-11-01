import psycopg2
import regex as re


# NOTE: the table name is "review" you dont need to specify the database name
def retrieve(query):
    try:
        conn = psycopg2.connect(database="assortment",
                                user="assortment_readonly_user",
                                password="I82aOqmZNwj4fIrH",
                                host="core-prod-gameplan-rds.360pi.com",
                                port="5432")
        cur = conn.cursor()
        cur.execute(_add_limit(query))
        rows = cur.fetchall()
    except psycopg2.Error as e:
        print(e.pgerror)
        conn.close()
        return None
    else:
        cur.close()
        conn.close()
        return rows


def _add_limit(query):
    query = re.sub(r"limit[\s][0-9]+", "", query)
    query += " limit 100"
    return query


#print(retrieve("SELECT * from review"))