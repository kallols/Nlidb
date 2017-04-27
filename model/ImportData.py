import psycopg2
conn = None
try:
    # self.conn = psycopg2.connect("dbname='dblp' user='postgres' host='localhost' password='Codechef'")
    conn = psycopg2.connect("dbname='library' user='postgres' host='localhost' password='Codechef'")
    # self.conn = psycopg2.connect("dbname='db_b130974cs' user='postgres' host='localhost' password='Codechef'")
except:
    print "I am unable to connect to the database"

cursor = conn.cursor()
# count =0
# query = open("load_employees.sql", "r+")
# for inp in query:
#     count +=1
#     print inp
#

with open("load_salaries.sql", "r+") as f:
    lines = f.readlines()

cursor.execute("""INSERT INTO book VALUES (1, 'Anu', 'K', 'M', 123, 'A')""")

print "connected to database..."