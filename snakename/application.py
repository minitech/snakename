import os

from flask import Flask, redirect, render_template, request, session, url_for
from sqlalchemy import exc, create_engine, desc, func, select

from .schema import metadata, suggestions, votes

app = Flask("snakename")
app.secret_key = os.urandom(32)

engine = create_engine("sqlite:///snakename.db")
metadata.create_all(engine)


@app.route("/")
def main():
    if "votes" not in session:
        session["votes"] = {}

    query = engine.execute(
        select([suggestions.c.id, suggestions.c.name, func.count(votes.c.suggestion).label("vote_count")])
        .select_from(suggestions.outerjoin(votes))
        .group_by(suggestions.c.id)
        .order_by(desc("vote_count"), suggestions.c.name))

    return render_template("index.html", suggestions=query)


@app.route("/suggest", methods=["POST"])
def suggest():
    query = (
        suggestions.insert()
        .values(name=request.form["name"]))

    try:
        engine.execute(query)
    except exc.IntegrityError:
        pass

    return redirect(url_for("main"))


@app.route("/vote", methods=["POST"])
def vote():
    suggestion = int(request.form["vote"])
    ip = request.environ["REMOTE_ADDR"]
    user_votes = session["votes"]

    if str(suggestion) in user_votes:
        if user_votes[str(suggestion)] == 3:
            return redirect(url_for("main"))

        user_votes[str(suggestion)] += 1
    else:
        user_votes[str(suggestion)] = 1

    session.modified = True

    engine.execute(
        votes.insert()
        .values(suggestion=suggestion, ip=ip))

    return redirect(url_for("main"))
