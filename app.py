from flask import Flask, render_template, request, redirect, url_for, abort, session, escape, flash
from pymongo import Connection


app = Flask(__name__)
app.secret_key='{\xdft\xb7\x06f\x9b\xa4\x0eP\xe1n\xdd\xd4\x93\x01\xd3`\xc1\xe5\xc1|\x0e`'

def authenticate(f):
    def inner():
        if username in session:
            return f:
        else:
            return redirect(url_for('register'))
    return inner

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
            #if only we used the flash stuff
            if form["pass"] != form["pass2"]:
                message = "Passwords Do Not Match!"
                color = "red"
            elif len(form["pass"]) < 5:
                message = "Passwords Are Too Short!"
                color = "red"
            else:
                if db.info.find_one({'user':form['user']}) == None:
                    db.info.insert({'user':form['user'],'pass':form['pass'], 'mango':0})
                    message = "Successfully Registered!"
                else:
                    message = "Username Already Registered!"
                    color = "red"
    return render_template("register.html",m=message, c=color)
@authenticate
@app.route("/account", methods=["POST","GET"])
def account():
    number = db.info.find_one({"user":session["username"]})["mango"]
    
    if request.method == "POST":
        form = request.form
        
        if form["grow"] == 'yes':
            db.info.update({'user':session['username']},{'$inc':{'mango': 1}},upsert=False, multi=False)
            number = number + 1
        
    return render_template("account.html",u=session['username'], number = number)
    
@authenticate
@app.route("/leader")
def leader():
    a = db.info.find()
    data = [ (x["user"],x["mango"]) for x in a]
    return render_template("leader.html",data = data, u = session["username"])
    
@authenticate
@app.route("/logout")
def logout():
    #this counts as a page right
    session.pop("username",None)
    return redirect(url_for("home"))

@authenticate
@app.route("/about")
def about():
    text = ""
    text = "You are logged in " + session["username"]
    return render_template("about.html",text=text)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    
    conn = Connection()
    db = conn['ayrz']
    app.debug = True
    app.run(host="0.0.0.0")
