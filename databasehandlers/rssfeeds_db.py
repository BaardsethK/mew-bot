import sqlite3
from sqlite3 import Error

def init_databases(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)

        sql_create_servers = ''' CREATE TABLE IF NOT EXISTS servers (
            server_id PRIMARY KEY,
            channel_id integer NOT NULL
            );'''

        sql_create_rss = ''' CREATE TABLE IF NOT EXISTS rss_feeds (
                id integer PRIMARY KEY,
                link text NOT NULL,
                server_id integer NOT NULL,
                FOREIGN KEY (server_id)
                REFERENCES servers (server_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
                );'''

        try:
            cursor = connection.cursor()
            cursor.execute(sql_create_servers)
            cursor.exectue(sql_create_rss)
            connection.close()
        except Error as e:
            print(e)
    except Error as e:
        print(e)
    
def create_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except Error as e:
        print(e)
    return connection

def check_rss(db_path, info):
    connection = create_connection(db_path)
    if connection != None:
        try:
            sql = ''' SELECT * FROM rss_feeds WHERE server_id = ?'''
            cursor = connection.cursor()
            cursor.execute(sql, (info,))
            rss_feed_data = cursor.fetchall()
            return rss_feed_data
        except Error as e:
            print(e)
    return None
        

def add_rss(db_path, info):
    connection = create_connection(db_path)
    if connection != None:
        sql = ''' INSERT INTO rss_feeds(link, server_id)
            VALUES(?,?) '''
        cursor = connection.cursor()
        cursor.execute(sql, info)
        connection.commit()
        return cursor.lastrowid

def remove_rss(db_path, info):
    connection = create_connection(db_path)
    if connection != None:
        sql = ''' DELETE FROM rss_feeds WHHERE id = ? and server_id = ? '''
        cursor= connection.cursor()
        cursor.execute(sql, info)
        connection.commit()

def add_server(db_path, info):
    connection = create_connection(db_path)
    if connection != None:
        sql = ''' INSERT INTO servers(server_id, channel_id)
            VALUES(?,?) '''
        cursor = connection.cursor()
        cursor.execute(sql, info)
        connection.commit()
        return cursor.lastrowid

def remove_server(db_path, info):
    connection = create_connection(db_path)
    if connection != None:
        sql = ''' DELETE FROM servers WHERE server_id = ? '''
        cursor = connection.cursor()
        cursor.execute(sql, info)
        connection.commit()