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
    sql = "select *, (select name from member where member.member_id = news.member_id) as 'member name' from news;"
    result = run_search_query_tuples(sql, (), db_path, True)
    for x in result:
        print(x['title'])
        print(x['subtitle'])
        print(x['member name'])



if __name__ == "__main__":
    db_path = 'data/pasta_db.sqlite'
    # get_master_data(db_path)
    # get_sqlite_schema(db_path)
    get_news(db_path)
