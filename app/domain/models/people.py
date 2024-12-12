from dataclasses import dataclass
from random import randint

@dataclass
class People:
    name:               str
    sugestao_presente:  str
    id:                 int | None = None
    codigo:             int | None = None
    group_id:           int | None = None
