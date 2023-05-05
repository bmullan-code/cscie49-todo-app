import psycopg2
import os

# Barry Mullan May 2023
# A simple ToDo app that demonstrate an oauth login flow (google) and postgres database persistence

# establish a connection to the database based on url in env var in this format
# DATABASE_URL=postgres://postgres_user:postgres_password@postgres_hostname:5432/postgres_database_name
def connect():
    url = os.environ.get("DATABASE_URL")
    connection = psycopg2.connect(url)
    return connection

# creates the table in the database if it does not already exist
def initialize(): 
    conn = connect()     # Connect to the database
    cur = conn.cursor()  # create a cursor
    # if you already have any table or not id doesnt matter this 
    # will create a todo table for you.
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS todo (id serial \
        PRIMARY KEY, email varchar(100), name varchar(100), complete boolean);''')
 
    conn.commit()  # commit the changes
    cur.close() # close the cursor and connection
    conn.close()

# fetches all rows for the logged in user
def db_fetchall(email):
    conn = connect()
    cur = conn.cursor()
    # Select all todo from the table
    cur.execute("SELECT * FROM todo where email = %s order by id",(email,))
    data = cur.fetchall()
    cur.close()
    conn.close()  
    return data

# creates a row based on email of logged in user, task name and complete status  
def db_create(email,name,complete):
    conn = connect()
    cur = conn.cursor()
    # Insert the data into the table
    cur.execute(
        '''INSERT INTO todo \
        (email,name,complete) VALUES (%s,%s,%s)''',
        (email,name,str(complete)))
    conn.commit()
    cur.close()
    conn.close()

# updates a row, keyed by id and with the updated task name and completion status
def db_update(id,name,complete):
    conn = connect()
    cur = conn.cursor()
    # Update the data in the table
    cur.execute(
        '''UPDATE todo SET name=%s,\
        complete=%s WHERE id=%s''', (name, str(complete), id))
    conn.commit()
    cur.close()
    conn.close()

# deletes a row based on the primary key id
def db_delete(id):
    conn = connect()
    cur = conn.cursor()
    # Delete the data from the table
    cur.execute('''DELETE FROM todo WHERE id=%s''', (id,))
    conn.commit()
    cur.close()
    conn.close()
  
# calls initialize function to create the table
initialize()