from dataclasses import dataclass, field
from typing import List

@dataclass
class LModule:
    symbol: str = ''
    parameters: List[str] = field(default_factory=list)