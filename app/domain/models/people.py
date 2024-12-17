from dataclasses import dataclass
from random import randint
from typing import Optional

@dataclass
class People:
    name:               str
    sugestao_presente:  str
    id:                 Optional[int] = None
    codigo:             Optional[int] = None
    group_id:           Optional[int] = None
