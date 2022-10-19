from db import DB
import csv

csv_file = "employees.csv"

def insert_into_database():

   with DB() as db:

      with open(csv_file, 'r', encoding='utf-8-sig') as f:

         reader = csv.DictReader(f)
         for row in reader:
            print(f"Inserting row: {row}")
            query = f"""
            INSERT INTO EMPLOYEE (login_id, dept_id, name, onboarded)
            VALUES
            ('{row['login']}', '{row['dept']}', '{row['name']}, '{row['onboarded']}')
            """
            print("Query: ", query)
            db.execute(query)

         db.commit()

insert_into_database()
