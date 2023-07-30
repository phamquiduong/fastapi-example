from datetime import datetime

from pydantic import BaseModel, ConfigDict

from auth.constants.token_constant import TokenType


class TokenSchema(BaseModel):
    token: str

    type: TokenType
    exp: datetime

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "token": ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl9pZCI6MSwidHlwZSI6ImFjY2VzcyJ9LCJle"
                      "HAiOjE2OTA2ODUxODh9.j0uiS4pW_-jKGYwq5PIJEDWLPUztBNdlWvuLZCsGd6s"),
            "type": "access",
            "exp": "2023-07-30T02:46:28.655614"}})


class AuthTokenSchema(BaseModel):
    access_token: TokenSchema
    refresh_token: TokenSchema

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "access_token": {
                "token": ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl9pZCI6MSwidHlwZSI6ImFjY2Vzcy"
                          "J9LCJleHAiOjE2OTA2ODU0MDR9.rEtN-LqpLEvZAFOMetRCpDYe3Gavq_OuhZDAe98aDSE"),
                "type": "access",
                "exp": "2023-07-30T02:50:04.570854"
            },
            "refresh_token": {
                "token": ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl9pZCI6MSwidHlwZSI6InJlZnJlc2g"
                          "ifSwiZXhwIjoxNjk1ODY4NTA0fQ.bt_FF9GScsBSt-8w_nsWNc1Pr_ZsvcIvPj_Zc0r-0iQ"),
                "type": "refresh",
                "exp": "2023-09-28T02:35:04.570866"
            }
        }})


class OAuth2PasswordBearerTokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
