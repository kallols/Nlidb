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

        cursor.execute("USE db_b130974cs")

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
        print "\nprinting tables..."
        print SchemaGraph.tables
        print "\nprinting tablerows..."
        print SchemaGraph.tableRows

        SchemaGraph.readPrimaryKeys(self, connection)
        SchemaGraph.findConnectivity(self)

    def readPrimaryKeys(self, connection):
        SchemaGraph.keys = dict()
        cursor = connection.cursor()

        for tableName in SchemaGraph.tables.iterkeys():
            cursor.execute("SHOW keys FROM %s WHERE Key_name = 'PRIMARY'" %tableName)
            rsPrimaryKey = cursor.fetchall()

            SchemaGraph.keys[tableName] = dict()
            pkList = list()

            for row in rsPrimaryKey:
                pkList.append(row[4])

            SchemaGraph.keys[tableName] = pkList
        print "\nprinting primary keys..."
        print SchemaGraph.keys

    def findConnectivity(self):
        SchemaGraph.connectivity = dict()

        for tableName in SchemaGraph.tables:
            SchemaGraph.connectivity[tableName] = list()

        #print SchemaGraph.connectivity

        for table1 in SchemaGraph.tables:
            list_of_tables_for_t1 = list()
            list_of_tables_for_t2 = list()
            for table2 in SchemaGraph.tables:
                if table1 == table2:
                    continue
                else:
                    if SchemaGraph.getJoinKeys(self, table1, table2):
                        list_of_tables_for_t1.append(table2)
                        list_of_tables_for_t2.append(table1)
            SchemaGraph.connectivity[table1] = list_of_tables_for_t1
            SchemaGraph.connectivity[table2] = list_of_tables_for_t2

        print "\nprinting connrctivity:"
        print SchemaGraph.connectivity

    def getJoinKeys(self, table1, table2):
        table1Keys = SchemaGraph.keys[table1]
        table2Keys = SchemaGraph.keys[table2]

        if table1Keys == table2Keys:
            return list()
        keys1ContainedIn2 = True

        for table1Key in table1Keys:
            if not table1Key in SchemaGraph.tables[table2]:
                keys1ContainedIn2 = False
                break

        if keys1ContainedIn2:
            return list(table1Keys)

        keys2ContainedIn1 = True
        for table2Key in table2Keys:
            if not table2Key in SchemaGraph.tables[table1]:
                keys2ContainedIn1 = False
                break

        if keys2ContainedIn1:
            return list(table2Keys)

        return list()

    def getJoinPath(self, table1, table2):
        #todo
        if not(table1 in SchemaGraph.tables) or not(table2 in SchemaGraph.tables):
            return list()

        visited = dict()
        for tableName in SchemaGraph.tables:
            visited[tableName] = False

        prev = dict()
        queue = list()
        queue.append(table1)
        visited[table1] = True
        found = False

        while queue and not found:
            tableCurr = queue[0]
            del queue[0] #remove first

            for tableNext in SchemaGraph.connectivity[tableCurr]:
                if not visited[tableNext]:
                    visited[tableNext] = True
                    queue.append(tableNext)
                    prev[tableNext] = tableCurr
                if tableNext == table2:
                    found = True

        path = list()

        if visited[table2]:
            tableEnd = table2
            path.append(tableEnd)
            while prev[tableEnd]:
                tableEnd = prev[tableEnd]
                path.append(tableEnd)

        return path.reverse()





