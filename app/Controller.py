import mysql.connector
from mysql.connector import Error

class Controller:
    def __init__(self):
        pass

    def start_connection(self):
        """ Connect to MySQL database """
        try:
            conn = mysql.connector.connect(host='127.0.01',
                                           database='dblp',
                                           user='root',
                                           password='Codechef')
            if conn.is_connected():
                print('Connected to MySQL database')
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")

            for(table_name) in cursor:
                print table_name

            print "\ncolumns:\n"
            cursor.execute("SHOW COLUMNS FROM author")

            for(column_name) in cursor:
                print column_name


        except Error as e:
            print(e)

        finally:
            conn.close()
            print("Database connection closed")

controller = Controller()
controller.start_connection()