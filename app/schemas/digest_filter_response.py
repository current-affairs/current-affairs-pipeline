

from typing import Literal

from pydantic import BaseModel, Field


class DigestFilterResponse(BaseModel):
    decision: Literal["ReadyToTake", "Ignore"] = Field(
        ..., 
        description="Whether to ReadyToTake or Ignore this news item for exam prep"
    )