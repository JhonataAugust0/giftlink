from dataclasses import dataclass
from typing import Optional

@dataclass
class Draw:
    id: Optional[int] = None
    grupo_id: int
    participante_id: int
    sorteado_id: int
