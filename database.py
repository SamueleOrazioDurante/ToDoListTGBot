import logger

import sqlite3

DB_NAME = "db.db"

def init(): # initialize sqlite database
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS lists (id_list INTEGER PRIMARY KEY, id_user INTEGER NOT NULL, name TEXT NOT NULL, master_id INTEGER NOT NULL)") # CHAT_ID will be used as ID for the user
    cursor.execute("CREATE TABLE IF NOT EXISTS todos (id_todo INTEGER PRIMARY KEY, id_list INTEGER NOT NULL, name TEXT NOT NULL, description TEXT, state BOOLEAN NOT NULL)") #DA INSERIRE DATE

    connection.commit()
    connection.close()

    logger.toConsole("Database created!")

def insert(table,values): #DA VALUTARE UTILIZZO DI UN ARRAY PER VALUES

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    logger.toConsole("INSERT INTO "+table+" VALUES "+values)
    cursor.execute("INSERT INTO "+table+" VALUES "+values)

    connection.commit()
    connection.close()

    logger.toConsole(f"New row in table {table} with values {values}")

def new_list(chat_id,name,master_id):
    insert("lists"+" (id_user,name,master_id)",f"({chat_id},\"{name}\",{master_id})")

def get_list(id_user):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT name,id_list FROM lists WHERE id_user = '"+str(id_user)+"' AND master_id = -1") # get all user`s lists name
    rows = cursor.fetchall()
    
    connection.close()

    return rows # return an array of lists name and id

def get_list_data(id_list):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT name,master_id FROM lists WHERE id_list = '"+str(id_list)+"'") # get list`s informations
    rows = cursor.fetchall()
    
    connection.close()

    return rows[0] # return row

def get_list_lists(id_list):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT name,id_list FROM lists WHERE master_id = '"+str(id_list)+"'") # get list`s slave lists
    rows = cursor.fetchall()
    
    connection.close()

    return rows # return rows

def get_list_todos(id_list):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT name,id_todo FROM todos WHERE id_list = '"+str(id_list)+"'") # get list`s slave todos
    rows = cursor.fetchall()
    
    connection.close()

    return rows # return rows

def new_todo(name,id_list):
    insert("todos"+" (id_list,name,state)",f"({id_list},\"{name}\",FALSE)")

def test_output():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM lists")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    connection.close()
