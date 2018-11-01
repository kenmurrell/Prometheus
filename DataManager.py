import psycopg2
import regex as re
import configparser
import datetime

config = configparser.ConfigParser()
config.read("config.ini")
PROD_NAME = "assortment"
PROD_USER = "assortment_readonly_user"
PROD_PASSWORD = config['PROD']['PASSWORD']
PROD_HOSTNAME = config['PROD']['HOSTNAME']

DEV_NAME = "assortment"
DEV_USER = "assortment_user"
DEV_PASSWORD = config['DEV']['PASSWORD']
DEV_HOSTNAME = config['DEV']['HOSTNAME']


# NOTE: the table name is "review" you dont need to specify the database name
def _add_limit(query):
    query = re.sub(r"limit[\s][0-9]+", "", query)
    query += " limit 100"
    return query


def _connect(name, user, password, host):
    try:
        conn = psycopg2.connect(database=name,
                                user=user,
                                password=password,
                                host=host,
                                port="5432")
        return conn
    except psycopg2.Error as e:
        print(e.pgerror)
        conn.close()
        return None


def get_products(client_id):
    with _connect(PROD_NAME, PROD_USER, PROD_PASSWORD, PROD_HOSTNAME) as conn:
        cur = conn.cursor()
        query = "SELECT root_channel_product_id FROM review WHERE channel_id = {client_id}".format(
            client_id=str(client_id))
        try:
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print (e.pgerror)
            return None


def get_reviews(prod_id, date1, date2):
    with _connect(PROD_NAME, PROD_USER, PROD_PASSWORD, PROD_HOSTNAME) as conn:
        cur = conn.cursor()
        query = "SELECT review_text, rating FROM review WHERE root_channel_product_id={prod_id} AND ts >= '{date1}' AND ts < '{date2}'".format(
            prod_id=prod_id,
            date1=date1.strftime('%Y-%m-%d'),
            date2=date2.strftime('%Y-%m-%d'))
        try:
            cur.execute(_add_limit(query))
            rows = cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print (e.pgerror)
            return None


def save_scores(timestamp, entity, productid, rating, scores):
    with _connect(DEV_NAME, DEV_USER, DEV_PASSWORD, DEV_HOSTNAME) as conn:
        cur = conn.cursor()
        query = "INSERT INTO review_results(ts, object, productid, rating, sp, wp, wn, sn) VALUES {0},{1},{2},{3},{4},{5},{6},{7}".format(
            timestamp,
            entity,
            productid,
            rating,
            scores["SP"],
            scores["WP"],
            scores["WN"],
            scores["SN"])
        try:
            cur.execute(query)
            cur.commit()
        except psycopg2.Error as e:
            print (e.pgerror)


print(get_reviews(605775, (datetime.datetime.today() - datetime.timedelta(days=1000)), datetime.datetime.today()))
