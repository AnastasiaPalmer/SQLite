# import os
import pandas as pd
import sqlite3
from prettytable import from_db_cursor

"""
1. Напишіть клас, який буде працювати з БД і буде мати метод, який у якості аргументів буде
приймати адресу файлу та БД. 
Метод повинен зчитувати всі дані з файлу та зберігати їх у
відповідній таблиці у БД. Причому, він повинен працювати як з txt, так і з csv файлами
(використайте функцію split() для визначення типу файла) і зберігати його у таблиці з такою
ж назвою. Перед збереженням, метод повинен перевіряти, чи є така таблиця, якщо ні –
створити її (назви і типи даних для створення таблиці витягувати не потрібно – просто
впишіть їх у запит).
"""

# load the data
data = pd.read_csv('covid.csv')

# create connection and cursor
conn = sqlite3.connect('covid.db')
c = conn.cursor()

# create table
create_table = f'''CREATE TABLE IF NOT EXISTS covid ({','.join(data.columns)})'''
c.execute(create_table)

result = c.execute('''SELECT count(*) as how FROM covid''').fetchone()
print('number of records in table Covid is ', result[0])

# fill table
if result[0] < 1:
    # insert data
    insert_query = f'''INSERT INTO covid VALUES ({','.join(['?'] * len(data.columns))})'''
    c.executemany(insert_query, data.values)
    conn.commit()

"""
2.txt. Використайте цю функцію і збережіть дані з попередньої лабораторної у БД.
"""

print("Дані з файлу 'covid.csv' були збережені у таблицю 'covid'")

"""
3. Виконайте завдання 8 з лабораторної роботи про роботу з файлами, але вже використовуючи мову
SQL. Звертаю увагу, що запит повинен повертати лише саму відповідь. Не потрібно
вивантажувати всю базу і потім її перебирати у Python. Також, додайте якесь оформлення,
щоб було зрозуміло, що за числа були виведені.

1. Яка загальна кількість хворих зафіксовано на Філіппінах на 30.08.2020?
2. Коли був зафіксований найбільший приріст хворих за тиждень в Україні?
3. Порахуйте, чи відповідають дані по загальній кількості випадків за 21.08.2020 по світу 
сумі випадків по країнах за цю дату?
4. Запишіть в текстовий файл найбільший показник по випадкам по кожній з країн. Н-д: Ukraine =)
"""

result = c.execute('''SELECT sum(total_cases) FROM covid WHERE location = "Philippines" AND date = "2020-08-30" ''').fetchone()
print('\n1. Загальна кількість хворих зафіксовано на Філіппінах на 30.08.2020: ', result[0])


result = c.execute('''SELECT strftime('%W', date) AS Week, SUM(total_cases) AS TotalCases           --- DATEPART for SQL
                      FROM covid
                      WHERE date BETWEEN '2020-01-01' AND '2023-02-26'
                      GROUP BY strftime('%W', date)
                      HAVING SUM(total_cases) = (SELECT MAX(CasesPerWeek)
                        FROM (SELECT strftime('%W', date) AS Week, SUM(total_cases) AS CasesPerWeek
                              FROM covid
                              WHERE date BETWEEN '2020-01-01' AND '2023-02-26'
                              GROUP BY strftime('%W', date)) AS WeeklyCases)
                                                                                             ''').fetchall()
print('\n2. Коли був зафіксований найбільший приріст хворих за тиждень в Україні: ', result[0])

result = c.execute('''SELECT SUM(total_cases) AS summ, 'LocCases'
                      FROM covid 
                      WHERE date = '2020-08-21' AND location <> 'World'
                      union
                         SELECT SUM(total_cases) AS summ, 'WorldCases'
                         FROM covid 
                         WHERE date = '2020-08-21' AND location = 'World'
                                                                                                                ''').fetchall()
print('\n3. дані по загальній кількості випадків за 21.08.2020 по світу сумі випадків по країнах за цю дату: ', result)

