from uuid import UUID

from pydantic import BaseModel, condecimal, validator, Field


class ClientRequestSchema(BaseModel):
    first_name: str = Field(..., title='Имя пользователя', example='MyName')
    amount: condecimal(max_digits=30, decimal_places=2) = Field(
        ..., title='Баланс счёта внутри системы', example=1000.50,
    )


class ClientResponseSchema(ClientRequestSchema):
    auth_key: str = Field(..., title='Ключ авторизации', example='3e3a9282-023a-4f3b-ab59-de0fe4581e9c')

    @validator('auth_key', pre=True, always=True)
    def get_auth_key(cls, value: UUID):
        return str(value)

    class Config:
        orm_mode = True


class ClientDBSchema(ClientResponseSchema):
    id: int = Field(..., title='id пользователя внутри системы', example=1)
