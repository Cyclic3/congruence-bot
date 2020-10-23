import sqlite3
from typing import NamedTuple


class ModuleState(NamedTuple):
    name: str
    desc: str
    channel_id: int
    role_id: int


class Database:
    conn = None

    def create_tables(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS modules ("
                  "name VARCHAR(16),"
                  "desc VARCHAR(16), "
                  "channel_id VARCHAR(16),"
                  "role_id VARCHAR(16),"
                  "UNIQUE(name, channel_id, role_id), PRIMARY KEY(name))")
        c.execute(
            "CREATE TABLE IF NOT EXISTS scale_targets (id VARCHAR(16), template TEXT, UNIQUE(id), PRIMARY KEY(id))")

    def start_add_module(self, name: str, desc: str):
        c = self.conn.cursor()
        c.execute("INSERT INTO modules(name, desc) VALUES (?, ?)", (name, desc))
        self.conn.commit()

    def remove_module(self, name: str):
        c = self.conn.cursor()
        c.execute("DELETE FROM modules WHERE name=?", (name, ))
        self.conn.commit()

    def finish_add_module(self, name: str, channel_id: str, role_id: str):
        c = self.conn.cursor()
        c.execute("UPDATE modules SET channel_id=?, role_id=? WHERE name=?", (channel_id, role_id, name))
        self.conn.commit()

    def check_module(self, name: str):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(name) FROM modules WHERE name=?", (name,))
        return c.fetchone()[0] == 1

    def get_modules(self):
        c = self.conn.cursor()
        c.execute("SELECT name FROM modules")
        return [i[0] for i in c.fetchall()]

    def get_module(self, name: str):
        c = self.conn.cursor()
        c.execute("SELECT name, desc, channel_id, role_id FROM modules WHERE name=?", (name,))
        res = c.fetchone()
        return ModuleState(name=res[0], desc=res[1], channel_id=int(res[2]), role_id=int(res[3]))

    def add_scale_target(self, channel_id: str, template: str):
        c = self.conn.cursor()
        c.execute("INSERT INTO scale_targets(id, template) VALUES (?, ?)", (channel_id, template))
        self.conn.commit()

    def get_scale_targets(self, channel_id: str):
        c = self.conn.cursor()
        c.execute("SELECT name FROM scale_targets")
        return [i[0] for i in c.fetchall()]

    def __init__(self):
        self.conn = sqlite3.connect("db")
        self.create_tables()

db = Database()
