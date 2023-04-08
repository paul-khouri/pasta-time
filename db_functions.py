import sqlite3
import csv
import string #for strip

def run_commit_query(sql_query,values_tuple, file_path):
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = 1")
        print("connection successful")
        cursor.execute(sql_query, values_tuple)
        conn.commit()
        print("Commit Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Commit Error: {}".format(error))
        return False
    conn.close()
    print("sqlite connection is closed")
    return True

def run_search_query_tuples(sql_query,values_tuple, file_path, rowfactory=False):
    """Run a query

    :param (str) sql_query: str
    :param (tuple) values_tuple: tuple (can be empty)
    :param (path) file_path: str
    :return: (tuple) result
    """
    result = None
    try:
        db = sqlite3.connect(file_path)
        # will get multi dict rather than tuples, needs flask
        if rowfactory:
            db.row_factory = sqlite3.Row
        cursor = db.cursor()
        #print("connection successful")
        cursor.execute(sql_query,values_tuple)
        result = cursor.fetchall()
        #print("Search Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Error running search query tuples: {}".format(error))
        return None
    db.close()
    if result is None:
        print("No search values were found")
    return result

def file_reader(f):
    collected_data = []
    with open(f , mode='r', encoding='utf-8-sig') as csv_file:
        csv_read = csv.reader(csv_file, delimiter = "," , quotechar='"', quoting=csv.QUOTE_MINIMAL)
        count = 0
        for row in csv_read:
            collected_data.append( [x.strip() for x in row] )
            count+=1
    print(count)
    return collected_data


def execute_external_script(sql_script_path, db_path):
    """Read a sql file and use to create a database

    :param sql_script_path: str (path to sql file)
    :param db_path: str (path to db dile)
    :return: bool
    """
    try:
        # connect to database (if it is not there it will be created)
        conn = sqlite3.connect(db_path)
        # the cursor allows us to do things with the database
        cursor = conn.cursor()
        #print("connection successful")
        # open and read the sql file
        sql_query = open(sql_script_path)
        sql_string = sql_query.read()
        # use the cursor to execute the script in the file
        cursor.executescript(sql_string)
        # commit (aka save) what has been done
        conn.commit()
        #print("Query executed")
        # shut down the cursor
        cursor.close()
    except sqlite3.Error as error:
        # if there is an error print it out in the console
        print("Error while executing sql: {}".format(error))
        # return False if another part of the program needs to know of the failure
        return False
    # all okay if we are here
    # shut down the connection
    conn.close()
    print("sqlite connection is closed")
    return True


if __name__ == "__main__":
    sql_path = 'data/create_db.sql'
    db_path = 'data/pasta_db.sqlite'
    execute_external_script(sql_path,db_path)
