from dataclasses import dataclass
from typing import Optional

@dataclass
class Keys:
    public_key:     str
    private_key:    str
    user_id:        Optional[int] = None