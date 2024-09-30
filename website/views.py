from flask import Flask , Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
views = Blueprint('views', __name__)

@views.route("/", methods= ["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('note')
        if len(note) < 1:
            flash("note is too short", category="alert-danger")
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added succesfully", category="alert-success")    
    return render_template("home.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
@login_required
def deleteNote():
    note_data = request.get_json()
    note_id = note_data.get('noteId')

    if note_id:
        note = Note.query.get(note_id)
        if note:
            db.session.delete(note)
            db.session.commit()
            return jsonify({}),200
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"error": "Invalid request"}), 404