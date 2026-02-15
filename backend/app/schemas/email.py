from pydantic import BaseModel
from typing import Optional

class AnalyzeEmailRequest(BaseModel):
    subject: Optional[str] = None
    sender: Optional[str] = None
    body: str
    headers_raw: Optional[str] = None
