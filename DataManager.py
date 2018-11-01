import psycopg2



def connect():
    conn = psycopg2.connect(database="testdb", user="assortment_readonly_user", password="I82aOqmZNwj4fIrH", host="127.0.0.1", port="5432")
