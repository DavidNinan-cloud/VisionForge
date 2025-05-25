from pydantic import BaseModel
from typing import Dict, Any, Optional

class GPTCommandRequest(BaseModel):
    action: str
    params: Optional[Dict[str, Any]] = {}
