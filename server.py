from flask import Flask, request, send_from_directory

import list_dbs
import create_db
import delete_db
import list_tables
import create_table
import list_columns
import create_column
import delete_column
import list_rows
import create_row
import delete_row
import update_row
import json

app = Flask(__name__)

USERNAME = "airportyh"

@app.route("/", methods=["GET"])
def home():
    return send_from_directory('static', 'index.html')

@app.route("/databases", methods=["GET"])
def api_list_dbs():
    return list_dbs.list_dbs(USERNAME)
    
@app.route("/databases/<db_name>", methods=["PUT"])
def api_create_db(db_name):
    create_db.create_db(db_name, USERNAME)
    return { "ok": True }

@app.route("/databases/<db_name>", methods=["DELETE"])
def api_delete_db(db_name):
    delete_db.delete_db(db_name, USERNAME)
    return { "ok": True }
    
@app.route("/databases/<db_name>/tables", methods=["GET"])
def api_list_tables(db_name):
    return list_tables.list_tables(db_name, USERNAME)

@app.route("/databases/<db_name>/tables/<table_name>", methods=["PUT"])
def api_create_table(db_name, table_name):
    create_table.create_table(db_name, table_name, USERNAME)
    return { "ok": True }

@app.route("/databases/<db_name>/tables/<table_name>/columns", methods=["GET"])
def api_list_columns(db_name, table_name):
    return list_columns.list_columns(db_name, table_name, USERNAME)

@app.route("/databases/<db_name>/tables/<table_name>/columns/<column_name>", methods=["PUT"])
def api_create_column(db_name, table_name, column_name):
    data = json.loads(request.data)
    column_type = data['type']
    create_column.create_column(db_name, table_name, column_name, column_type, USERNAME)
    return { "ok": True }

@app.route("/databases/<db_name>/tables/<table_name>/columns/<column_name>", methods=["DELETE"])
def api_delete_column(db_name, table_name, column_name):
    delete_column.delete_column(db_name, table_name, column_name, USERNAME)
    return { "ok": True }

@app.route("/databases/<db_name>/tables/<table_name>/rows", methods=["GET"])
def api_list_rows(db_name, table_name):
    return list_rows.list_rows(db_name, table_name, USERNAME)

@app.route("/databases/<db_name>/tables/<table_name>/rows", methods=["POST"])
def api_create_row(db_name, table_name):
    data = json.loads(request.data)
    columns = data['columns']
    values = data['values']
    id = create_row.create_row(db_name, table_name, columns, values, USERNAME)
    return { "id": id }

@app.route("/databases/<db_name>/tables/<table_name>/rows/<id>", methods=["DELETE"])
def api_delete_row(db_name, table_name, id):
    result = delete_row.delete_row(db_name, table_name, id, USERNAME)
    return { "deleted": result }
    
@app.route("/databases/<db_name>/tables/<table_name>/rows/<id>", methods=["PUT"])
def api_update_row(db_name, table_name, id):
    data = json.loads(request.data)
    columns = data['columns']
    values = data['values']
    updated = update_row.update_row(db_name, table_name, id, columns, values, USERNAME)
    return { "updated": updated }
    
    