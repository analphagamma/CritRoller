import sqlite3
from random import randint



class DBHandler(object):

    def __init__(self, database_path):
        self.database_path = database_path

        self.w_types = {'magic': 1,
                   'bludgeoning': 2,
                   'piercing': 3,
                   'slashing': 4}
                   
        self.conn = sqlite3.connect(database_path)
        self.c = self.conn.cursor()

    def initialize_db(self):

        self.c.execute('''CREATE TABLE IF NOT EXISTS `Crits` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`author`	TEXT,
	`name`	TEXT,
	`text`	TEXT NOT NULL,
    'type_id' INTEGER,
	`used`	INTEGER NOT NULL
) ''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS `Fumbles` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`author`	TEXT,
	`name`	TEXT,
	`text`	TEXT NOT NULL,
    'type_id' INTEGER,
	`used`	INTEGER NOT NULL
)''')

        self.c.execute('''CREATE TABLE `Types` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`type`	TEXT NOT NULL UNIQUE
)''')
        for item in ['magic', 'bludgeoning', 'piercing', 'slashing']:
            self.c.execute('INSERT INTO Types(type) values ( ? )', (item, ) )

        self.conn.commit()

    def add_entry(self, table, author, name, text, weapon_type):

        if not self.w_types.get(weapon_type):
            return None
        else:
            weapon_type = self.w_types.get(weapon_type)
            
        print('Author: {}\nName: {}\n Weapon type: {}\nText: {}'.format(author, name, weapon_type, text))
        if table == 'Crit':
            self.c.execute('INSERT INTO Crits(author, name, text, type_id,  used) VALUES( ?, ?, ?, ?, 0 )', (author, name, text, weapon_type))
        elif table == 'Fumble':
            self.c.execute('INSERT INTO Fumbles(author, name, text, type_id, used) VALUES( ?, ?, ?, ?, 0 )', (author, name, text, weapon_type))
        else:
            return
            
        self.conn.commit()

    def reset_used(self, table):
        if table == 'Crits':
            self.c.execute('UPDATE Crits SET used = 0')
        elif table == 'Fumbles':
            self.c.execute('UPDATE Fumbles SET used = 0')
        else:
            return

        self.conn.commit()

    def select_random(self, from_table, used, weapon_type):

        if not self.w_types.get(weapon_type):
            return None
        else:
            weapon_type = self.w_types.get(weapon_type)
        
        if from_table == 'Crit':
            self.c.execute('SELECT * FROM Crits WHERE (used IN (0, ( ? )) AND type_id=( ? ) ) ORDER BY RANDOM() LIMIT 1', (used, weapon_type))
        elif from_table == 'Fumble':
            self.c.execute('SELECT * FROM Fumbles WHERE (used IN (0, ( ? )) AND type_id=( ? ) ) ORDER BY RANDOM() LIMIT 1', (used, weapon_type))
        else:
            return

        return self.c.fetchone()

    def set_used(self, name, table):
        if table == 'Crit':
            self.c.execute('Update Crits SET used = 1 WHERE name = ( ? )', (name, ))
        elif table == 'Fumble':
            self.c.execute('Update Fumbles SET used = 1 WHERE name = ( ? )', (name, ))

        self.conn.commit()
