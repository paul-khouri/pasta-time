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
        fn = f.get('firstname')
        sn = f.get('secondname')
        em = f.get('email')
        dp = f.getlist('dietarypreference')
        # prep form data if needed again
        form_data={}
        for k, v in f.items():
            if k != "dietarypreference":
                form_data[k] = v
            else:
                dp = f.getlist('dietarypreference')
                for p in dp:
                    form_data[p.lower().replace(" ", "")] = "checked"
        print(form_data)
        return render_template("confirm.html", fn=fn, sn=sn, em=em, dp=dp, form_data=form_data)
    elif request.method == "GET":
        carried_data = request.args
        #print(type(carried_data))
        #print(len(carried_data))

        if len(carried_data) == 0:
            form_data = {
                "firstname": "Paul",
                "secondname": "Jones",
                "email": "dp@c.com",
                "vegan": "checked"
            }
        else:
            print(carried_data)
            form_data=carried_data
        return render_template("signup.html", **form_data)


if __name__ == "__main__":
    app.run(debug=True)