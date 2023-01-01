from flask import Flask, request
import list_dbs
import create_db
import delete_db

app = Flask(__name__)

USERNAME = "airportyh"

@app.route("/databases", methods=["GET"])
def api_list_dbs():
    return list_dbs.list_dbs(USERNAME)
    
@app.route("/databases", methods=["POST"])
def api_create_db():
    db_name = request.form['name']
    create_db.create_db(db_name, USERNAME)
    return { "ok": True }

@app.route("/databases/<db_name>", methods=["DELETE"])
def api_delete_db(db_name):
    delete_db.delete_db(db_name, USERNAME)
    return { "ok": True }
    
    