from flask import Flask, render_template, request
import pymongo
app = Flask(__name__)

def makeDB():
    conn = Connection()
    db = conn['ayrz']

def testDB():
    db.test.insert({'hi':'hi'})


    
@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        form = request.form
    if form["submit"] == 'yes' and form['user'] != "" and form["pass"] != "":
        names = db.info.find()
        if names.has_key(form['user']):
            if names[form['user']]==form['pass']:
                print "<h1>USERNAME + PASSWORD CORRECT</h1>"
                #USERNAME + PASSWORD CORRECT
            else:
                print "<h1>USERNAME + PASSWORD WRONG</h1>"
                #USERNAME + PASSWORD WRONG
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
                message = "Successfully Registered!"
    return render_template("register.html",m=message, c=color)

if __name__ == "__main__":
    #makeDB()
    #testDB()
    app.debug = True
    app.run()
