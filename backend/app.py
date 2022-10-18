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


@app.route("/organisations", methods=["GET"])
def all_organisations():
    org_data = []
    with DB() as db:
        db.execute("SELECT * FROM organisation")
        org_data = db.fetch_both()

    return jsonify(org_data)


@app.route("/employees", methods=["GET"])
def all_employees():
    emp_data = []
    with DB() as db:
        db.execute("SELECT * FROM employee")
        emp_data = db.fetch_both()

    return jsonify(emp_data)

if __name__ == "__main__":
    dir(app.run)
    app.run(host='94.237.60.14', port=8889)