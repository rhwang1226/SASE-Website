import sqlite3
import bcrypt

con = sqlite3.connect('database.db')
print("Connected to database successfully")

con.execute('DROP TABLE IF EXISTS eboard')
con.execute('DROP TABLE IF EXISTS login')

con.execute('CREATE TABLE eboard (name TEXT NOT NULL, position TEXT NOT NULL, greeting TEXT NOT NULL, picture TEXT NOT NULL)')
con.execute('CREATE TABLE login (username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, salt TEXT NOT NULL)')
print("Created table successfully!")

unhashed = "sasegoblue"
salt = bcrypt.gensalt()
password = bcrypt.hashpw(unhashed.encode('utf-8'), salt)
print("Hashed String:", password.decode('utf-8'))

cur = con.cursor()
#cur.execute("INSERT INTO eboard (name, position, greeting, picture) VALUES ('Hannah Kim', 'President', 'Hannah Kim is a Junior majoring in Microbiology! With a passion for exploring the intricacies of the microscopic world, Hannah is a dedicated student on her academic journey. When she''s not immersed in her scientific studies, you can find her indulging in her favorite KDramas, currently relishing the joys of rewatching Hospital Playlist Season 2. Additionally, Hannah finds solace in the captivating world of books, spending her free time engrossed in the pages of various literary adventures. As a leisure activity, she also enjoys hitting the golf course, honing her skills and enjoying the outdoors. Now, here''s an interesting tidbit about Hannah: despite her time on campus, she has never set foot on North Campus and has yet to experience the thrill of riding a Blue Bus.', 'hannah.PNG')")
cur.execute("INSERT INTO login (username, password, salt) VALUES ('admin', '" + str(password.decode()) + "', '" + str(salt.decode()) + "')")

con.commit()

con.close()