from sqlite3 import connect
from config import path_to_file


class DAO:
    class UserExistsError(Exception):
        pass

    class UserDoesntExistError(Exception):
        pass

    def __init__(self):
        self.con = connect(path_to_file("db.db"))
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
        self.cur = self.con.cursor()
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


if __name__ == "__main__":
    a = DAO()
    try:
        a.add_user("123", "qwerty")
    except DAO.UserExistsError as e:
        a.delete_user_by_name("123")
    print(a.get_user_by_name("123"))
