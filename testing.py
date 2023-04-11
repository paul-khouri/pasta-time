from db_functions import run_search_query_tuples


def get_news(db_path):
    sql = """select news.title, news.subtitle, news.content,news.newsdate, member.name 
    from news
    join member on news.member_id = member.member_id;
    """
    result = run_search_query_tuples(sql, (), db_path, True)

    for row in result:
        for k in row.keys():
            print(k)
            print(row[k])


def get_menu(db_path):
    sql = """select title, description, price, type from food"""
    result = run_search_query_tuples(sql,(), db_path, True)
    for row in result:
        temp = ""
        for k in row.keys():
            temp += str(row[k])
            temp += ', '
        print(temp)

def get_combos(db_path):
    sql = """select name, description, feeds from combo"""
    result = run_search_query_tuples(sql, (), db_path, True)
    for row in result:
        temp = ""
        for k in row.keys():
            temp += str(row[k])
            temp += ', '
        print(temp)

def get_combo_menu(db_path):
    sql = """select combo.name, combo.description, combo.feeds, food.title, food.price, food.type
    from combo
    join combo_menu on combo.combo_id = combo_menu.combo_id
    join food on combo_menu.food_id = food.food_id"""
    result = run_search_query_tuples(sql, (), db_path, True)
    name = ""
    for row in result:
        if row['name'] != name:
            output = "Combo: {} , {}, feeds {}".format(row['name'], row['description'], row['feeds'])
            print(output)
            name = row['name']
        output = "{} {} {}".format(row['title'], row['price'], row['type'])
        print(output)






if __name__ == "__main__":
    db_path = 'data/pasta_db.sqlite'
    #get_menu(db_path)
    #get_combos(db_path)
    get_combo_menu(db_path)
