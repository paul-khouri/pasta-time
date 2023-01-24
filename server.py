from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/menu')
def menu():
    return render_template("menu.html")


@app.route('/combos')
def combos():
    return render_template("combos.html")


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