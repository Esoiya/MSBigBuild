from db import DB
import csv

from datetime import datetime

csv_file = "employees.csv"

def format_date(date):

   dt = datetime.strptime(date, "%d/%m/%Y")
   
   return dt.date().isoformat()


def load_employees(csv_file=csv_file):

   with DB() as db:

      with open(csv_file, 'r', encoding='utf-8-sig') as f:

         reader = csv.DictReader(f)
         for row in reader:
            print(f"Inserting row: {row}")
            onboarded_date = format_date(row["onboarded"])

            query = f"""
            INSERT INTO employee (login_id, dept_id, name, onboarded)
            VALUES ('{row['login']}', '{row['dept']}', '{row['name']}', '{onboarded_date}')
            """
            print("Query: ", query)
            #db.execute(query)

         # db.commit()


load_employees()