from pydantic import BaseModel



class Account_schema(BaseModel):
  name: str



class Account_schema_response(Account_schema):
  id: str