import mysql.connector
from mysql.connector import Error
from model.SchemaGraph import SchemaGraph

class Controller:
    conn = None
    def __init__(self):
        pass

    def startConnection(self):
        """ Connect to MySQL database """
        try:
            conn = mysql.connector.connect(host='127.0.01',
                                           database='dblp',
                                           user='root',
                                           password='Codechef')
            if conn.is_connected():
                print('Connected to MySQL database')

            schema = SchemaGraph(conn)
            schema.readPrimaryKeys()

        except Error as e:
            print(e)

    def closeConnection(self):
        try:
            conn.close()
        except Error as e:
            print(e)
        print("Database connection closed")

controller = Controller()
controller.startConnection()