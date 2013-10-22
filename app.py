from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("username"):
        return "User %s is logged in!"%session['username']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)
    if username != None:
        #flash("User Authenticated!")
        session['username'] = user_id
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect("/user/%s"%username)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for("index"))


@app.route("/user/<username>")
def view_user(username):
    print username
    ownerId = model.get_user_by_name(username)
    #get wall posts from id and send to wall.html
    rows = model.getPosts(ownerId)
    posts = []
    for row in rows:
        posts.append(row)
    return render_template("wall.html", posts=posts, username=username)

@app.route("/user/<username>")
def post_on_wall():
    text = request.form.get("newPost")
    username = request.form.get("username")
    user_id = session.get("username")
    
    ownerId = model.get_user_by_name(username)
    model.make_post(ownerId, user_id, text)
    return redirect("/user/%s"%username)

if __name__ == "__main__":
    app.run(debug = True)
