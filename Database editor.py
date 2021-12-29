import sqlite3 as ms
con = ms.connect('Medibot.db')
cursor = con.cursor()
cursor.execute('''UPDATE diseases
                  SET specialty = "Pulmonologist"
                  WHERE specialty = "Pulmonology";''')

con.commit()
