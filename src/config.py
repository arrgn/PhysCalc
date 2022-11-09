from db_module import DAO
from user_model import User

path_to_db = "db.db"
# default_user: list[str(username), str(password)]
default_user = ["guest", ""]

dao = DAO(path_to_db)
user = User(database=dao)
user.add_user(*default_user)
