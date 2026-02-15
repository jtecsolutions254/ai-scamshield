from pydantic import BaseModel

class AnalyzeURLRequest(BaseModel):
    url: str
