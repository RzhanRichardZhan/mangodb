from flask import Flask, render_template, request, redirect, url_for, abort, session, escape
from pymongo import Connection


app = Flask(__name__)
app.secret_key='{\xdft\xb7\x06f\x9b\xa4\x0eP\xe1n\xdd\xd4\x93\x01\xd3`\xc1\xe5\xc1|\x0e`'



@app.route("/", methods=["POST","GET"])
def home():
    if 'username' in session:
        return redirect(url_for('account'))
    if request.method == "POST":
        form = request.form
        worked = False
        if form["submit"] == 'yes' and form['user'] != "" and form["pass"] != "":
            names = db.info.find()
            #NAMES = LIST OF DICTIONARIES
            for person in names:
                if person['user']==form['user']:
                    if person['pass']==form['pass']:
                        worked = True                        
        if worked:
            session['username']=form['user']
            return redirect(url_for('account'))
        else:
            return render_template("home.html",text = "Incorrect password or username")
    return render_template("home.html")



@app.route("/register",methods=["POST","GET"])
def register():
    message = ""
    color = "green"
    if request.method == "POST":
        form = request.form
        if form["submit"] == 'yes' and form['user'] != "" and form["pass"] != "":
            #mongostuff
            if form["pass"] != form["pass2"]:
                message = "Passwords Do Not Match!"
                color = "red"
            elif len(form["pass"]) < 5:
                message = "Passwords Are Too Short!"
                color = "red"
            else:
                if db.info.find_one({'user':form['user']}) == None:
                    db.info.insert({'user':form['user'],'pass':form['pass']})
                    message = "Successfully Registered!"
                else:
                    message = "Username Already Registered!"
                    color = "red"
    return render_template("register.html",m=message, c=color)

@app.route("/account")
def account():
    
    if not ('username' in session):
       return "STOP TRYIN TO CHEAT THE MANGO STORE"
    
    return render_template("account.html",u=session['username'])

@app.route("/logout")
def logout():
    #CLEAR ALL COOKIES
    session.pop("username",None)
    return redirect(url_for("home"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    
    conn = Connection()
    db = conn['ayrz']
    app.debug = True
    app.run()
