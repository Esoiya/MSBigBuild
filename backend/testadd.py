import db
import csv

csv_file = "employees.csv"

def insert_into_database():
   csv_rows = []
   with open(csv_file, newline='', encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
         csv_rows.append(row)
   line_number = 0
   all_lines = []
   line = ''
   for row in csv_rows:
      line += f'''( '{row['name']}', '{row['login']}', '{row['onboarded']}', '{row['dept']}'), '''
      line_number += 1
      if line_number == 500:
         all_lines.append(line[:-2] + ';')
         line_number = 0
         line = ''

   with db.DB() as cursor:
      for line in all_lines:
         cursor.execute(f'''INSERT INTO EMPLOYEE(name, login_id, onboarded, dept_id) VALUES {line}''')

      conn.commit()

insert_into_database()
