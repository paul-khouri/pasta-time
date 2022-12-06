import sqlite3
from db_install import run_search_query_tuples, run_commit_query


def get_master_data(p):
    """

    :param p:
    :return: None
    """
    sql = 'select * from sqlite_master;'
    result = run_search_query_tuples(sql,(), p)
    print(type(result))
    for x in result:
        print(x)

def get_sqlite_schema(p):
    # name has been changed to sqlite_schema but still
    # seems to be master in this this installation
    sql = 'select name from sqlite_master;'
    result = run_search_query_tuples(sql,(), p)
    for x in result:
        for y in x:
            print(y)

def select_all_table(p,table):
    sql = "select * from {}".format(table)
    result = run_search_query_tuples(sql, (), p)
    for row in result:
        print(row)

def select_combos(p):
    sql= """select combo.name, food.title from combo 
    join combo_menu on combo.combo_id = combo_menu.combo_id
    join food on combo_menu.food_id = food.food_id
    """
    result = run_search_query_tuples(sql, (), p)
    for row in result:
        print(row)

def test_delete(p):
    sql = "delete from combo where name =?"
    values_tuple = ('Classic',)
    run_commit_query(sql, values_tuple, p)

def other(p):
    sql = "pragma foreign_keys=1;"
    run_commit_query(sql,(), p)
    sql = "pragma foreign_keys;"
    result = run_search_query_tuples(sql,(),p)
    print(result)
    print(sqlite3.sqlite_version)



if __name__ == "__main__":
    p = 'pasta_db.sqlite'
    #get_master_data(p)
    #get_sqlite_schema(p)
    #select_all_table(p, 'combo_menu')
    #select_all_table(p, 'combo')
    select_combos(p)
    #test_delete(p)
    #other(p)
    print()