from db_functions import run_search_query_tuples


def get_sqlite_schema(db_path):
    """Get list of tables in the database

    :param db_path:
    :return: None
    """
    sql = "select name from sqlite_master where type='table';"
    # notice the empty bracket in the second argument
    result = run_search_query_tuples(sql, (), db_path)
    for x in result:
        for y in x:
            print(y)

def get_news(db_path):
    """

    :param db_path:
    :return:
    """
    sql = """select news.title, news.subtitle, news.content, news.newsdate, member.name
    from news
    join member on news.member_id= member.member_id
    """
    result = run_search_query_tuples(sql, (), db_path, True)
    for r in result:
        for k in r.keys():
            output = "Key: {} , Value: {}".format(k, r[k])
            print(output)








if __name__ == "__main__":
    db_path = 'data/pasta_db.sqlite'
    # get_master_data(db_path)
    # get_sqlite_schema(db_path)
    get_news(db_path)
