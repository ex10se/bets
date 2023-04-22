from uuid import UUID

from pydantic import BaseModel, condecimal, validator


class ClientRequestSchema(BaseModel):
    first_name: str
    amount: condecimal(max_digits=30, decimal_places=2)


class ClientResponseSchema(BaseModel):
    first_name: str
    amount: condecimal(max_digits=30, decimal_places=2)
    auth_key: str

    @validator("auth_key", pre=True, always=True)
    def get_auth_key(cls, value: UUID):
        return str(value)

    class Config:
        orm_mode = True


class ClientDBSchema(ClientResponseSchema):
    id: int
