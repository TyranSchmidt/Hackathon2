import flask
from flask import request
from database import *
from flask import session

app = flask.Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class CustomError(Exception):
    pass

@app.route('/', methods=["GET", "POST"])
def sign_up():
    country_list = country_db()
    if request.method == "POST":
        if request.form['btn'] == "Log in":
            session['username'] = request.form.get("Username")
            password_in = request.form.get("Password_in")
            is_logged_in = log_in(session['user_email'], password_in)
            if is_logged_in:
                return flask.redirect("profile")
        elif request.form['btn'] == "Sign up":
            full_name = request.form.get("Full_name")
            session['username'] = request.form.get("Username")
            new_username = check_username(session['username'])
            if new_username == False:
                session.pop('username', None)
                raise CustomError("That username is already taken.")
            email = request.form.get("Email")
            country = request.form.get("Country")
            password = request.form.get("Password")
            id_hex = make_id()
            new_account(id_hex, full_name, session['username'], email, country, password)
            new_profile(Full_name=full_name, Username=session['username'], Country=country, Unique_id=id_hex, Hidden="yes")
            return flask.redirect("help")
    return flask.render_template("sign_up_page.html", country_list=country_list)

@app.route('/help', methods=["GET", "POST"])
def help():
    if request.method == "POST":
        if request.form['nav-link'] == "sign_out":
            session.pop('username', None)
            return flask.redirect('sign_up')
    return flask.render_template("help.html")

@app.route('/profile', methods=["GET", "POST"])
def profile():
    country_list = country_db()
    no_hidden = "no"
    Full_name, Date_of_birth, session['Username'], Country, City, Unique_id, Hobbies, Hidden=open_profile(session['username'])
    if request.method == "POST":
        if request.form['btn'] == "Apply Changes":
            full_name = request.form.get("Full_name")
            date_of_birth = request.form.get("Date_of_birth")
            session['username'] = request.form.get("Username")
            country = request.form.get("Country")
            city = request.form.get("City")
            unique_id = request.form.get("Unique ID")
            hobbies = request.form.get("Hobbies")
            hidden = request.form.get('Hidden')
            if hidden == "yes":
                no_hidden = "no"
            else:
                no_hidden = "yes"
            Full_name, Date_of_birth, session['Username'], Country, City, Unique_id, Hobbies, Hidden=update_profile(full_name, date_of_birth, session['username'], country, city, unique_id, hobbies, hidden)
        elif request.form['nav-link'] == "sign_out":
            session.pop('username', None)
            return flask.redirect('sign_up')
    return flask.render_template("profile.html", country_list=country_list, full_name=Full_name, date_of_birth=Date_of_birth, username=session['Username'], country=Country, city=City, unique_id=Unique_id, hobbies=Hobbies, hidden=Hidden, no_hidden=no_hidden)

@app.route('/view', methods=["GET", "POST"])
def view():
    country_list = country_db()
    x = table_parts()
    rows = table_items()
    return flask.render_template("buddy-finder.html", country_list=country_list, x=x, rows=rows)

@app.route('/search', methods=["GET", "POST"])
def search():
    country_list = country_db()
    user_profiles = searchable_users()
    if request.method == "POST":
        print(request.form)
        username = request.form.get("username", "")
        country = request.form.get("country", "")
        city = request.form.get("city", "")
        hobbies = request.form.get("hobbies", "")
        user_profiles = search_db(username, country, city, hobbies)
    return flask.render_template("search.html", country_list=country_list, user_profiles=user_profiles)

if __name__ == "__main__":
    app.run(debug=True)

