from db import DB
import csv

dept_file = 'organisation.csv'

def load_departments():

    with DB() as db:

      with open(dept_file, 'r') as f:

         reader = csv.DictReader(f)
         for row in reader:
            print(f"Inserting row: {row}")
            query = f"""
            INSERT INTO organisation (dept_id, code, description)
            VALUES ('{row['dept']}', '{row['code']}', '{row['description']}')
            """
            print("Query: ", query)
            db.execute(query)

         db.commit()
