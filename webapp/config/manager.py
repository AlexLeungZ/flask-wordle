from dataclasses import dataclass, field
from multiprocessing.managers import BaseManager


@dataclass
class _global:
    # Object can be reassigned here
    words: list[str] = field(default_factory=list)


# Attributes as Global Variable
# Attributes are non-reassignable, but sub attributes can be reassigned
class FlaskManager(BaseManager):
    gvar: _global = _global()
