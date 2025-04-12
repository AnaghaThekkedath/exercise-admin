# stores the models for the appliction

from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class Exercise:
    id: str
    type: str
    muscle_group: str
    info: Optional[str] = None

    @classmethod
    def create(cls, type: str, muscle_group: str, info: Optional[str] = None) -> 'Exercise':
        return cls(
            id=str(uuid.uuid4()),
            type=type,
            muscle_group=muscle_group,
            info=info
        )