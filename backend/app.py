import json

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from db import DB
import quota
from ipa_single_user import *


app = Flask(__name__)
app.debug = True
cors = CORS(app)

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
        db.execute("SELECT login_id, dept_id, name, DATE_FORMAT(onboarded, '%Y-%m-%d') AS onboarded FROM employee")
        emp_data = db.fetch_both()

    return jsonify(emp_data)

@app.route("/employees/<string:date>", methods=["GET"])
def all_employees_date(date):
    emp_data = []
    with DB() as db:
        db.execute(
            f"SELECT login_id, dept_id, name, DATE_FORMAT(onboarded, '%Y-%m-%d') AS onboarded FROM employee where onboarded = {date}"
            )
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
        # create_usr_home using ipa server: TODO create reusable function
        db.commit()
    ipa_add_user(data["login_id"], data["name"], data["dept_id"], data["onboarded"])

    return jsonify({"success": True, "data": data})

@app.route("/employee/<string:login>", methods=["GET", "PUT", "DELETE"])
def employee(login):
    if request.method == "GET":
        emp_data = []
        with DB() as db:
            db.cur.execute(
                "select login_id, dept_id, name, DATE_FORMAT(onboarded, '%Y-%m-%d') AS onboarded from employee where login_id = ?",
                (login, )
            )
            emp_data = db.fetch_both()
        
        if emp_data:
            return jsonify(emp_data[0])
        return jsonify({"error": f"Employee: {login} not found"}), 404

    elif request.method == "PUT":
        update_data = json.loads(request.data)
        with DB() as db:
            db.cur.execute(
                "update employee set name = ?, dept_id = ? where login_id = ?",
                (update_data["name"], update_data["dept_id"], login)
            )
            # update user_home_comment? using ipa server: TODO create reusable function
            # when user changes their name OR change department
            db.commit()

        return jsonify({"success": True, "data": update_data})

    else:
        with DB() as db:
            db.cur.execute(
                "delete from employee where login_id = ?",
                (login, )
            )
            # delete_usr_home using ipa server: TODO create reusable function
            db.commit()
        ipa_del_user(login)
        return jsonify({"success": True, "login ID": login})

@app.route("/quotas", methods=["GET"])
def all_quota():
    return jsonify(quota.get_storage_of_all())

@app.route("/quota/<string:login>", methods=["GET", "PUT"])
def employee_quota(login):
    storage_data = quota.get_storage_of_user(login)
    if storage_data == 'Not a valid user':
        return jsonify({"error": f"Employee: {login} not found"}), 404
    if request.method == "GET":
        return jsonify(storage_data)

    elif request.method == "PUT":
        update_data = json.loads(request.data)
        quota.set_quota_for_user(login, int(update_data["limit"]), int(update_data["limit"]) + 20)
        return jsonify({"success": True, "data": update_data})

@app.route("/quotas/<string:department>", methods=["GET"])
def department_quotas(department):
    emp_data = []
    with DB() as db:
        db.cur.execute(
            "select * from employee where dept_id = ?",
            (department, )
        )
        emp_data = db.fetch_both()

    if emp_data:
        quota_data = {}
        for employee in emp_data:
            quota_data[employee['login_id']] = quota.get_storage_of_user(employee['login_id'])
        return jsonify(quota_data)
    return jsonify({"error": f"Department: {department} not found"}), 404


if __name__ == "__main__":
    dir(app.run)
    app.run(host='0.0.0.0', port=8889)
