from flask import Flask, render_template, request
import pymongo
app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def home():
    """
    if request.method == "POST":
        form = request.form
        if form["submit"] == 'yes' and form['user'] != "" and form["pass"] != "":
            #mongostuff
    """
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
    app.debug = True
    app.run()
