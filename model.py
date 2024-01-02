from pydantic import BaseModel
from typing import List



class Values(BaseModel):
    id: int
    Accuracy: float
    conf_matrix: List[List[int]]
    roc_auc: float
