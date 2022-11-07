from sqlite3 import connect
from config import path_to_file


class DAO:
    class UserExistsError(Exception):
        pass

    class UserDoesntExistError(Exception):
        pass

    def __init__(self, path_to_db="db.db"):
        self.con = connect(path_to_file(path_to_db))
        self.cur = self.con.cursor()
        build = """
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER           PRIMARY KEY
                           UNIQUE
                           NOT NULL,
    username VARCHAR (255) UNIQUE
                           NOT NULL,
    password VARCHAR (255) NOT NULL
);
        """
        self.cur.execute(build)
        build = """
CREATE TABLE IF NOT EXISTS workspaces (
    user_id      REFERENCES users (id) ON DELETE CASCADE
                 NOT NULL,
    file    TEXT NOT NULL,
    title    VARCHAR(255) NOT NULL,
    description TEXT
);
        """
        self.cur.execute(build)

    def get_user_by_name(self, name):
        sql = """SELECT * FROM users WHERE username=?"""
        return list(self.cur.execute(sql, [name]))

    def add_user(self, name, passwd):
        if self.get_user_by_name(name):
            raise self.UserExistsError(f"user with name {name} already exists")
        sql = """INSERT INTO users(username, password) VALUES(?, ?)"""
        res = list(self.cur.execute(sql, [name, passwd]))
        self.con.commit()
        return list(res)

    def delete_user_by_name(self, name):
        if not self.get_user_by_name(name):
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """DELETE FROM users WHERE username=?"""
        res = self.cur.execute(sql, [name])
        self.con.commit()
        return list(res)

    def add_workspace_to_user(self, name, file, title, description):
        user = self.get_user_by_name(name)
        if not user:
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """INSERT INTO workspaces VALUES(?, ?, ?, ?)"""
        res = self.cur.execute(sql, [user[0][0], file, title, description])
        self.con.commit()
        return list(res)

    def get_workspaces_by_user(self, name):
        user = self.get_user_by_name(name)
        if not user:
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """SELECT * FROM workspaces JOIN users ON id=user_id WHERE id=?"""
        res = self.cur.execute(sql, [user[0][0]])
        self.con.commit()
        return list(map(lambda x: x[:4], res))

    def delete_workspace_from_user(self, name, file):
        user = self.get_user_by_name(name)
        if not user:
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """DELETE FROM workspaces WHERE user_id=? AND file=?"""
        res = self.cur.execute(sql, [user[0][0], file])
        self.con.commit()
        return list(res)


if __name__ == "__main__":
    a = DAO()
    try:
        a.add_user("123", "qwerty")
    except DAO.UserExistsError as e:
        print(e)
    a.add_workspace_to_user("123", "a.txt", "MFW", "My First Workspace")
    print(a.get_user_by_name("123"))
    workspaces = a.get_workspaces_by_user("123")
    if len(workspaces) > 5:
        a.delete_workspace_from_user("123", "a.txt")
    print(a.get_workspaces_by_user("123"))