result = c.execute('''SELECT max(total_cases), location
                      FROM covid T
                      WHERE T.location != 'World' AND location not like '%income%'
                      GROUP BY location
                      order by total_cases DESC 
                      limit 10
''')
text = from_db_cursor(c)
# print('\n4. Запишіть найбільший показник по випадкам по кожній з країн.\n', text)  # from_db_cursor(c))

# f = open("output3.2.txt", "w")
# f.write(text.get_string())
# f.close()

with open("output3.2.txt", "w") as fd:
    fd.write(text.get_string())


# class DBHandler:
#     def __init__(self, db_file):
#         self.db_file = db_file
#         self.conn = sqlite3.connect(db_file)
#         self.cursor = self.conn.cursor()
#
#     def insert_data_from_file(self, file_path, table_name):
#         # Визначаємо тип файлу (csv або txt)
#         file_type = file_path.split(".")[-1]
#         if file_type == "csv":
#             delimiter = ","
#         else:
#             delimiter = "\t"
#
#         # Відкриваємо файл і зчитуємо дані
#         with open(file_path, "r") as f:
#             reader = csv.reader(f, delimiter=delimiter)
#             data = [row for row in reader]
#
#         # Створюємо таблицю, якщо вона ще не існує
#         create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join([data[0][i] for i in range(len(data[0]))])})"
#         self.cursor.execute(create_table_query)
#
#         # Вставляємо дані в таблицю
#         insert_query = f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(data[0]))})"
#         self.cursor.executemany(insert_query, data)
#         self.conn.commit()
#
#         print(f"Дані з файлу {file_path} були збережені у таблицю {table_name}")


# class DBHandler:
#     def __init__(self, file_name, db_name):
#         self.file_name = file_name
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#
#         self.split = self.file_name.split('.')
#         if self.split == "csv":
#             self.csv_to_sql()
#         elif self.split == "txt":
#             self.txt_to_sql()
#
#     def csv_to_sql(self, file_name, db_name, table_name):
#         bd = pd.read_csv(file_name)
#         conn = sqlite3.connect(db_name)
#         bd.to_sql(table_name, conn, if_exists="replace", index=False)
#         conn.close()
#
#     def txt_to_sql(self, txt_file, db_file, table_name):
#         df = pd.read_csv(txt_file, sep='\t')
#         conn = sqlite3.connect(db_file)
#         df.to_sql(table_name, conn, if_exists='replace', index=False)
#         conn.close()


# import csv
# import sqlite3
#
#
# class DBHandler:
#     def __init__(self, db_file):
#         self.db_file = db_file
#         self.conn = sqlite3.connect(db_file)
#         self.cursor = self.conn.cursor()
#
#     def insert_data_from_file(self, file_path, table_name):
#         # Визначаємо тип файлу (csv або txt)
#         file_type = file_path.split(".")[-1]
#         if file_type == "csv":
#             delimiter = ","
#         else:
#             delimiter = "\t"
#
#         # Відкриваємо файл і зчитуємо дані
#         with open(file_path, "r") as f:
#             reader = csv.reader(f, delimiter=delimiter)
#             data = [row for row in reader]
#
#         # Створюємо таблицю, якщо вона ще не існує
#         create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join([data[0][i] for i in range(len(data[0]))])})"
#         self.cursor.execute(create_table_query)
#
#         # Вставляємо дані в таблицю
#         insert_query = f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(data[0]))})"
#         self.cursor.executemany(insert_query, data)
#         self.conn.commit()
#
#         print(f"Дані з файлу {file_path} були збережені у таблицю {table_name}")

# converter = DBHandler('path_to_db')
# converter.insert_data_from_file('C:\\Users\\nasti\Documents\University\АтП\3\3.1')
# converter.insert_data_from_file('C:/Users/nasti/Documents/University/АтП/3/3.1', 'biaka')
# converter.insert_data_from_file('./2.txt', 'biaka')

# converter.insert_data_from_file('./covid.csv', 'covid')
