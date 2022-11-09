from db_module import DAO


class User:
    def __init__(self, name=None, database=None):
        self.name = None
        self.dao = None
        if name is not None:
            self.name = name
        if database is not None:
            self.dao = database

    def add_user(self, name, password):
        try:
            self.dao.add_user(name, password)
            self.name = name
            return True
        except DAO.UserExistsError as e:
            print(e)
            return False

    def set_user(self, name, password):
        try:
            res = self.dao.get_checked_user(name, password)
            self.name = name
            return res
        except DAO.UserDoesntExistError as e:
            print(e)
            return False

    def get_user(self):
        return self.name

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
