from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
db_path = 'data/pasta_db.sqlite'


@app.template_filter()
def news_date(sqlite_dt):
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %H:%M")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/menu')
def menu():
    return render_template("menu.html")


@app.route('/combos')
def combos():
    return render_template("combos.html")

@app.route('/news')
def news():
    # check if an id has been sent. Means delete that id
    delete_id= request.args
    print(delete_id)
    if len(delete_id) !=0:
        sql = "delete from news where news_id =?"
        values_tuple=(delete_id['id'],)
        result = run_commit_query(sql, values_tuple, db_path)
        print(result)
    # -------------
    # query for the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
      from news
      join member on news.member_id= member.member_id
      order by news.newsdate desc;
      """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html", news=result)


@app.route('/news_cu', methods=['GET', 'POST'])
def news_cu():
    if request.method=='POST':
        f=request.form
        values_tuple = (f['title'],f['subtitle'],f['content'])
        sql = """insert into news (title,subtitle, content, newsdate, member_id)
        values(?,?,?, datetime('now'), 2)"""
        result = run_commit_query(sql, values_tuple,db_path)
        print(result)
        return redirect(url_for('news'))
    elif request.method=='GET':
        cu_id = request.args
        print(cu_id)
        test_dict={
            "title": "Party night!",
            "subtitle": "Come along after hours next Saturday 5 May",
            "content" : "Meet the staff and enjoy value drinks and entree plates"
        }

        return render_template("news_cu.html",
                               title=test_dict['title'],
                               subtitle=test_dict['subtitle'],
                               content=test_dict['content'])

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        f = request.form
        return render_template("confirm.html", form_data=f)
    elif request.method == "GET":
        carried_data = request.args
        print(carried_data)
        if len(carried_data) == 0:
            temp_form_data={
                "firstname" : "James",
                "secondname" : "Lovelock",
                "email": "jl@gmail.com",
                "aboutme" : "I have been in love with Italian food all my life"
            }
            #temp_form_data = {}
        else:
            temp_form_data= carried_data
        return render_template("signup.html", **temp_form_data)



if __name__ == "__main__":
    app.run(debug=True)