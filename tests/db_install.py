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
    finally:
        if conn:
            conn.close()
            print("sqlite connection is closed")

def run_search_query_tuples(sql_query,values_tuple, file_path):
    """Run a Query only

    :param (str) sql_query:
    :param (path) file_path:
    :return: (tuple) result
    """
    result = None
    try:
        db = sqlite3.connect(file_path)
        # will get multi dict rather than tuples, needs flask
        #db.row_factory = sql.Row
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
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        #print("connection successful")
        sql_query = open(sql_script_path)
        sql_string = sql_query.read()
        cursor.executescript(sql_string)
        conn.commit()
        #print("Query executed")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while executing sql: {}".format(error))
        return False

    conn.close()
    print("sqlite connection is closed")
    return True

if __name__ == "__main__":
    db = 'pasta_db.sqlite'
    execute_external_script("db_install.sql", "pasta_db.sqlite")
    f = "pasta.csv"
    data = file_reader(f)
    sql = "insert into food(title, price, description, type)values(?,?,?,?)"
    for d in data:
        run_commit_query(sql, tuple(d), db)
    combos= [
        ('Classic', 'Old school Italian pasta dinner', 4),
        ('Allergy free', 'This dinner combo is nut free, dairy free, gluten free and vegan', 4),
        ('Padua', 'A North Italian selection', 4),
        ('Sienna', 'A simple selection for a night at home', 2),
    ]
    sql = "insert into combo(name, description, feeds)values(?,?,?)"
    for c in combos:
        run_commit_query(sql, c, db)

    combo_menu={
        'Classic': ['CONCHIGLIE ALLA BOLOGNESE', 'FETTUCCINE CARBONARA',
                    'CASARECCE PRIMAVERA','RAVIOLI DI RICOTTA','1154 GARLIC & ROSEMARY ROLL',
                    'MARINATED OLIVES','PANNA COTTA', 'TORTA CIOCCOLATO'],
        'Allergy free':['VEGAN AGLIO OLIO','VEGAN VESUVIANA','VEGAN POMODORO','VEGAN PESTO',
                        'GREENS','TORTA CIOCCOLATO'],
        'Padua':['FUSILLI ALLA VODKA','SPAGHETTI AGLIO OLIO E GAMBERETTI', 'RIGATONI POMODORO',
                 'RAVIOLI DI RICOTTA', 'GIARDINIERA', 'ROCKET', 'PANNA COTTA', 'TORTA CIOCCOLATO'],
        'Sienna':['LINGUINE VESUVIANA','RIGATONI POMODORO', 'MARINATED OLIVES','ROCKET','PANNA COTTA']
    }
    # for combo, dishes in the dictionary
    # select to get id of combo
    # loop through dishes and get ids
    for combo, dishes in combo_menu.items():
        for d in dishes:
            sql = """insert into combo_menu(combo_id, food_id)values(
            (select combo_id from combo where name=?), (select food_id from food where title =?)
            )
            """
            values_tuple=(combo, d)
            run_commit_query(sql, values_tuple, db)


    #execute_external_script("db_install.sql", "pasta_db.sqlite")
