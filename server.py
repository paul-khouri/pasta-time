from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def run_search_query_tuples(sql_query,values_tuple, file_path, row_factory=False):
    """Run a Query only with tuple to go with question marks

    :param (str) sql_query:
    :param values_tuple : tuple
    :param (path) file_path:
    :return: (tuple) result
    """
    db = None
    try:
        db = sqlite3.connect(file_path)
        # will get multi dict rather than tuples, needs flask
        if row_factory:
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
    if db:
        db.close()
        print("sqlite connection is closed")
    return result


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/menu')
def menu():
    db_path = 'data/pasta_db.sqlite'
    sql_query = 'select title, description, price, type from food'
    result = run_search_query_tuples(sql_query, (), db_path)
    return render_template("menu.html", menu=result)


@app.route('/combos')
def combos():
    db_path = 'data/pasta_db.sqlite'
    sql_query = """select combo.name, food.title, food.price from combo 
                    join combo_menu on combo.combo_id = combo_menu.combo_id
                    join food on combo_menu.food_id=food.food_id"""
    result = run_search_query_tuples(sql_query, (), db_path)
    total = 0
    name = result[0][0]
    print(name)
    for row in result:
        print(row[1])
        total += row[2]
        # if we get to the end of the combo
        if name != row[0]:
            # print the toatl price
            print(total)
            total = 0
            # set and print the the new name variable
            name = row[0]
            print(name)
    print(total)



    return render_template("combos.html", combos=result)


if __name__ == "__main__":
    app.run(debug=True)
