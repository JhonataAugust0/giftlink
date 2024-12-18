from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RecoveryToken:
    id: Optional[int] = None
    user_id: int = 0
    token: str = ''
    expires_at: datetime = datetime.utcnow()
    is_used: bool = False