import psycopg2
from model.SchemaGraph import SchemaGraph

class Controller:
    conn = None
    def __init__(self):
        pass

    def startConnection(self):
        """ Connect to MySQL database """
        try:
            conn = psycopg2.connect("dbname='dblp' user='postgres' host='localhost' password='Codechef'")
        except:
            print "I am unable to connect to the database"
        schema = SchemaGraph(conn)


    def closeConnection(self):
        try:
            conn.close()
        except Error as e:
            print(e)
        print("Database connection closed")

controller = Controller()
controller.startConnection()