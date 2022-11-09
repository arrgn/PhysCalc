from db_module import DAO
from path_module import path_to_userdata, copy_file, create_dir


class User:
    def __init__(self, database=None):
        self.name = "guest"
        self.id = 0
        self.dao = None
        if database is not None:
            self.dao = database

    def add_user(self, name, password):
        try:
            self.dao.add_user(name, password)
            self.name = name
            self.id = str(self.dao.get_user_by_name(self.name)[0][0])
            create_dir(self.id)
            copy_file(path_to_userdata("default.png", "default"), self.id)
            return True
        except DAO.UserExistsError as e:
            print(e)
            return False

    def set_user(self, name, password):
        try:
            res = self.dao.get_checked_user(name, password)
            self.name = name
            self.id = str(self.dao.get_user_by_name(self.name)[0][0])
            return res
        except DAO.UserDoesntExistError as e:
            print(e)
            return False

    def get_user(self):
        return self.name

    def get_user_id(self):
        return self.id

    def get_avatar(self):
        try:
            res = self.dao.get_user_by_name(self.name)
            if not res:
                raise DAO.UserDoesntExistError(f"user with name {self.name} doesnt exist")
            return res[0][2]
        except DAO.UserDoesntExistError as e:
            print(e)
            return False

    def change_username(self, new_name):
        try:
            res = self.dao.change_username(self.name, new_name)
            self.name = new_name
            return True
        except DAO.UserDoesntExistError as e:
            print(e)
            return False
        except DAO.UserExistsError as e:
            print(e)
            return False

    def change_avatar(self, avatar="default.png"):
        try:
            res = self.dao.change_avatar(self.name, avatar)
            return True
        except DAO.UserDoesntExistError as e:
            print(e)
            return False

    def delete_user(self):
        try:
            res = self.dao.delete_user_by_name(self.name)
            return res
        except DAO.UserDoesntExistError as e:
            print(e)
            return False

    def get_workspaces(self):
        try:
            res = self.dao.get_workspaces_by_user(self.name)
            return res
        except DAO.UserDoesntExistError as e:
            print(e)
            return False

    def get_workspace(self, ws_name):
        try:
            res = self.dao.get_workspace(self.name, ws_name)
            return res
        except (DAO.UserDoesntExistError, DAO.WorkspaceNotFoundError) as e:
            print(e)
            return False

    def add_workspace(self, ws_name, file, description=""):
        try:
            self.dao.add_workspace_to_user(self.name, ws_name, file, description)
            return True
        except DAO.UserDoesntExistError as e:
            print(e)
            return False

    def delete_workspace(self, ws_name):
        try:
            res = self.dao.delete_workspace_from_user(self.name, ws_name)
            return res
        except (DAO.UserDoesntExistError, DAO.WorkspaceNotFoundError) as e:
            print(e)
            return False
