from abc import update_abstractmethods
import json

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from db import DB

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route("/")
def home():
    return "<H1> RobbingHood database </H1>"


@app.route("/departments", methods=["GET"])
def all_departments():
    org_data = []
    with DB() as db:
        db.execute("SELECT * FROM organisation")
        org_data = db.fetch_both()

    return jsonify(org_data)

@app.route("/add-department", methods=["POST"])
def add_department():
    data = json.loads(request.data)
    with DB() as db:
        db.cur.execute(
            "insert into organisation (dept_id, code, description) values (?, ?, ?)",
            (data["dept_id"], data["code"], data["description"])
        )
        db.commit()

    return jsonify({"success": True, "data": data})


@app.route("/department/<string:dept>", methods=["GET", "PUT", "DELETE"])
def department(dept):

    if request.method == "GET":
        dept_data = []
        with DB() as db:
            db.cur.execute(
                "select * from organisation where dept_id = ?",
                (dept, )
            )
            dept_data = db.fetch_both()

        if dept_data:
            return jsonify(dept_data[0])
        return jsonify({"error": f"Department ID: {dept} not found!"}), 404

    elif request.method == "PUT":
        update_data = json.loads(request.data)
        with DB() as db:
            db.cur.execute(
                "update organisation set code = ?, description = ? where dept_id = ?",
                (update_data["code"], update_data["description"], dept)
            )
            db.commit()

        return jsonify({"success": True, "data": update_data})

    else:
        with DB() as db:
            db.cur.execute(
                "delete from organisation where dept_id = ?",
                (dept, )
            )
            db.commit()
        
        return jsonify({"success": True, "Department ID": dept})


@app.route("/employees", methods=["GET"])
def all_employees():
    emp_data = []
    with DB() as db:
        db.execute("SELECT * FROM employee")
        emp_data = db.fetch_both()

    return jsonify(emp_data)

@app.route("/add-employee", methods=["POST"])
def add_employee():
    data = json.loads(request.data)
    with DB() as db:
        db.cur.execute(
            "insert into employee (login_id, dept_id, name, onboarded) values (?, ?, ?, ?)",
            (data["login_id"], data["dept_id"], data["name"], data["onboarded"])
        )
        db.commit()

    return jsonify({"success": True, "data": data})

@app.route("/employee/<string:login>", methods=["GET", "DELETE"])
def employee(login):
    if request.method == "GET":
        emp_data = []
        with DB() as db:
            db.cur.execute(
                "select * from employee where login_id = ?",
                (login, )
            )
            emp_data = db.fetch_both()
        
        if emp_data:
            return jsonify(emp_data[0])
        return jsonify({"error": f"Employee: {login} not found"}), 404

    else:
        with DB() as db:
            db.cur.execute(
                "delete from employee where login = ?",
                (login, )
            )
            db.commit()

        return jsonify({"success": True, "login ID": login})


if __name__ == "__main__":
    dir(app.run)
    app.run(host='0.0.0.0', port=8889)