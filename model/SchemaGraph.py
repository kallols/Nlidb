import mysql.connector
from mysql.connector import Error

class SchemaGraph :

    tables = None
    tableRows = None
    keys = None
    connectivity = None

    def __init__(self,connection):

        SchemaGraph.tables = dict()
        SchemaGraph.tableRows = dict()

        print "Retrieving schema graph..."
        cursor = connection.cursor()

        cursor.execute("USE dblp")

        cursor.execute("SHOW TABLES")
        table_names = cursor.fetchall()

        for table_name in table_names:
            #print table_name[0]
            SchemaGraph.tables[table_name[0]] = dict()
            SchemaGraph.tableRows[table_name[0]] = dict()

            cursor.execute("SHOW columns FROM %s" % (table_name[0]))
            col_info = cursor.fetchall()
            col_name_type_dict = dict()
            for col in col_info:
                col_name_type_dict[col[0]] = col[1]
            #print col_name_type_dict

            col_name_values_dict = dict()
            for col in col_info :
                cursor.execute("SELECT %s FROM %s ORDER BY RAND() LIMIT 20"
                               % (col[0], table_name[0]))
                row = cursor.fetchall()
                col_name_values_dict[col[0]] = row


            SchemaGraph.tables[table_name[0]] = col_name_type_dict
            SchemaGraph.tableRows[table_name[0]] = col_name_values_dict

        print "printing tables..."
        print SchemaGraph.tables
        print "printing tablerows..."
        print SchemaGraph.tableRows










