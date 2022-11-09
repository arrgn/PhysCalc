from sqlite3 import connect
from path_module import path_to_file, path_to_userdata


class DAO:
    class UserExistsError(Exception):
        pass

    class UserDoesntExistError(Exception):
        pass

    class WorkspaceNotFoundError(Exception):
        pass

    def __init__(self, path_to_db="db.db", default_user=None):
        if default_user is None:
            default_user = ["default", ""]
        self.con = connect(path_to_file(path_to_db))
        self.cur = self.con.cursor()
        build = """
CREATE TABLE IF NOT EXISTS users
(
    id       INTEGER PRIMARY KEY UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE        NOT NULL,
    password VARCHAR(255)               NOT NULL,
    avatar   TEXT                       NOT NULL
);
        """
        self.cur.execute(build)
        build = """
CREATE TABLE IF NOT EXISTS workspaces
(
    user_id REFERENCES users (id) ON DELETE CASCADE NOT NULL,
    file        TEXT                                NOT NULL,
    title       VARCHAR(255)                        NOT NULL,
    description TEXT
);
        """
        self.cur.execute(build)
        if not self.get_user_by_name(default_user[0]):
            self.add_user(default_user[0], default_user[1])

    def get_user_by_name(self, name):
        sql = """SELECT id, username, avatar FROM users WHERE username=?"""
        res = self.cur.execute(sql, [name])
        return list(res)

    def get_checked_user(self, name, password):
        if not self.get_user_by_name(name):
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """SELECT id, username, avatar FROM users WHERE username=? AND password=?"""
        res = self.cur.execute(sql, [name, password])
        return list(res)

    def add_user(self, name, passwd, avatar="default.png"):
        if self.get_user_by_name(name):
            raise self.UserExistsError(f"user with name {name} already exists")
        sql = """INSERT INTO users(username, password, avatar) VALUES(?, ?, ?)"""
        res = self.cur.execute(sql, [name, passwd, path_to_userdata(avatar, name)])
        self.con.commit()
        return list(res)

    def change_username(self, old_name, new_name):
        user = self.get_user_by_name(old_name)
        if not user:
            raise self.UserDoesntExistError(f"user with name {old_name} doesnt exist")
        candidate = self.get_user_by_name(new_name)
        if candidate:
            raise self.UserExistsError(f"user with name {new_name} already exists")
        sql = """UPDATE users SET username=? WHERE id=?"""
        res = self.cur.execute(sql, [new_name, user[0][0]])
        self.con.commit()
        return res

    def change_avatar(self, name, avatar="default.png"):
        user = self.get_user_by_name(name)
        if not user:
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """UPDATE users SET avatar=? WHERE id=?"""
        res = self.cur.execute(sql, [path_to_userdata(avatar, name), user[0][0]])
        self.con.commit()
        return res

    def delete_user_by_name(self, name):
        if not self.get_user_by_name(name):
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """DELETE FROM users WHERE username=?"""
        res = self.cur.execute(sql, [name])
        self.con.commit()
        return list(res)

    def add_workspace_to_user(self, username, file, title, description):
        user = self.get_user_by_name(username)
        if not user:
            raise self.UserDoesntExistError(f"user with name {username} doesnt exist")
        sql = """INSERT INTO workspaces VALUES(?, ?, ?, ?)"""
        res = self.cur.execute(sql, [user[0][0], file, title, description])
        self.con.commit()
        return list(res)

    def get_workspaces_by_user(self, name):
        user = self.get_user_by_name(name)
        if not user:
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """SELECT title, file, description FROM workspaces JOIN users ON id=user_id WHERE id=?"""
        res = self.cur.execute(sql, [user[0][0]])
        self.con.commit()
        return list(res)

    def get_workspace(self, name, ws_name):
        user = self.get_user_by_name(name)
        if not user:
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        sql = """SELECT title, file, description FROM workspaces JOIN users ON id=user_id WHERE id=? AND title=?"""
        res = self.cur.execute(sql, [user[0][0], ws_name])
        if not res:
            raise self.WorkspaceNotFoundError(f"workspace with name {ws_name} was not found at user {name}")
        return list(res)

    def delete_workspace_from_user(self, name, ws_name):
        user = self.get_user_by_name(name)
        if not user:
            raise self.UserDoesntExistError(f"user with name {name} doesnt exist")
        workspace = self.get_workspace(name, ws_name)
        if not workspace:
            raise self.WorkspaceNotFoundError(f"workspace with name {ws_name} was not found at user {name}")
        sql = """DELETE FROM workspaces WHERE user_id=? AND title=?"""
        res = self.cur.execute(sql, [user[0][0], ws_name])
        self.con.commit()
        return list(res)


if __name__ == "__main__":
    a = DAO()
    try:
        a.change_username("123", "456")
    except (DAO.UserDoesntExistError, DAO.UserExistsError) as e:
        print(e)
    try:
        a.add_user("default", "")
    except DAO.UserExistsError as e:
        print(e)
    try:
        a.add_user("123", "qwerty")
    except DAO.UserExistsError as e:
        print(e)
    a.add_workspace_to_user("123", "a.txt", "MFW", "My First Workspace")
    a.add_workspace_to_user("123", "b.txt", "MSW", "HAHAHA")
    a.add_workspace_to_user("default", "b.txt", "MFW", "HAHAHA")
    print(a.get_user_by_name("default"))
    workspaces = a.get_workspaces_by_user("123")
    if len(workspaces) > 10:
        a.delete_workspace_from_user("123", "MFW")
        a.delete_workspace_from_user("123", "MSW")
        print(a.get_workspaces_by_user("123"))
    print(a.get_workspace("123", "MFW"))
    print(a.get_workspaces_by_user("123"))
