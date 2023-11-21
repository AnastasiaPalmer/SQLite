import sqlite3
from prettytable import from_db_cursor

conn = sqlite3.connect('covid.db')
cucu = conn.cursor()

# # look data to feet
# result = cucu.execute('''SELECT count(*) FROM covid WHERE location = "Philippines" AND (date = "30.08.2020" OR date = "2020-08-30") ''').fetchall()
# print(result)
#
# result = cucu.execute('''SELECT count(*) FROM covid WHERE location = "Philippines" AND date = "2020-08-30" ''').fetchall()
# print(result)
# result = cucu.execute('''SELECT count(*) as how FROM covid WHERE location = "Philippines" AND date = "2020-08-30" ''').fetchone()
# r = result
# print('number of records', result[0])
#
# # delit = cucu.execute('delete FROM covid') # commit !!! -_-
# # delit = cucu.execute('drop table covid')


result = cucu.execute('''SELECT max(total_cases), location
                      FROM covid T
                      WHERE T.location != 'World' AND location not like '%income%'
                      GROUP BY location
                      order by total_cases DESC 
                      limit 10
''')
print('\n4. Запишіть в текстовий файл найбільший показник по випадкам по кожній з країн. Н-д: Ukraine:')
print( from_db_cursor(cucu) )
# for row in result:
#     print( row)
