from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from q_set import get_combo_menu
from datetime import datetime
from dateutil import tz

app = Flask(__name__)
app.secret_key = "sgdjkdgjdfgkdjfgk"
db_path = 'data/pasta_db.sqlite'


def log_in_check(auth=0):
    """Check that id and authorisation in session keys
    :param : auth (int) default = 0

    :return: bool
    """
    if 'id' in session.keys() and 'authorisation' in session.keys():
        if session['authorisation'] == auth:
            return True
        else:
            return False
    else:
        return False


@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %Y %I:%M %p")


@app.template_filter()
def make_price(p):
    return "${:.2f}".format(p)


@app.template_filter()
def make_discount(p):
    discount = p*0.85
    return "${:.2f} with 15% discount = ${:.2f}".format(p, discount)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/menu')
def menu():
    sql = """select title, description, price, type from food"""
    result = run_search_query_tuples(sql, (), db_path, True)
    return render_template("menu.html", menu=result)


@app.route('/combos')
def combos():
    result = get_combo_menu(db_path)
    return render_template("combos.html", combos=result)


@app.route('/news')
def news():
    """Get all news items and comments

    :return: template
    """
    # list to hold dictionary of news items and the comments
    news_set = []
    # get the news items in descending order
    sql="""select news.news_id,news.title,news.subtitle, news.content, news.newsdate, member.name
     from news
     join member on member.member_id = news.member_id
     order by newsdate desc
     """
    result = run_search_query_tuples(sql, (), db_path, True)
    # for each news item
    for row in result:
        # start a dictionary to for the item
        news_dict = {}
        # loop and add keys and values to a fresh , mutable dictionary
        for k in row.keys():
            news_dict[k] = row[k]
        # for the particular news item
        # query all its comments in ascending order
        sql = """select comment.comment_id, comment.comment, comment.commentdate, member.name, member.member_id
        from comment
        join member on comment.member_id = member.member_id
        where comment.news_id = ?
        order by comment.commentdate asc
        """
        values_tuple = (news_dict['news_id'],)
        result = run_search_query_tuples(sql,values_tuple, db_path, True)
        # add the list of the comments (immutable dictionary) to a new comments key
        news_dict['comments'] = result
        # add to news_set list
        news_set.append(news_dict)
    return render_template("news.html", news=news_set)


@app.route('/news_cud', methods=['GET', 'POST'])
def news_cud():
    # basic log-in check
    if not log_in_check():
        error = "You are not authorised to access this page"
        return render_template("error.html", message=error)
    # collect data from the web address
    # this happens regardless of GET or POST
    data = request.args
    required_keys = ['id', 'task']
    # check that we have the required keys
    # run error page if a problem
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)
    # yes, we have an id and a task key
    # if I have arrived directly from the page
    if request.method == "GET":
        # is the task to delete ?
        if data['task'] == 'delete':
            #delete comments
            sql = "delete from comment where news_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            sql = "delete from news where news_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        # is the task to update ?
        elif data['task'] == 'update':
            sql = """ select title, subtitle, content from news where news_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("news_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        # is the task to add ?
        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'title': 'Test Title', 'subtitle': 'Test subtitle', 'content': 'Test Content'}
            temp = {}  # switches off temp
            return render_template("news_cud.html",
                                   id=0,
                                   task=data['task'],
                                   **temp)
        # run error if not one of these
        else:
            message = "Unrecognised task coming from news page"
            return render_template('error.html', message=message)
    # if it is a POST, we are coming from a form submission
    elif request.method == "POST":
        # collected form information
        f = request.form
        # print(f)
        if data['task'] == 'add':
            # add the new news entry to the database
            # have a guaranteed session id
            sql = """insert into news(title,subtitle,content, newsdate, member_id) 
                        values(?,?,?, datetime('now', 'localtime'),?)"""
            values_tuple = (f['title'], f['subtitle'], f['content'], session['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # once added redirect to news page to see the newly added news item
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            # we are updating so 'rewrite' all the data even if
            sql = """update news set title=?, subtitle=?, content=?, 
            newsdate=datetime('now', 'localtime') where news_id=?"""
            values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the sent id
            return redirect(url_for('news'))
        else:
            # let's put in an error catch
            message = "Unrecognised task coming from news form submission"
            return render_template('error.html', message=message)


@app.route('/comment_cud', methods=['GET','POST'] )
def comment_cud():
    # collect data from the web address
    # this happens regardless of GET or POST
    data = request.args
    if request.method == "GET":
        required_keys = ['id', 'task']
    elif request.method == "POST":
        # passed on form action
        required_keys = ['news_id', 'member_id', 'task']
    # check that we have the required keys
    # run error page if a problem
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)
    if request.method == "GET":
        # is the task to delete ?
        if data['task'] == 'delete':
            sql = "delete from comment where comment_id = ?"
            values_tuple = (data['id'],)
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
    elif request.method == "POST":
        f = request.form
        if data['task'] == 'add':
            sql = """insert into comment(news_id, member_id, comment, commentdate)
            values(?, ?, ?, datetime('now', 'localtime'))
            """
            values_tuple = (data['news_id'],data['member_id'], f['comment'] )
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news')+"#"+data['news_id'])


@app.route('/members')
def members():
    sql = """select * from member"""
    result = run_search_query_tuples(sql, (), db_path, True)
    return render_template("members.html", member=result)


@app.route('/member_cud', methods=['GET','POST'] )
def member_cud():
    return redirect(url_for('members'))


@app.route('/login', methods=["GET","POST"])
def login():
    """Get log-in from user, test and respond

    :return: template
    """
    # check current session status (should be empty)
    print(session)
    if request.method == "GET":
        # go to log-in page with pre-filled values
        return render_template("log-in.html", email='m@g.com', password='temp')
    elif request.method == "POST":
        f=request.form
        print(f)
        sql= """ select member_id, name, password, authorisation from member where email = ? """
        values_tuple=(f['email'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        print(result)
        if result:
            print("have a result")
            result = result[0]
            if result['password'] == f['password']:
                print("yep all okay")
                session['id'] = result['member_id']
                session['name'] = result['name']
                session['authorisation'] = result['authorisation']
                return redirect(url_for('index'))
            else:
                error = "Your credentials are not recognised"
                return render_template("log-in.html", error=error)
        else:
            error = "Your credentials are not recognised"
            return render_template("log-in.html", error=error)
        # test if form password matches stored password


@app.route('/logout')
def logout():
    session.clear()
    referrer = request.referrer
    print(referrer)
    return redirect(referrer)
    #return redirect(url_for('index'))


@app.route('/signup', methods=["GET", "POST"])
def signup():
    referrer = request.referrer
    print(referrer)
    if request.method == "POST":
        f = request.form
        sql = """insert into member(name, email, bio, password, authorisation)
        values(?,?,?,?, 1)"""
        values_tuple= (f['membername'],f['email'], f['aboutme'],f['password'])
        result = run_commit_query(sql, values_tuple, db_path)
        if result:
            return render_template("log-in.html", email=f['email'])
        else:
            message = """Unfortunately, something went wrong. 
                      Please make sure you have not signed up before 
                      with the same email. """
            return render_template('error.html',message=message)
    elif request.method == "GET":
        carried_data = request.args
        print(carried_data)
        if len(carried_data) == 0:
            temp_form_data = {
                "membername": "James",
                "secondname": "Lovelock",
                "email": "jl@gmail.com",
                "aboutme": "I have been in love with Italian food all my life"
            }
            # temp_form_data = {}
        else:
            temp_form_data = carried_data
        return render_template("signup.html", **temp_form_data)





if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=80)
