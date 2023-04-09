from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples
from datetime import datetime

app = Flask(__name__)
db_path = 'data/pasta_db.sqlite'


@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %I:%M %p")


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
    # query for the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
       from news
       join member on news.member_id= member.member_id
       order by news.newsdate desc;
       """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html", news=result)






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