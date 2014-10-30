from flask import Flask, render_template, request
from pymongo import Connection


app = Flask(__name__)



@app.route("/", methods=["POST","GET"])
def home():
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
            print "YOU CAN LOG IN"
        else:
            print "YOU CAN'T LOG IN"
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
                db.info.insert({'user':form['user'],'pass':form['pass']})
                message = "Successfully Registered!"
    return render_template("register.html",m=message, c=color)




if __name__ == "__main__":
    conn = Connection()
    db = conn['ayrz']
    app.debug = True
    app.run()
