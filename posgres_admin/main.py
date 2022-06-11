import psycopg2
import random


# Administration algorithms
def help_docs():
    '''Desc: No need for parameters, the function just outputs the commands
              that can be used in postgres command line ORM
    '''
    docs = ("\n# PostgreSQL Commands:\n"
            "\n"
            "`create table`      -- For creating tables\n"
            "`drop table`        -- For deleting tables\n"
            "`insert row`        -- For entering data to a table\n"
            "`delete row`        -- For deleting data from a table\n"
            "`list tables`       -- For listing all the tables in the db\n"
            "`list rows`         -- For listing the rows of a table\n"
            "`update all rows`   -- For updating all rows in a single column\n"
            "`update single row` -- For updating a single row of column\n"
            "`limit rows`        -- For limiting the rows\n"
            "`limit between`     -- For limiting between the rows\n"
            "`order by`          -- For ordering the table\n"
            "`populate db`       -- If you are lazy to enter inserts \n"
            "`quit`              -- For quiting the program"
            "\n"
            )
    print(docs)


def create_table(cursor):
    '''Desc: creates a table in the selected database
    '''
    name = input("Table name: ")
    columns = int(input("How many columns: "))

    # Drop the table if it exists in the database
    cursor.execute("DROP TABLE IF EXISTS " + name)

    query = "CREATE TABLE " + str(name) + \
            "(id SERIAL PRIMARY KEY"
    i = 0
    while (i < columns):
        col_name = input("Column " + str(i + 1) + " name: ")
        col_type = input(
            "Column " + str(i + 1) + " type (text or int or float): "
        )
        query += ", " + str(col_name) + " " + str(col_type).upper()
        i += 1
    query += "); "
    # Execute the SQL query
    cursor.execute(query)


def populate_db(cursor):
    '''Desc: This function requires a db.connection.cursor as a arg. The main
       of this function is to create a dummy table named by the user
       and populates it
    '''
    table_name = input("What do you want to name your table: ")

    # Drop the table if it exists in the database
    cursor.execute("DROP TABLE IF EXISTS " + table_name)

    # Creating the table
    create_table = (
        "CREATE TABLE " + str(table_name) + "( " +
        "id SERIAL PRIMARY KEY, " +
        "Name TEXT, " +
        "Age INT, " +
        "Salary INT" +
        ");"
    )

    cursor.execute(create_table)

    # Populating the database
    dummy_data_names = ["Emily", "Hannah", "Madison", "Ashley", "Sarah",
                        "Samantha", "Jessica", "Elizabeth", "Taylor", "Lauren",
                        "Alyssa", "Kayla", "Victoria", "Rachel", "Jasmine",
                        "Abigail", "Brianna", "Olivia", "Emma", "Megan",
                        "Anna", "Sydney", "Destiny", "Morgan", "Jennifer",
                        "Kaitlyn", "Nicole", "Amanda", "Katherine", "Natalie",
                        "Savannah", "Chloe", "Rebecca", "Stephanie", "Maria",
                        "Allison", "Isabella", "Amber", "Mary", "Danielle",
                        "Brooke", "Michelle", "Sierra", "Katelyn", "Andrea",
                        "Kimberly", "Courtney", "Erin", "Hailey", "Alexandra",
                        "Sophia", "Mackenzie", "Gabrielle", "Jordan"]

    # Populate the data with 30 entries in the future I will add the feature
    # so that the user can select how many entries they want.
    for i in range(0, 50, 1):
        query = (
            "INSERT INTO " + table_name +
            " (Name, Age, Salary) VALUES (" +
            "'" + dummy_data_names[random.randint(0, 54)] + "', "
            + str(random.randint(0, 100)) + ", " +
            str(random.randint(1000, 5000))
            + ");"
        )
        cursor.execute(query)


def insert_row(cursor):
    '''Desc: this
    '''
    name = input("Table name: ")
    cursor.execute("SELECT column_name FROM information_schema.columns\
                    WHERE table_name = \'" + str(name) + "'")
    columns = cursor.fetchall()

    query = "INSERT INTO " + str(name) + "("
    values = ""
    i = 1  # `i` starts at 1 because the `0` is a auto incrementing int
    while (i < len(columns)):
        query += str(columns[i][0]) + ", "
        user_data = input(str(columns[i][0] + ": "))
        values += user_data + ", "
        i += 1
    query = query[:-2]
    query += ") VALUES(" + values
    query = query[:-2]
    query += ");"

    # Execute the SQL query
    cursor.execute(query)


