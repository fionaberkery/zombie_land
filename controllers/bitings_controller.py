from flask import Blueprint, Flask, redirect, render_template, request
import repositories.human_repository as human_repo
import repositories.zombie_repository as zombie_repo
import repositories.biting_repository as biting_repo
from models.biting import Biting

bitings_blueprint = Blueprint("bitings", __name__)
import repositories.biting_repository as biting_repository

# INDEX
@bitings_blueprint.route("/bitings")
def bites():
    bitings = biting_repository.select_all()
    return render_template("bitings/index.html", bitings=bitings)

# NEW
@bitings_blueprint.route("/bitings/new")
def new_bite():
    humans = human_repo.select_all()
    zombies = zombie_repo.select_all()
    return render_template("bitings/new.html", humans=humans, zombies=zombies)

# CREATE
@bitings_blueprint.route("/bitings", methods=["POST"])
def create_bite():
    human = request.form["human_id"]
    zombie = request.form["zombie_id"]
    
    humans = human_repo.select(human)
    zombies = zombie_repo.select(zombie)
    bite = Biting(humans, zombies)
    biting_repository.save(bite)
    return redirect("/bitings")

# EDIT
@bitings_blueprint.route("/bitings/<id>/edit")
def edit_bite(id):
    humans = human_repo.select_all()
    zombies = zombie_repo.select_all()
    biting = biting_repo.select(id)
    return render_template('bitings/edit.html', humans=humans, zombies=zombies, biting=biting)

# UPDATE
@bitings_blueprint.route("/bitings/<id>", methods=["POST"])
def update_bite(id):
    human = request.form["human_id"]
    zombie = request.form["zombie_id"]

    humans = human_repo.select(human)
    zombies = zombie_repo.select(zombie)
    bite = Biting(humans, zombies, id)
    biting_repository.update(bite)
    return redirect("/bitings")

# DELETE
@bitings_blueprint.route("/bitings/<id>/delete", methods=["POST"])
def delete_bite(id):
    biting_repo.delete(id)
    return redirect("/bitings")
