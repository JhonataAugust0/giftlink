from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class People:
    name:               str
    gift_suggestion:    str
    email:              str
    hashed_password:    str
    salt:               str = ''
    is_active:          bool = True
    created_at:         datetime = datetime.now()
    id:                 Optional[int] = None
    code:               Optional[int] = None
    group_id:           Optional[int] = None
