from db_functions import run_search_query_tuples


def get_combo_menu(db_path):
    sql = """select combo.name, combo.description, combo.feeds, food.title, 
    food.price, food.type, food.description as fooddescription
    from combo
    join combo_menu on combo.combo_id = combo_menu.combo_id
    join food on combo_menu.food_id = food.food_id"""
    result = run_search_query_tuples(sql, (), db_path, True)
    return result