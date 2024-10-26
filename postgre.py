import psycopg2 as pg
import psycopg2.extras as pgdict
# import the psycopg2 lib
# the .extras allows us to convert the db contents
# into a dict. this will allow us to call data by its column name
# directly rather than use lists indexing

#  define the hostname, port_id, password, user
#  and the database name 
hostname = 'localhost'
port_id = '5432'
password_id = 'november'
user_name = 'postgres'
database_name = 'Sample'
conn = None
cur = None
# Assign values as None to remove error if 
# database cannot be closed/read

# To remove error in failure to find the db
#  let us put our block of code in a try except statement

try:
    # pg.connect is our function we call to 
    # initialize the db
    conn = pg.connect(
    dbname = database_name,
    port = port_id,
    user = user_name,
    password = password_id,
    host = hostname

    )
    # to start executing we need to create a cursor function
    #  we will ref the dict lib here as
    cur = conn.cursor(cursor_factory=pgdict.DictCursor)

    # to prevent table being created everytime
    # let us drop the table if exist first

    cur.execute('DROP TABLE IF EXISTS lee')


    # sample create script written in PostGreSql
    create_script = '''
    CREATE TABLE IF NOT EXISTS lee(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100))'''
    cur.execute(create_script)
    # execute it as above using cur.execute and the command
    add_val = '''
    INSERT INTO lee(name, email)
    VALUES  ('Tony', 'tony@gmail.com'),
        ('John', 'john@gmail.com'),
        ('Mark', 'mark@gmail.com')'''

    cur.execute(add_val)

    alter_script = '''
    ALTER TABLE lee
    ADD COLUMN AGE SMALLINT'''
    cur.execute(alter_script)

    # Define the UPDATE script with placeholders for id and age
    add_val_newcol = '''
UPDATE lee
SET AGE = %s
WHERE id = %s
'''

# Define the list of ages corresponding to each row
    age_val = [30, 43, 22]

# Loop through age values and update each row by its id
    for idx, age in enumerate(age_val, start=1):  # Assuming id starts from 1
        cur.execute(add_val_newcol, (age, idx))
    
    # for i in age_val:
    #     cur.execute(add_val_newcol, i)

    # for rec in cur.fetchmany(2):
    #     print(rec)
    # the above is used to print lines in the db

    # conn.commit() so that the queries may run

    cur.execute('SELECT * FROM lee')
    
    # now, to refrence call name as dict we do the below
    for rec1 in cur.fetchall():
        print(rec1['name'],rec1['email'])

    conn.commit()
except Exception as err:
    print(err)

# we will use finally to make sure cur and conn,
# thus our db, are closed at the end; whether open or not

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

