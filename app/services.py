from app.schema import Account_schema
from app.models import Account_model
from app.DB import DB_CONNECT
from app.Error import Error
from bson.objectid import ObjectId
from bson.errors import InvalidId




def create_user(user:Account_schema):
  query_filter = {"name":user.name}

  if DB_CONNECT.count(query_filter) > 0:
    return None, Error("name already in use", 400)
  
  account = Account_model(
    id = ObjectId(),
    name = user.name
  )

  try:
    DB_CONNECT.create(account)
  except Exception as e:
    print(e)
    return None, Error("failed to create account", 500)
  return account, None


def get_all_users():
  accounts = DB_CONNECT.fetch_all()

  return accounts, None


def get_single_user(name:str):

  if name == "":
    return None, Error("name is required", 400)
  
  query_filter = {"name": name}
  try:
    account = DB_CONNECT.fetch_one(query_filter)
    if account:
      return account, None
    return None, Error("user not found", 404)
  except Exception as e:
    print(e)
    return None, Error("failed to get user", 500)
  

def update_user(name:str, account_object: Account_model = None):

  if name is not None:
    # check if name is already in use

    account, error = get_single_user(name)

    if account:
       return None, Error("name already in use", 400)
    account_object.name = name


  try:
      DB_CONNECT.update({"_id": account_object.id}, account_object.to_dict())
      return account_object, None
  except Exception:
      return None, Error("failed to update user", 500)
  

def delete_user(account: Account_schema):
  try:

    query_filter = {"_id": account.id}
    req = DB_CONNECT.delete(query_filter)

    return req, None
  
  except Exception:
    return None, Error("failed to delete account", 500)