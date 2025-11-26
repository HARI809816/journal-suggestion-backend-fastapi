from pydantic import BaseModel
from typing import Optional

class JournalColumnsResponse(BaseModel):
    _id: Optional[str] = None
    Journal_Name: Optional[str] = None
    Special_Issue_Name: Optional[str] = None
from pydantic import BaseModel
from typing import Optional

class JournalColumnsResponse(BaseModel):
    _id: Optional[str] = None
    Journal_Name: Optional[str] = None
    Special_Issue_Name: Optional[str] = None
    Special_Issue_keywords: Optional[str] = None

    class Config:
        populate_by_name = True  # This allows field names with underscores
        arbitrary_types_allowed = True
        orm_mode = True
        from_attributes = True
        protected_namespaces = ()

class RecommendationInput(BaseModel):
    Journal_Name: str
    Special_Issue_Name: str
    Similarity_Score: float
    Qdrant_id: Optional[str] = None
    Special_Issue_keywords: Optional[str] = None