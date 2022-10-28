from pydantic import BaseModel, Field, EmailStr, validator


class GetUserListResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    email: EmailStr = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")

    class Config:
        orm_mode = True


class CreateUserRequestSchema(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Password1")
    nickname: str = Field(..., description="Nickname")


class CreateUserResponseSchema(BaseModel):
    email: EmailStr = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")

    class Config:
        orm_mode = True


class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Password")


class LoginResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class ExceptionResponseSchema(BaseModel):
    error: str