def drop_table(cursor):
    '''Desc: deletes the selected table
    '''
    name = input("Table name: ")
    verification = input("Are you sure ? (y or n) ")
    if (verification == "y"):
        query = "DROP TABLE IF EXISTS " + str(name)
    # Execute the SQL query
    cursor.execute(query)


def delete_row(cursor):
    '''Desc: deletes the selected row
    '''
    name = input("Table name: ")
    id = input('Row id: ')
    query = "DELETE FROM " + str(name) + " WHERE id = " + id + ";"

    cursor.execute(query)


def list_tables(cursor):
    '''Desc: List tables
    '''
    cursor.execute("SELECT table_name FROM information_schema.tables\
                    WHERE table_schema = 'public' ")
    tables = cursor.fetchall()

    for table in tables:
        print(table)


def list_rows(cursor):
    '''Desc: This list all of the rows
    '''
    name = input("Table name: ")
    cursor.execute("SELECT * FROM " + str(name))
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def limit_rows(cursor):
    '''Desc: This function requires a cursor paramter which is a
              db.connection.cursor. and returns you the limited rows of a table
    '''
    table_name = input("Table name: ")
    limit = input("How many rows you want: ")

    query = "SELECT * FROM " + str(table_name) + " LIMIT " + str(limit) + ";"

    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def limit_between(cursor):
    '''Desc: This function requires a db.connection.cursor parameter. It will
              print out the selected rows of a table to the terminal
    '''
    table_name = input("Table name: ")
    starting_row = input("Starting from which row: ")
    limit = input("How many rows you want: ")

    query = (
        "SELECT * FROM " + str(table_name) + " LIMIT " + str(limit) +
        " OFFSET " + starting_row + ";"
    )

    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def order_by(cursor):
    '''Desc: This function requires a db.connection.cursor parameter. It will
              print out the table in a acsending or decesnding order
    '''
    table_name = input("Table name: ")
    column_name = input("Order by (col name): ")
    ordering_way = input("Ordering way (desc or asc): ")

    query = (
        "SELECT * FROM " + str(table_name) + " ORDER BY " + str(column_name) +
        " " + str(ordering_way.upper()) + ";"
    )

    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)


def update_all_rows(cursor):
    '''Desc: This program requires a parameter which is a dbconnection.cursor
              The functions updates all of the data inside a table
    '''
    table_name = input("Table name: ")
    column_name = input("Column name: ")
    new_value = input("New value: ")

    query = (
        "UPDATE " + str(table_name) + " SET " + str(column_name) + " = "
        + str(new_value) + ";"
    )

    cursor.execute(query)


def update_single_row(cursor):
    '''Desc: This program  requires a parmeter which is a dbconnection.cursor
              The function updates a single data in a row of a specific column
    '''
    table_name = input("Table name: ")
    row_id = input("Row id: ")
    column_name = input("column name: ")
    new_value = input("New value: ")

    query = (
        "UPDATE " + str(table_name) + " SET " + str(column_name) + " = " +
        str(new_value) + " WHERE id = " + str(row_id) + ";"
    )

    cursor.execute(query)


# Database connection
dbname = None
connection = None

try:
    # Get the database name from the user
    dbname = input("\nDatabase name: ")
    username = input("\nDB username: ")
    password = input("\nDB password: ")
    connection = psycopg2.connect(dbname=str(dbname), user=username, password=password)
    cursor = connection.cursor()

    print("Type 'help' for docs")

    while(True):
        user_input = input("\n$ ")

        if (user_input == "help"):
            help_docs()
        elif (user_input == "create table"):
            create_table(cursor)
        elif (user_input == "drop table"):
            drop_table(cursor)
        elif (user_input == "insert row"):
            insert_row(cursor)
        elif (user_input == "delete row"):
            delete_row(cursor)
        elif (user_input == "list tables"):
            list_tables(cursor)
        elif (user_input == "list rows"):
            list_rows(cursor)
        elif (user_input == "update all rows"):
            update_all_rows(cursor)
        elif (user_input == "update single row"):
            update_single_row(cursor)
        elif (user_input == "limit rows"):
            limit_rows(cursor)
        elif (user_input == "limit between"):
            limit_between(cursor)
        elif (user_input == "order by"):
            order_by(cursor)
        elif (user_input == "populate db"):
            populate_db(cursor)
        elif (user_input == "quit"):
            break
        else:
            print("You have entered invalid characters! Type `help`")

        connection.commit()

except psycopg2.DatabaseError as e:
    print("Error: " + str(e))
finally:
    if connection is True:
        connection.close()
