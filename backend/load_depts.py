from db import DB
import csv

dept_file = 'organisation.csv'

with DB() as db:

    with open(dept_file, 'r', encoding='utf-8-sig') as f:

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
