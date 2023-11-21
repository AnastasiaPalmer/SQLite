"""
4. Виконайте наступні завдання, використовуючи мову SQL та засоби Python:
- Знайдіть назву всіх фільмів
- Знайдіть директора та рік кожного фільму
- Знайдіть інформацію по кожному з фільмів

- Знайдіть фільми Id яких дорівнює 6
- Знайдіть фільми, що вийшли з 2000 по 2010 рік
- Знайдіть фільми, які були випущені у 2006, 2088, 2010 роках.

- Знайдіть фільми та їх директорів, випущені до 2010 року (з використанням NOT)
- Знайдіть всі фільми Toy Story
- Знайдіть 2.txt фільми Toy Story іншим способом

- Знайдіть всі фільми, що були зняті Джоном Лассатером
- Знайдіть всі фільми, що НЕ були зняті Джоном Лассетером
- Знайдіть всі фільми WALL-*

- Виведіть перелік режисерів(без дублювання) в алфавітному порядку
- Перелік з 4 фільмів новійших фільмів
- Перелік з 5 фільмів, відсортованих за алфавітом

- Перелік з наступних 5 фільмів, відсортованих за алфавітом
- Для таблиць Movies та Boxoffice, об’єднаних через INNER JOIN:
- Знайдіть внутрішні та міжнародні продажі для кожного фільму
- Покажіть всі фільми з їх рейтингами у спадному порядку
- Далі поєднуйте таблиці так, як Вам буде зручно:
- Виведіть перелік будівель та людей, які живуть у цих будівлях, з їх професіями
- Виведіть перелік людей та їх спеціальностей, які не прикріплені до будинків
- Виведіть всі назви фільмів та їх загальні збори в доларовому еквіваленті
"""

import sqlite3
from prettytable import from_db_cursor

conn = sqlite3.connect('movies.db')
curr = conn.cursor()

curr.execute('''SELECT Title FROM Movies''')

curr.execute('''SELECT Title, Director, Year FROM Movies''')

curr.execute('''SELECT * FROM Movies
                LEFT JOIN Boxoffice on Movies.Id = Boxoffice.Movie_id''')

curr.execute('''SELECT * FROM Movies WHERE Id = "6"''')

curr.execute('''SELECT * FROM Movies WHERE Year >= 2000 AND Year <= 2010 ORDER BY Year DESC ''')

curr.execute('''SELECT * FROM Movies WHERE Year = 2006 OR Year = 2088 OR Year = 2010 ORDER BY Year''')

curr.execute('''SELECT Title, Director, Year FROM Movies WHERE NOT Year >= 2010 ORDER BY Year''')

curr.execute('''SELECT * FROM Movies WHERE Title LIKE "Toy Story%" ''')

curr.execute('''SELECT * FROM Movies WHERE Director LIKE "John Lasseter" ''')

curr.execute('''SELECT * FROM Movies WHERE Director NOT LIKE "John Lasseter" ''')

curr.execute('''SELECT * FROM Movies WHERE Title LIKE "WALL%"''')

curr.execute('''SELECT DISTINCT Director FROM Movies ORDER BY Director''')

curr.execute('''SELECT * FROM Movies ORDER BY Year DESC LIMIT 4''')

curr.execute('''SELECT * FROM Movies ORDER BY Title LIMIT 5''')

curr.execute('''SELECT * FROM Movies ORDER BY Title LIMIT 5 OFFSET 5''')

curr.execute('''SELECT * FROM Movies
                INNER JOIN Boxoffice on Movies.Id = Boxoffice.Movie_id''')

curr.execute('''SELECT m.id, m.Title, b.Domestic_sales, b.International_sales
                FROM Boxoffice b
                INNER JOIN Movies m on b.Movie_id = m.Id
                ORDER BY 1''')

curr.execute('''SELECT m.id, m.Title, b.Rating
                FROM Boxoffice b
                INNER JOIN Movies m on b.Movie_id = m.Id
                ORDER BY Rating DESC ''')

curr.execute('''SELECT *
                FROM Buildings b
                JOIN Employees e on e.Building = b.Building_names''')

curr.execute('''SELECT * FROM Employees WHERE Building= "" ''')

curr.execute('''SELECT m.Id ,m.Title, printf("%14.2f$",b.International_sales + b.Domestic_sales) as zbir
                FROM Movies m
                LEFT JOIN Boxoffice B on m.Id = B.Movie_id
                ORDER BY zbir DESC 
                ''')

"""
- Виведіть всі назви фільмів та їх загальні збори в доларовому еквіваленті
"""
print(from_db_cursor(curr))
