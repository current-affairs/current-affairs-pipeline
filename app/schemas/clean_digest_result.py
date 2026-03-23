from typing import Any, Dict, List

from pydantic import BaseModel


class CleanDigestResult(BaseModel):
    status: str
    total_processed: int
    successful_updates: int
    failed_updates: int
    warnings: List[Dict[str, Any]]
    errors: List[Dict[str, Any]]