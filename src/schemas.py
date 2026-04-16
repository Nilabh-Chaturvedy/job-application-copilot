from pydantic import BaseModel
from typing import List

class plan(BaseModel):

    steps : List[str]