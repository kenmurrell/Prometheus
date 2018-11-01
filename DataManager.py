import psycopg2
import regex as re
import datetime


# NOTE: the table name is "review" you dont need to specify the database name
def _add_limit(query):
    query = re.sub(r"limit[\s][0-9]+", "", query)
    query += " limit 100"
    return query


def _connect():
    try:
        conn = psycopg2.connect(database="assortment",
                                user="assortment_readonly_user",
                                password="I82aOqmZNwj4fIrH",
                                host="core-prod-gameplan-rds.360pi.com",
                                port="5432")
        return conn
    except psycopg2.Error as e:
        print(e.pgerror)
        conn.close()
        return None


def get_products(client_id):
    with _connect() as conn:
        cur = conn.cursor()
        query = "SELECT root_channel_product_id FROM review WHERE channel_id = {client_id}".format(client_id=str(client_id))
        try:
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print (e.pgerror)
            return None


def get_reviews(prod_id, date1, date2):
    with _connect() as conn:
        cur = conn.cursor()
        query = "SELECT review_text FROM review WHERE root_channel_product_id={prod_id} AND ts >= '{date1}' AND ts < '{date2}'".format(prod_id=prod_id,
                                                                                                                                   date1=date1.strftime('%Y-%m-%d'),
                                                                                                                                   date2=date2.strftime('%Y-%m-%d'))
        try:
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print (e.pgerror)
            return None

