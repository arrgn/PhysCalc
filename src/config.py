from db_module import DAO
from user_model import User

path_to_db = "db.db"
# default_user: list[str(username), str(password)]
default_user = ["default", ""]

dao = DAO(path_to_db, default_user)
user = User(dao.get_user_by_name(default_user[0])[0][1], dao)
