from db_module import DAO
from path_module import path_to_userdata, copy_file, create_user_dir
from loggers import logger


class User:
    def __init__(self, database=None):
        self.name = "guest"
        self.id = 1
        self.dao = None
        if database is not None:
            self.dao = database

    def log_out(self):
        try:
            res = self.dao.get_user_by_id(1)
            self.name = res[0][1]
            self.id = 1
            return res
        except DAO.UserDoesntExistError:
            logger.exception("Tracked exception occurred!")
        return False

    def add_user(self, name, password):
        try:
            self.dao.add_user(name, password)
            self.name = name
            self.id = str(self.dao.get_user_by_name(self.name)[0][0])
            create_user_dir(self.id)
            copy_file(path_to_userdata("default.png", "default"), self.id)
            return True
        except DAO.UserExistsError:
            logger.exception("Tracked exception occurred!")
        return False

    def set_user(self, name, password):
        try:
            res = self.dao.get_checked_user(name, password)
            self.name = name
            self.id = str(self.dao.get_user_by_name(self.name)[0][0])
            return res
        except DAO.UserDoesntExistError:
            logger.exception("Tracked exception occurred!")
        return False

    def get_user(self):
        return self.name

    def get_user_id(self):
        return self.id

    def get_users(self):
        return self.dao.get_users()

    def get_avatar(self):
        try:
            res = self.dao.get_user_by_name(self.name)
            if not res:
                raise DAO.UserDoesntExistError(f"user with name {self.name} doesnt exist")
            return res[0][2]
        except DAO.UserDoesntExistError:
            logger.exception("Tracked exception occurred!")
        return False

    def change_username(self, new_name):
        try:
            res = self.dao.change_username(self.name, new_name)
            self.name = new_name
            return True
        except DAO.UserDoesntExistError:
            logger.exception("Tracked exception occurred!")
        except DAO.UserExistsError:
            logger.exception("Tracked exception occurred!")
        return False

    def change_avatar(self, avatar="default.png"):
        try:
            res = self.dao.change_avatar(self.name, avatar)
            return True
        except DAO.UserDoesntExistError:
            logger.exception("Tracked exception occurred!")
        return False

    def delete_user(self):
        try:
            res = self.dao.delete_user_by_name(self.name)
            return res
        except DAO.UserDoesntExistError:
            logger.exception("Tracked exception occurred!")
        return False

    def get_workspaces(self):
        """
        Get ALL workspaces from user
        """
        try:
            dao_res = self.dao.get_workspaces_by_user(self.name)
            res = list(map(lambda x: {
                "title": x[0],
                "file": x[1],
                "description": x[2]
            }, dao_res))
            return res
        except DAO.UserDoesntExistError:
            logger.exception("Tracked exception occurred!")
        return False

    def get_workspace(self, ws_name):
        """
        Get CURRENT workspace from user
        """
        try:
            res_dao = self.dao.get_workspace(self.name, ws_name)[0]
            res = {
                "user_id": res_dao[0],
                "title": res_dao[1],
                "file": res_dao[2],
                "description": res_dao[3]
            }
            return res
        except (DAO.UserDoesntExistError, DAO.WorkspaceNotFoundError):
            logger.exception("Tracked exception occurred!")
        return False

    def add_workspace(self, ws_name, file, description=""):
        try:
            self.dao.add_workspace_to_user(self.name, file, ws_name, description)
            return True
        except DAO.UserDoesntExistError:
            logger.exception("Tracked exception occurred!")
        return False

    def delete_workspace(self, ws_name):
        try:
            res = self.dao.delete_workspace_from_user(self.name, ws_name)
            return res
        except (DAO.UserDoesntExistError, DAO.WorkspaceNotFoundError):
            logger.exception("Tracked exception occurred!")
        return False
