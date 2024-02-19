from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserDelete(BaseModel):
    id: int


class UserUpdate(UserBase):
    id: int
    password: str


class UserInDB(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class OpenAIRequest(BaseModel):
    prompt: str
    engine: str = "gpt-3.5-turbo"
    max_tokens: int = 50
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class OpenAIResponse(BaseModel):
    completion: str
