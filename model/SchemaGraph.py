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

        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
        table_names = cursor.fetchall()

        for table_name in table_names:
            #print table_name[0]
            SchemaGraph.tables[table_name[0]] = dict()
            SchemaGraph.tableRows[table_name[0]] = dict()

            cursor.execute("select column_name, data_type from information_schema.columns where table_name = '%s'" % (table_name[0]))
            col_info = cursor.fetchall()

            col_name_type_dict = dict()
            for col in col_info:
                col_name_type_dict[col[0]] = col[1]
            #print col_name_type_dict

            col_name_values_dict = dict()
            for col in col_info :
                cursor.execute("SELECT %s FROM %s ORDER BY RANDOM() LIMIT 20"
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
        SchemaGraph.findConnectivity(self, connection)

    def readPrimaryKeys(self, connection):
        SchemaGraph.keys = dict()
        cursor = connection.cursor()
        #get primary keys for each table
        for tableName in SchemaGraph.tables.iterkeys():
            cursor.execute("""SELECT a.attname, format_type(a.atttypid, a.atttypmod)
                              AS data_type FROM   pg_index i
                              JOIN   pg_attribute a ON a.attrelid = i.indrelid
                              AND a.attnum = ANY(i.indkey)
                              WHERE  i.indrelid = '%s'::regclass
                              AND i.indisprimary;""" %tableName)
            rsPrimaryKey = cursor.fetchall()

            SchemaGraph.keys[tableName] = dict()
            pkList = list()

            for row in rsPrimaryKey:
                pkList.append(row[0])

            SchemaGraph.keys[tableName] = pkList
        print "\nprinting primary keys..."
        print SchemaGraph.keys

    def findConnectivity(self, connection):
        SchemaGraph.connectivity = dict()

        for tableName in SchemaGraph.tables:
            SchemaGraph.connectivity[tableName] = list()

        cursor = connection.cursor()

        #get foreign keys from table
        cursor.execute("""SELECT tc.table_name, kcu.column_name, ccu.table_name
                AS foreign_table_name, ccu.column_name
                AS foreign_column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY'""")

        foreignKeys = cursor.fetchall()

        for foreignKey in foreignKeys:
            table1 = foreignKey[0]
            table2 = foreignKey[2]
            if not table2 in SchemaGraph.connectivity[table1]:
                SchemaGraph.connectivity[table1].append(table2)
            if not table1 in SchemaGraph.connectivity[table2]:
                SchemaGraph.connectivity[table2].append(table1)
        print "\nprinting connectivity: "
        print SchemaGraph.connectivity

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





