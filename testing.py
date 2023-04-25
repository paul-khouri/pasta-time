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
    result = run_search_query_tuples(sql, (), db_path, True)
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


def get_comments(db_path):
    sql="""select news.news_id,news.title,news.subtitle, news.content, comment.comment, member.name
     from news
     left join comment on news.news_id = comment.news_id
     left join member on comment.member_id = member.member_id
     order by news.newsdate desc
     """
    result = run_search_query_tuples(sql, (), db_path, True)

    newsID = 0

    for row in result:
        if row['news_id'] != newsID:
            news_item = "{} {} {}".format(row['news_id'], row['title'], row['subtitle'])
            print(news_item)
            comment = "{} {}".format(row['comment'], row['name'])
            print(comment)
            newsID = row['news_id']
        else:
            comment = "{} {}".format(row['comment'], row['name'])
            print(comment)


def get_comments_trial(db_path):
    news_set = []
    sql="""select news.news_id,news.title,news.subtitle, news.content, news.newsdate, member.name
     from news
     join member on member.member_id = news.member_id
     order by newsdate desc
     """
    result = run_search_query_tuples(sql, (), db_path, True)
    for row in result:
        news_dict = {}
        for k in row.keys():
            news_dict[k] = row[k]
        sql = """select comment.comment, comment.commentdate, member.name
        from comment
        join member on comment.member_id = member.member_id
        where comment.news_id = ?
        order by comment.commentdate asc
        """
        values_tuple = (news_dict['news_id'],)
        result = run_search_query_tuples(sql,values_tuple, db_path, True)
        news_dict['comments'] = result
        news_set.append(news_dict)
    for n in news_set:
        for k in n.keys():
            if k != 'comments':
                print(n[k])
            else:
                for c in n[k]:
                    temp = "{} {} {}".format(c['comment'],c['commentdate'], c['name'])
                    print(temp)









if __name__ == "__main__":
    db_path = 'data/pasta_db.sqlite'
    # get_news(db_path)
    # get_menu(db_path)
    # get_combos(db_path)
    # get_combo_menu(db_path)
    # get_comments(db_path)
    get_comments_trial(db_path)
