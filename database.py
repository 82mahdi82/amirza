import mysql.connector
from config import *
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
logging.basicConfig(filename=LogFile,level=logging.DEBUG,format=LOG_FORMAT,filemode='w')

def ErrorReport(message, FunctionName, Type='General'):
    if Local:
        print(f' Error in {Type} in function ({FunctionName}): ' + str(message))
    else:
        logging.error(f' Error in {Type} in function ({FunctionName}): ' + str(message))

def CreateDatabase():
    import mysql.connector
    config = {'user': 'root', 'password': 'n3gKJd4CiFTnovf9VpOb', 'host': 'amirzadadlo_db'}
    conn = mysql.connector.connect(**config)
    mycursor = conn.cursor()
    # mycursor.execute("DROP DATABASE IF EXISTS word_game")
    mycursor.execute("CREATE DATABASE IF NOT EXISTS word_game")
    conn.commit()
    conn.close()
    print("Database Created")



class SQL:
    def __init__(self, FuncName='General'):
        self.conn = mysql.connector.connect(**config)
        self.conn.autocommit = False
        self.name = FuncName

    def __enter__(self):
        return self.conn.cursor(dictionary=True)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            ErrorReport(exc_value, FunctionName=self.name, Type='SQL Queries')
            self.conn.rollback()
            return exc_traceback
        else:
            self.conn.commit()
        if self.conn.is_connected():
            self.conn.close()
        
    def cursor(self):
        return self.conn.cursor(dictionary=True)
    


def CreateTable():
    with SQL('Create_letters_Table') as c:
        try:
            SQL_QUERY = ('''
CREATE TABLE IF NOT EXISTS letters (   
    letter           VARCHAR(600) DEFAULT NULL,
    level            int PRIMARY KEY,
    insert_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
''')
            c.execute(SQL_QUERY)

            SQL_QUERY_WORD="""
CREATE TABLE IF NOT EXISTS words (
    level            INT,
    word             VARCHAR(600) DEFAULT NULL,
    insert_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (level) REFERENCES letters(level)
);
"""
            c.execute(SQL_QUERY_WORD)


            SQL_QUERY_USERS="""
CREATE TABLE IF NOT EXISTS users (
    cid              BIGINT PRIMARY KEY,
    name             VARCHAR(200) DEFAULT NULL,
    level            int DEFAULT 0,
    inventory        int DEFAULT 0,
    insert_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_update      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""
            c.execute(SQL_QUERY_USERS)
        except mysql.connector.errors.IntegrityError:
            ErrorReport('CREATE TABLE','CreateTable',Type='SQL Queries')


def insert_letters(letter, level):
    with SQL('insert_letters') as c:
        try:
            c.execute(f'INSERT IGNORE INTO letters (letter, level) VALUES (%s, %s)', (letter, level))
            return c.lastrowid
        except mysql.connector.errors.IntegrityError:
            ErrorReport('insert TABLE','letters',Type='SQL Queries')

def insert_word(level, word):
    with SQL('insert_words') as c:
        try:
            c.execute(f'INSERT IGNORE INTO words (word, level) VALUES (%s, %s)', (word, level))
            return c.lastrowid
        except mysql.connector.errors.IntegrityError:
            ErrorReport('insert TABLE','words',Type='SQL Queries')

def insert_user(cid, name):
    with SQL('insert_users') as c:
        try:
            c.execute(f'INSERT IGNORE INTO users (cid, name) VALUES (%s, %s)', (cid, name))
            return c.lastrowid
        except mysql.connector.errors.IntegrityError:
            ErrorReport('insert TABLE','users',Type='SQL Queries')

def select_letters():
    with SQL('select_letters') as c:
        try:
            c.execute('SELECT * FROM letters')
            res = c.fetchall()
            return res
        except mysql.connector.errors.IntegrityError:
            ErrorReport('select TABLE','select_letters',Type='SQL Queries')

def select_one_letter(level):
    with SQL('select_one_letter') as c:
        try:
            c.execute('SELECT * FROM letters where level = %s', (level,))
            res = c.fetchall()
            return res
        except mysql.connector.errors.IntegrityError:
            ErrorReport('select TABLE','select_one_letter',Type='SQL Queries')


def select_user(cid):
    with SQL('select_user') as c:
        try:
            c.execute('SELECT * FROM users where cid = %s', (cid,))
            res = c.fetchall()
            return res
        except mysql.connector.errors.IntegrityError:
            ErrorReport('select TABLE','user',Type='SQL Queries')


def select_user_by_leve():
    with SQL('select_user_by_leve') as c:
        try:
            c.execute("SELECT * FROM users ORDER BY level DESC LIMIT 10")
            res = c.fetchall()
            return res
        except mysql.connector.errors.IntegrityError:
            ErrorReport('select TABLE','select_user_by_leve',Type='SQL Queries')


def select_all_user():
    with SQL('select_all_user') as c:
        try:
            c.execute('SELECT * FROM users')
            res = c.fetchall()
            return res
        except mysql.connector.errors.IntegrityError:
            ErrorReport('select TABLE','all_user',Type='SQL Queries')


def select_words(level):
    with SQL('select_words') as c:
        try:
            c.execute('SELECT * FROM words where level = %s', (level,))
            res = c.fetchall()
            return res
        except mysql.connector.errors.IntegrityError:
            ErrorReport('select TABLE','select_words',Type='SQL Queries')


def update_letters(letter, level):
    with SQL('update_letters') as c:
        try:
            c.execute(f"update letters set letter = %s where level=%s", (letter,level))
        except mysql.connector.errors.IntegrityError:
            ErrorReport('update user_table','update_letters',Type='SQL Queries')

def levelup(cid):
    with SQL('levelup') as c:
        try:
            c.execute(f"update users set level = level+1 where cid = %s", (cid,))
        except mysql.connector.errors.IntegrityError:
            ErrorReport('update user_table','levelup',Type='SQL Queries')

def update_user(inventory ,cid):
    with SQL('update_user') as c:
        try:
            c.execute(f"update users set inventory = %s where cid = %s", (inventory, cid))
        except mysql.connector.errors.IntegrityError:
            ErrorReport('update user_table','update_user',Type='SQL Queries')

def delete_words(level):
    with SQL('delete_words') as c:
        try:
            c.execute('delete from words where level = %s',(level,))
        except mysql.connector.errors.IntegrityError:
            ErrorReport('delete words','delete_words',Type='SQL Queries')


CreateDatabase()
CreateTable()