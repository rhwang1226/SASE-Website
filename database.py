import sqlite3

con = sqlite3.connect('database.db')
print("Connected to database successfully")

con.execute('DROP TABLE IF EXISTS eboard')

con.execute('CREATE TABLE eboard (name TEXT NOT NULL CHECK(name <> ""), position TEXT NOT NULL, greeting TEXT NOT NULL CHECK(greeting <> ""))')
con.execute('CREATE TABLE login (username TEXT NOT NULL CHECK(name <> ""), password TEXT NOT NULL')
print("Created table successfully!")

cur = con.cursor()
cur.execute("INSERT INTO eboard (name, position, greeting) VALUES ('Hannah Kim', 'President', 'Hannah Kim is a Junior majoring in Microbiology! With a passion for exploring the intricacies of the microscopic world, Hannah is a dedicated student on her academic journey. When she''s not immersed in her scientific studies, you can find her indulging in her favorite KDramas, currently relishing the joys of rewatching Hospital Playlist Season 2. Additionally, Hannah finds solace in the captivating world of books, spending her free time engrossed in the pages of various literary adventures. As a leisure activity, she also enjoys hitting the golf course, honing her skills and enjoying the outdoors. Now, here''s an interesting tidbit about Hannah: despite her time on campus, she has never set foot on North Campus and has yet to experience the thrill of riding a Blue Bus.')")

con.commit()

con.close()