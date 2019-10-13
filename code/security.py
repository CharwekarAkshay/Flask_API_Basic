from werkzeug.security import safe_str_cmp
from user import User

# Old Code

# users = [User(1,"akshay","coldcoder")]

# username_mapping = {"akshay": {
#     "id": 1, "username": "akshay", "password": "coldcoder"}}

# userid_mapping = {1: {"id": 1, "username": "akshay", "password": "coldcoder"}}

# username_mapping = { u.username: u  for u in users }
# userid_mapping = { u.id : u for u in users }


def authenticate(username, password):
    # we can set default value with get method but we can't do it with square bracket
    # user = username_mapping.get(username, None)
    user = User.find_by_username(username);
    if user and safe_str_cmp(password, user.password):
        return user
    else: 
        return {"message": "Message can't be retrive"}


def identity(payload):
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return User.find_by_id(user_id);
