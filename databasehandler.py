import sqlite3
from sqlite3 import Error

def init_databases(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        sql = ''' CREATE TABLE IF NOT EXISTS users (
                user_id integer PRIMARY KEY,
                portfolio_id integer NOT NULL,
                points integer NOT NULL
                );'''
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
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

#TODO: Create table to handle user "investment" portfolio    
def create_portfolio_table(db_path):
    connection = create_connection(db_path)
    if connection != None:
        sql = ''' CREATE TABLE IF NOT EXISTS portfolios (
                 portfolio_id integer PRIMARY KEY,
                 FOREIGN KEY (portfolio_id) REFERENCES users (portfolio_id)

        ) '''
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
        except Error as e:
            print(e)

def check_user(db_path, info):
    connection = create_connection(db_path)
    if connection != None:
        try:
            sql = ''' SELECT * FROM users WHERE user_id = ?'''
            cursor = connection.cursor()
            cursor.execute(sql, (info,))
            user_data = cursor.fetchone()
            return user_data
        except Error as e:
            print(e)
    return None
        

def add_user(db_path, info):
    connection = create_connection(db_path)
    if connection != None:
        sql = ''' INSERT INTO users(user_id, portfolio_id, points)
              VALUES(?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(sql, info)
        connection.commit()
        return cursor.lastrowid

def increase_user_score(db_path, info):
    connection = create_connection(db_path)
    if connection != None:
        sql = ''' UPDATE users SET points = points + ? WHERE user_id = ? '''
        cursor = connection.cursor()
        cursor.execute(sql, info)
        connection.commit()
        return cursor.lastrowid