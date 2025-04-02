from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Message_Schema_Response(JSONResponse):
    def __init__(self, status_code: int, message: str):
        content = {
            "message": message
        }
        super().__init__(status_code=status_code, content=content)

class Message_Schema(BaseModel):
    message: str
