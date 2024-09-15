import logger

import sqlite3

def init(): # initialize sqlite database
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS lists (id_list INTEGER PRIMARY KEY, id_user INTEGER NOT NULL, name TEXT NOT NULL)") # CHAT_ID will be used as ID for the user
    cursor.execute("CREATE TABLE IF NOT EXISTS todo (id_todo INTEGER PRIMARY KEY, id_list INTEGER NOT NULL, name TEXT NOT NULL, description TEXT, state BOOLEAN NOT NULL)") #DA INSERIRE DATE

    connection.commit()
    connection.close()

    logger.toConsole("Database created!")

def insert(table,values): #DA VALUTARE UTILIZZO DI UN ARRAY PER VALUES

    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO "+table+" VALUES "+values)

    connection.commit()
    connection.close()

    logger.toConsole(f"New row in table {table} with values {values}")

def new_list(chat_id,name):
    insert("lists"+" (id_user,name)",f"({chat_id},\"{name}\")")

def test_output():

    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM lists")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    connection.close()