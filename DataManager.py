import psycopg2
import regex as re
import configparser
import datetime
import psycopg2.extras

config = configparser.ConfigParser()
config.read("connection_cfg.ini")
PROD_NAME = "assortment"
PROD_USER = "assortment_readonly_user"
PROD_PASSWORD = config['PROD']['PASSWORD']
PROD_HOSTNAME = config['PROD']['HOSTNAME']

DEV_NAME = "assortment"
DEV_USER = "assortment_user"
DEV_PASSWORD = config['DEV']['PASSWORD']
DEV_HOSTNAME = config['DEV']['HOSTNAME']


def update_last_run():
    config = configparser.ConfigParser()
    with open("lastrun_cfg.ini", "w") as cfgfile:
        d = datetime.datetime.now()
        config.add_section("PERSISTENCE")
        config.set("PERSISTENCE", "last_run", d.strftime("%Y-%m-%d %H:%M:%S"))
        config.write(cfgfile)


def get_last_run():
    config = configparser.ConfigParser()
    config.read("lastrun_cfg.ini")
    last_run = config['PERSISTENCE']['last_run']
    return datetime.datetime.strptime(last_run, "%Y-%m-%d %H:%M:%S")


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


def get_reviews(client_id, last_run, current_run):
    with _connect(PROD_NAME, PROD_USER, PROD_PASSWORD, PROD_HOSTNAME) as conn:
        cur = conn.cursor()
        query = "SELECT root_channel_product_id, review_text, rating FROM review WHERE channel_id = {client_id} AND ts >= '{date1}' AND ts < '{date2}'".format(
            client_id=str(client_id),
            date1=last_run.strftime('%Y-%m-%d'),
            date2=current_run.strftime('%Y-%m-%d'))
        try:
            cur.execute(query)
            rows = cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print (e.pgerror)
            return None


def save_scores(timestamp, entity, productid, rating, scores):
    with _connect(DEV_NAME, DEV_USER, DEV_PASSWORD, DEV_HOSTNAME) as conn:
        cur = conn.cursor()
        query = "INSERT INTO review_results(ts, entity, productid, rating, sp, wp, wn, sn) VALUES ('{0}','{1}',{2},{3},{4},{5},{6},{7})".format(
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
            conn.commit()
            # id = cur.fetchone()[0]
            cur.close()
        except psycopg2.Error as e:
            pass
            print(e.pgcode)


def save_scores_batch(entity_list):
    with _connect(DEV_NAME, DEV_USER, DEV_PASSWORD, DEV_HOSTNAME) as conn:
        cur = conn.cursor()
        query = "INSERT INTO review_results(ts, entity, productid, rating, sp, wp, wn, sn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        psycopg2.extras.execute_batch(cur, query, entity_list)
        conn.commit()
        cur.close()


def _reset_table():
    with _connect(DEV_NAME, DEV_USER, DEV_PASSWORD, DEV_HOSTNAME) as conn:
        cur = conn.cursor()
        query = "DELETE from review_results"
        try:
            cur.execute(query)
            conn.commit()
            # id = cur.fetchone()[0]
            cur.close()
        except psycopg2.Error as e:
            pass
            print(e.pgcode)

# print(get_reviews(605775, (datetime.datetime.today() - datetime.timedelta(days=1000)), datetime.datetime.today()))
