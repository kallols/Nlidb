import psycopg2
from model.SchemaGraph import SchemaGraph

class Controller:
    conn = None
    def __init__(self):
        pass

    def startConnection(self):
        """ Connect to MySQL database """
        try:
            self.conn = psycopg2.connect("dbname='dblp' user='postgres' host='localhost' password='ashwin2048'")
        except:
            print "I am unable to connect to the database"
        schema = SchemaGraph(self.conn)


controller = Controller()
controller.startConnection()