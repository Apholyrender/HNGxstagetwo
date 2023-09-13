from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schema import Account_schema, Account_schema_response
from app.services import create_user, get_all_users, get_single_user, update_user, delete_user

router = APIRouter()


@router.get("/api")
def read_accounts():
  accounts, Error = get_all_users()

  if Error:
    return JSONResponse(status_code=500, content={"msg":"failed to get users"})
  
  if accounts is None:
    return JSONResponse(status_code=404, content={"msg":"no users found"})
  return [Account_schema_response(id= str(account.id), name=account.name) for account in accounts]



@router.get("/api/{name}")
def read_account(name: str):
  account, error = get_single_user(name)
      
  if error:
    return JSONResponse(status_code=error.code, content={"msg":error.msg})
  if not account:
    return JSONResponse(status_code=404, content={"msg":"user not found"})
  return Account_schema_response(id= str(account.id), name=account.name).model_dump()

@router.post("/api")
def create_account(request: Account_schema):
    account, error = create_user(request)

    if error:
        return JSONResponse(status_code=error.code, content={"msg":error.msg})

    if not account:
        return JSONResponse(status_code=500, content={"msg":"failed to create user"})
    print(account.to_dict())
    return JSONResponse(content=Account_schema_response(id= str(account.id), name=account.name).model_dump(), status_code=201)


@router.put("/api/{name}")
def update_account(name: str, request: Account_schema):
  account, error = get_single_user(name)

  if error:
    return JSONResponse(status_code=error.code, content={"msg":error.msg})

  if not account:
    return JSONResponse(status_code=404, content={"msg":"user not found"})

  account, error = update_user(
    account_object=account,
    name=request.name,
    )

  if error:
    return JSONResponse(status_code=error.code, content=error.msg)

  if not account:
    return JSONResponse(status_code=500, content={"msg":"failed to update user"})

  return Account_schema_response(id= str(account.id), name=account.name).model_dump()


@router.delete("/api/{name}")
def delete_account(name: str):
  account, error = get_single_user(name)

  if error:
    return JSONResponse(status_code=error.code, content={"msg":error.msg})

  if not account:
    return JSONResponse(status_code=404, content={"msg":"user not found"})

  account, error = delete_user(account)

  if error:
    return JSONResponse(status_code=error.code, content={"msg":error.msg})

  if not account:
    return JSONResponse(status_code=500, content={"msg":"failed to delete user"})

  return JSONResponse(status_code=204, content={})