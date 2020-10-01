import sqlite3
connection = sqlite3.connect('petTest.s3db')

cursor = connection.cursor()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS pet (
        name TEXT,
        owner TEXT,
        legs INTEGER DEFAULT 4);
    '''
)
cursor.execute("INSERT INTO pet VALUES ('Kitty', 'John', 4)")
cursor.execute("INSERT INTO pet VALUES ('Bello', 'Alex', 4)")
cursor.execute("SELECT * FROM pet")
result = cursor.fetchall()
print(result)
connection.commit()
connection.close()
