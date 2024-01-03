from random import choice
from neomodel import config
from .init import init as init_db
import os
from .entities import Person
from flask import Flask, render_template, request, redirect

config.DATABASE_URL = f"bolt://{os.getenv('NEO4J_USERNAME')}:{os.getenv(f'NEO4J_PASSWORD')}@db:7687"
LOGGED_USER = "Pepa"

app = Flask(__name__)
@app.route("/")
@app.route("/home")
def hello_world():
    logged_user_node: Person = Person.nodes.get(name=LOGGED_USER)
    num_of_matches = len(logged_user_node.matches())
    num_of_available_matches = len(logged_user_node.available_matches()) 
    return render_template("home.html", profile=logged_user_node, num_of_matches=num_of_matches, num_of_available_matches=num_of_available_matches)

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "GET":
        person: Person = Person.nodes.get(name=LOGGED_USER)
        potential_matches = person.available_matches()
        if potential_matches:
            random_profile = choice(potential_matches)
        else:
            random_profile = None
        return render_template("search.html", profile=random_profile)
    else:
        date_choice = request.form.get("date_choice")
        friend_name = request.form.get("friend_name")
        user_node:Person = Person.nodes.get(name=LOGGED_USER)
        friend_node:Person = Person.nodes.get(name=friend_name)
        if date_choice == "like":
            user_node.like(friend_node)
        elif date_choice == "dislike":
            user_node.dislike(friend_node)
        return redirect("/search")

@app.route("/matches")
def matches():
    person: Person = Person.nodes.get(name=LOGGED_USER)
    matches = person.matches()
    return render_template("matches.html", profiles=matches)

if not Person.nodes.get_or_none(name="Pepa"):
    init_db()
app.run(debug=True, host="0.0.0.0")
...
    
