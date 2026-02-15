from pydantic import BaseModel
from typing import Optional

class AnalyzeSMSRequest(BaseModel):
    text: str
    sender: Optional[str] = None
